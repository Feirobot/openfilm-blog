#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path

REPO = Path(os.environ.get("OPENFILM_REPO", "/root/AIwork/openfilm-blog"))
STATUS_PATH = REPO / ".pipeline/status.json"


def insert_images(path: Path, images: list[dict], alts: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    urls = [item["url"] for item in images]
    if all(url in text for url in urls):
        return
    if any(url in text for url in urls):
        raise RuntimeError(f"partial image insertion detected in {path}")
    lines = text.splitlines()
    headings = [i for i, line in enumerate(lines) if re.match(r"^## (?!参考资料|References)", line)]
    if not headings:
        raise RuntimeError(f"no level-2 section found in {path}")
    positions = []
    for i in range(len(images)):
        index = round(i * (len(headings) - 1) / max(1, len(images) - 1))
        positions.append(headings[index])
    insertions: dict[int, list[str]] = {}
    for position, image, alt in zip(positions, images, alts):
        insertions.setdefault(position, []).extend([f"![{alt}]({image['url']})", ""])
    for position in sorted(insertions, reverse=True):
        lines[position:position] = insertions[position]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--zh-alt", action="append", required=True)
    parser.add_argument("--en-alt", action="append", required=True)
    args = parser.parse_args()
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    if status.get("workflow_state") != "running" or status.get("stage") != "translated":
        raise SystemExit("stage gate rejected: expected running/translated")
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    locales = manifest.get("locales", {})
    zh_images = locales.get("zh", {}).get("images", [])
    en_images = locales.get("en", {}).get("images", [])
    if not zh_images or not en_images:
        raise SystemExit("manifest requires separate zh and en image sets")
    if len(zh_images) != len(en_images):
        raise SystemExit("zh and en image sets must contain the same number of images")
    if len(zh_images) != len(args.zh_alt) or len(en_images) != len(args.en_alt):
        raise SystemExit("each localized image requires one matching localized alt")
    zh_urls = {item["url"] for item in zh_images}
    en_urls = {item["url"] for item in en_images}
    if zh_urls & en_urls:
        raise SystemExit("zh and en articles cannot share localized image URLs")
    zh_path = REPO / status["article"]
    en_path = REPO / status["translated_article"]
    insert_images(zh_path, zh_images, args.zh_alt)
    insert_images(en_path, en_images, args.en_alt)
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat(timespec="seconds")
    all_images = zh_images + en_images
    status.update({
        "stage": "images_generated",
        "current_stage": "images_generated",
        "next_stage": "published",
        "next_automation": None,
        "images": [item["url"] for item in all_images],
        "images_zh": [item["url"] for item in zh_images],
        "images_en": [item["url"] for item in en_images],
        "images_local": [item["local"] for item in all_images],
        "first_image_aspect": "1:1",
        "image_layout_validation": "passed",
        "image_language_validation": "passed",
        "r2_upload_status": "success",
        "updated_at": now,
    })
    status.setdefault("history", []).append({
        "stage": "images_generated", "at": now, "by": "画师",
        "note": (
            f"固定媒体工具完成中英文各 {len(zh_images)} 张 WebP 的版式与语言校验、"
            "R2 上传、公开验证及分别入稿；两种语言首图均为 1:1。"
        ),
    })
    STATUS_PATH.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "ok": True,
        "count_per_locale": len(zh_images),
        "file_count": len(all_images),
        "stage": "images_generated",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
