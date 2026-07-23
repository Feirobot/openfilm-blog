# WakerFlow 节点 04：校验与发布

目标 Waker：启航-海外（`dc1ab58b1923`）

1. 仅当状态为 `workflow_state: running` 且 `stage: images_generated` 时执行。
2. 只运行 `timeout 22m python3 .pipeline/publish-blog.py`。
3. 脚本负责引用格式、文章与图片、Astro 构建、draft 切换、受限暂存、提交、推送和线上页面/RSS/图片验证。
4. 已提交但未推送的重试必须由脚本恢复，不手工拆分 git、npm、curl 命令，不调用 GitHub MCP。
5. 失败时立即停止并返回脚本最后一条明确错误，不回滚、不重复提交。
6. 成功后确认状态为 `workflow_state: completed` 且 `stage: published`，锁已释放。

成功只返回：

```json
{
  "status": "ok",
  "stage": "published",
  "commit_hash": "提交哈希",
  "published_url": "中文 URL",
  "published_url_en": "英文 URL",
  "rss_verified": true,
  "workflow_run_id": "当前运行 ID"
}
```

失败返回 `{"status":"failed","stage":"published","error":"明确原因"}`。
