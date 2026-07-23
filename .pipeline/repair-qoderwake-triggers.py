#!/usr/bin/env python3
"""Keep retired OpenFilm automations disabled after the WakerFlow migration."""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path("/root/.qoderwake-cn/data/store/qoderwake.sqlite")
WORKSPACE = "/root/AIwork/openfilm-blog"
TRIGGER_IDS = (
    "tr_ad39249772024519",
    "tr_516ea4db27cb47d7",
    "tr_0e49b354967e4f3f",
    "tr_7a6182a67db84957",
)


def normalized_json(raw: str | None, *, payload: bool) -> str:
    value = json.loads(raw) if raw else {}
    if not isinstance(value, dict):
        value = {}
    value.pop("projectId", None)
    value.pop("projectName", None)
    if payload:
        value["executionTarget"] = "workspaceSource"
        value["workspaceSource"] = {"type": "file"}
        value["workspaceRef"] = WORKSPACE
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report drift without updating")
    args = parser.parse_args()
    if not DB_PATH.exists():
        print(f"database not found: {DB_PATH}", file=sys.stderr)
        return 2

    connection = sqlite3.connect(DB_PATH, timeout=15)
    connection.row_factory = sqlite3.Row
    placeholders = ",".join("?" for _ in TRIGGER_IDS)
    rows = connection.execute(
        f"SELECT trigger_id, enabled, execution_target, workspace_type, "
        f"workspace_ref, extensions, payload FROM triggers "
        f"WHERE trigger_id IN ({placeholders})",
        TRIGGER_IDS,
    ).fetchall()
    found = {row["trigger_id"] for row in rows}
    missing = sorted(set(TRIGGER_IDS) - found)
    drifted = []
    for row in rows:
        extensions = normalized_json(row["extensions"], payload=False)
        payload = normalized_json(row["payload"], payload=True)
        expected = (0, "workspaceSource", "file", WORKSPACE, extensions, payload)
        actual = tuple(row[key] for key in (
            "enabled", "execution_target", "workspace_type", "workspace_ref",
            "extensions", "payload",
        ))
        if actual != expected:
            drifted.append(row["trigger_id"])
            if not args.check:
                connection.execute(
                    "UPDATE triggers SET enabled = 0, execution_target = ?, "
                    "workspace_type = ?, workspace_ref = ?, extensions = ?, payload = ? "
                    "WHERE trigger_id = ?",
                    ("workspaceSource", "file", WORKSPACE, extensions, payload, row["trigger_id"]),
                )
    if not args.check:
        connection.commit()
    connection.close()
    if missing:
        print("missing triggers: " + ", ".join(missing), file=sys.stderr)
    if drifted:
        print(("detected" if args.check else "repaired") + " trigger drift: " + ", ".join(drifted))
    elif not missing:
        print("Retired OpenFilm trigger bindings are disabled")
    return 1 if missing or (args.check and drifted) else 0


if __name__ == "__main__":
    raise SystemExit(main())
