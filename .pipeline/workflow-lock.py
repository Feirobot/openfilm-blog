#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import shutil
from pathlib import Path

REPO = Path(os.environ.get("OPENFILM_REPO", "/root/AIwork/openfilm-blog"))
PIPELINE = REPO / ".pipeline"
STATUS_PATH = PIPELINE / "status.json"
LOCK_DIR = PIPELINE / "workflow.lock"
OWNER_PATH = LOCK_DIR / "owner.json"
TZ = dt.timezone(dt.timedelta(hours=8))


def read_json(path: Path, default: dict) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else default
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json_atomic(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def acquire() -> int:
    PIPELINE.mkdir(parents=True, exist_ok=True)
    try:
        LOCK_DIR.mkdir()
    except FileExistsError:
        owner = read_json(OWNER_PATH, {})
        print(json.dumps({"ok": False, "reason": "workflow_locked",
                          "workflow_run_id": owner.get("workflow_run_id")}, ensure_ascii=False))
        return 3

    try:
        status = read_json(STATUS_PATH, {})
        if status.get("workflow_state") == "running":
            print(json.dumps({"ok": False, "reason": "status_running",
                              "workflow_run_id": status.get("workflow_run_id")}, ensure_ascii=False))
            return 3
        now = dt.datetime.now(TZ)
        run_id = now.strftime("openfilm-%Y%m%d-%H%M%S")
        timestamp = now.isoformat(timespec="seconds")
        owner = {"workflow_run_id": run_id, "acquired_at": timestamp, "pid": os.getpid()}
        write_json_atomic(OWNER_PATH, owner)
        status.update({
            "workflow_run_id": run_id, "workflow_state": "running", "stage": "initializing",
            "current_stage": "initializing", "next_stage": "draft_created",
            "next_automation": None, "updated_at": timestamp, "retry_count": 0,
        })
        status.setdefault("history", []).append({
            "stage": "initializing", "at": timestamp, "by": "胶片编辑",
            "note": "已获取原子工作流锁，开始新一轮选题与写作。",
        })
        write_json_atomic(STATUS_PATH, status)
        print(json.dumps({"ok": True, "workflow_run_id": run_id, "stage": "initializing"}, ensure_ascii=False))
        return 0
    except Exception:
        shutil.rmtree(LOCK_DIR, ignore_errors=True)
        raise
    finally:
        if LOCK_DIR.exists() and not OWNER_PATH.exists():
            shutil.rmtree(LOCK_DIR, ignore_errors=True)


def release(run_id: str, force: bool) -> int:
    if not LOCK_DIR.exists():
        print(json.dumps({"ok": True, "released": False, "reason": "not_locked"}))
        return 0
    owner = read_json(OWNER_PATH, {})
    status = read_json(STATUS_PATH, {})
    if not force:
        if owner.get("workflow_run_id") != run_id or status.get("workflow_run_id") != run_id:
            print(json.dumps({"ok": False, "reason": "run_id_mismatch"}))
            return 4
        if status.get("workflow_state") not in {"completed", "failed"}:
            print(json.dumps({"ok": False, "reason": "workflow_not_finished",
                              "workflow_state": status.get("workflow_state")}))
            return 5
    shutil.rmtree(LOCK_DIR)
    print(json.dumps({"ok": True, "released": True, "workflow_run_id": run_id}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("acquire")
    release_parser = subparsers.add_parser("release")
    release_parser.add_argument("--run-id", required=True)
    release_parser.add_argument("--force", action="store_true")
    subparsers.add_parser("status")
    args = parser.parse_args()
    if args.command == "acquire":
        return acquire()
    if args.command == "release":
        return release(args.run_id, args.force)
    print(json.dumps({"locked": LOCK_DIR.exists(), "owner": read_json(OWNER_PATH, {})}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
