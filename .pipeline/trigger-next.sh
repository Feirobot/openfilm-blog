#!/bin/bash
set -euo pipefail

REPO_DIR="/root/AIwork/openfilm-blog"
STATUS_FILE="$REPO_DIR/.pipeline/status.json"
QODERWAKE="/root/.qoderwake-cn/bin/qoderwake-cn"

case "${1:-}" in
  translate)
    expected="draft_created"; waker="57517720e12a"; automation="tr_516ea4db27cb47d7" ;;
  illustrate)
    expected="translated"; waker="d9b25b78e908"; automation="tr_0e49b354967e4f3f" ;;
  publish)
    expected="images_generated"; waker="57517720e12a"; automation="tr_7a6182a67db84957" ;;
  *)
    echo "usage: $0 {translate|illustrate|publish}" >&2
    exit 2 ;;
esac

read -r state stage < <(python3 - "$STATUS_FILE" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    status = json.load(f)
print(status.get("workflow_state", ""), status.get("stage", ""))
PY
)

if [[ "$state" != "running" || "$stage" != "$expected" ]]; then
  echo "stage gate rejected: workflow_state=$state stage=$stage expected=$expected" >&2
  exit 3
fi

python3 "$REPO_DIR/.pipeline/repair-qoderwake-triggers.py" >/dev/null
timeout 60s "$QODERWAKE" automation run-now \
  --waker-id "$waker" \
  --automation-id "$automation"
