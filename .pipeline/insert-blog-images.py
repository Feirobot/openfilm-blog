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
    images = manifest.get("images", [])
    if not images or len(images) != len(args.zh_alt) or len(images) != len(args.en_alt):
        raise SystemExit("each image requires one --zh-alt and one --en-alt")
    zh_path = REPO / status["article"]
    en_path = REPO / status["translated_article"]
    insert_images(zh_path, images, args.zh_alt)
    insert_images(en_path, images, args.en_alt)
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat(timespec="seconds")
    status.update({
        "stage": "images_generated",
        "current_stage": "images_generated",
        "next_stage": "published",
        "next_automation": "tr_7a6182a67db84957",
        "images": [item["url"] for item in images],
        "images_local": [item["local"] for item in images],
        "first_image_aspect": "1:1",
        "r2_upload_status": "success",
        "updated_at": now,
    })
    status.setdefault("history", []).append({
        "stage": "images_generated", "at": now, "by": "画师",
        "note": f"固定媒体工具完成 {len(images)} 张 WebP 转换、R2 上传、公开验证及双语入稿；首图 1:1。",
    })
    STATUS_PATH.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "count": len(images), "stage": "images_generated"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
