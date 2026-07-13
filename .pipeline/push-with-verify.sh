#!/bin/bash
# push-with-verify.sh - 带验证和重试的 git push 脚本
# 用法: ./push-with-verify.sh [max_retries]

set -e

MAX_RETRIES=${1:-3}
RETRY_DELAY=5
REPO_DIR="/root/AIwork/openfilm-blog"

cd "$REPO_DIR"

push_and_verify() {
    local attempt=$1
    echo "=== 推送尝试 $attempt/$MAX_RETRIES ==="

    # 记录推送前的本地 HEAD
    LOCAL_HEAD=$(git rev-parse HEAD)
    echo "本地 HEAD: $LOCAL_HEAD"

    # 断点续跑时远端引用可能已经与本地一致，无需再访问网络。
    CURRENT_AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "unknown")
    if [ "$CURRENT_AHEAD" = "0" ]; then
        echo "远端引用已与本地同步，跳过重复推送"
        return 0
    fi

    # 执行推送（带超时）
    if timeout 180 git push origin main 2>&1; then
        echo "推送命令执行成功"
    else
        EXIT_CODE=$?
        if [ $EXIT_CODE -eq 124 ]; then
            echo "推送超时（180秒）"
        else
            echo "推送失败，退出码: $EXIT_CODE"
        fi
    fi

    # 验证推送是否成功
    # 刷新远程引用
    git fetch origin main --quiet 2>/dev/null || true

    REMOTE_HEAD=$(git rev-parse origin/main 2>/dev/null || echo "unknown")
    echo "远程 HEAD: $REMOTE_HEAD"

    # 检查本地是否领先远程
    AHEAD_COUNT=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "unknown")
    echo "本地领先远程: $AHEAD_COUNT 个提交"

    if [ "$AHEAD_COUNT" = "0" ]; then
        echo "✓ 推送验证成功：本地与远程同步"
        return 0
    else
        echo "✗ 推送验证失败：本地仍领先远程 $AHEAD_COUNT 个提交"
        return 1
    fi
}

# 主循环
for i in $(seq 1 $MAX_RETRIES); do
    if push_and_verify $i; then
        echo ""
        echo "=== 推送完成 ==="
        git log --oneline -1
        exit 0
    fi

    if [ $i -lt $MAX_RETRIES ]; then
        echo "等待 ${RETRY_DELAY}秒 后重试..."
        sleep $RETRY_DELAY
        RETRY_DELAY=$((RETRY_DELAY * 2))  # 指数退避
    fi
done

echo ""
echo "=== 推送失败：已尝试 $MAX_RETRIES 次 ==="
exit 1
