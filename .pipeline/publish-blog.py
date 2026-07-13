#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import time
import urllib.request
from pathlib import Path

REPO = Path(os.environ.get("OPENFILM_REPO", "/root/AIwork/openfilm-blog"))
STATUS_PATH = REPO / ".pipeline/status.json"
TOPIC_PATH = REPO / ".pipeline/topic.json"


def run(command: list[str], timeout: int = 600, capture: bool = False) -> str:
    result = subprocess.run(command, cwd=REPO, text=True, timeout=timeout,
                            stdout=subprocess.PIPE if capture else None,
                            stderr=subprocess.STDOUT if capture else None,
                            check=True)
    return (result.stdout or "").strip()


def http_ok(url: str, contains: str | None = None) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "OpenFilm-Pipeline/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8", "ignore") if contains else ""
            return response.status == 200 and (contains is None or contains in body)
    except Exception:
        return False


def frontmatter(text: str) -> tuple[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise RuntimeError("missing frontmatter")
    title = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', match.group(1), re.M)
    if not title:
        raise RuntimeError("missing frontmatter title")
    return match.group(0), title.group(1).strip('"\'')


def validate_references(text: str, heading: str, path: Path) -> None:
    match = re.search(rf"(?ms)^## {re.escape(heading)}\s*\n(.*?)(?=^## |^> |\Z)", text)
    if not match:
        raise RuntimeError(f"missing ## {heading} in {path}")
    entries = [line.strip() for line in match.group(1).splitlines() if line.strip()]
    if not 3 <= len(entries) <= 7:
        raise RuntimeError(f"{path} must contain 3-7 references, found {len(entries)}")
    pattern = re.compile(r"^- \[[^\]]+\]\(https://[^\s)]+\)$")
    invalid = [line for line in entries if not pattern.fullmatch(line)]
    if invalid:
        raise RuntimeError(f"invalid reference format in {path}: {invalid[0]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-references", nargs=2, metavar=("ZH_ARTICLE", "EN_ARTICLE"))
    args = parser.parse_args()
    if args.check_references:
        for filename, heading in zip(args.check_references, ("参考资料", "References")):
            path = Path(filename)
            validate_references(path.read_text(encoding="utf-8"), heading, path)
        print(json.dumps({"ok": True, "references": "valid", "articles": 2}))
        return
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    if status.get("workflow_state") != "running" or status.get("stage") != "images_generated":
        raise SystemExit("stage gate rejected: expected running/images_generated")
    article = REPO / status["article"]
    translated = REPO / status["translated_article"]
    for path, heading in ((article, "参考资料"), (translated, "References")):
        if not path.is_file():
            raise SystemExit(f"missing article: {path}")
        text = path.read_text(encoding="utf-8")
        frontmatter(text)
        validate_references(text, heading, path)
    images = status.get("images", [])
    if not images or not all(url.startswith("https://media.openfilm.cc/") for url in images):
        raise SystemExit("verified R2 images are required")
    if args.check:
        print(json.dumps({"ok": True, "stage": "images_generated", "articles": 2, "images": len(images)}))
        return

    originals = {path: path.read_text(encoding="utf-8") for path in (article, translated)}
    _, title = frontmatter(originals[article])
    draft_states = [bool(re.search(r"(?m)^draft:\s*true\s*$", text)) for text in originals.values()]
    if all(draft_states):
        resume_existing_commit = False
    elif not any(draft_states):
        resume_existing_commit = True
    else:
        raise RuntimeError("mixed draft states; both bilingual articles must agree")

    content_committed = resume_existing_commit
    try:
        if resume_existing_commit:
            clean = subprocess.run(["git", "diff", "--quiet", "--", status["article"],
                                    status["translated_article"]], cwd=REPO).returncode == 0
            if not clean:
                raise RuntimeError("draft is false but article files have uncommitted changes")
            article_commit = run(["git", "log", "-1", "--format=%H", "--", status["article"]], capture=True)
            translated_commit = run(["git", "log", "-1", "--format=%H", "--", status["translated_article"]], capture=True)
            if not article_commit or article_commit != translated_commit:
                raise RuntimeError("bilingual articles were not committed together")
            content_commit = article_commit[:7]
            print(json.dumps({"resume": True, "content_commit": content_commit}))
        else:
            for path, text in originals.items():
                updated, count = re.subn(r"(?m)^draft:\s*true\s*$", "draft: false", text, count=1)
                if count != 1:
                    raise RuntimeError(f"expected draft: true in {path}")
                path.write_text(updated, encoding="utf-8")
            run(["npm", "install", "--no-audit", "--no-fund"], timeout=600)
            run(["npm", "run", "build"], timeout=600)
            run(["git", "add", "--", status["article"], status["translated_article"],
                 ".pipeline/status.json", ".pipeline/topic.json"])
            staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO).returncode
            if staged == 0:
                raise RuntimeError("no staged content changes after preparing publication")
            run(["git", "commit", "-m", f"content: 新增文章《{title}》（含双语版本）"])
            content_committed = True
            content_commit = run(["git", "rev-parse", "--short", "HEAD"], capture=True)
        run(["timeout", "3m", ".pipeline/push-with-verify.sh", "2"], timeout=200)
    except Exception:
        if not content_committed:
            for path, text in originals.items():
                path.write_text(text, encoding="utf-8")
            subprocess.run(["git", "restore", "--staged", "--", status["article"],
                            status["translated_article"], ".pipeline/status.json", ".pipeline/topic.json"],
                           cwd=REPO, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        raise

    zh_slug = article.stem
    en_slug = translated.stem
    zh_url = f"https://openfilm.cc/zh/posts/{zh_slug}/"
    en_url = f"https://openfilm.cc/en/posts/{en_slug}/"
    checks = [(zh_url, None), (en_url, None), ("https://openfilm.cc/rss.xml", zh_slug)] + [(url, None) for url in images]
    deadline = time.monotonic() + 600
    while time.monotonic() < deadline:
        if all(http_ok(url, contains) for url, contains in checks):
            break
        time.sleep(15)
    else:
        raise SystemExit("deployment verification timed out; content commit is already pushed")

    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat(timespec="seconds")
    status.update({
        "workflow_state": "completed", "stage": "published", "current_stage": "published",
        "next_stage": None, "next_automation": None, "published_url": zh_url,
        "published_url_en": en_url, "commit_hash": content_commit, "updated_at": now,
    })
    status.setdefault("history", []).append({
        "stage": "published", "at": now, "by": "启航",
        "note": f"固定发布工具完成构建、推送及中英文页面、RSS、{len(images)} 张图片验证。内容提交 {content_commit}。",
    })
    STATUS_PATH.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    TOPIC_PATH.write_text('{"topic": null}\n', encoding="utf-8")
    run(["git", "add", "--", ".pipeline/status.json", ".pipeline/topic.json"])
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO).returncode != 0:
        run(["git", "commit", "-m", f"chore: 完成工作流 {status.get('workflow_run_id', '')}"])
    run(["timeout", "3m", ".pipeline/push-with-verify.sh", "2"], timeout=200)
    print(json.dumps({"ok": True, "stage": "published", "commit": content_commit,
                      "zh_url": zh_url, "en_url": en_url, "rss": "verified"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
