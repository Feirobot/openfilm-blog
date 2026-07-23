# WakerFlow 节点 02：英文翻译

目标 Waker：启航-海外（`dc1ab58b1923`）

1. 仅当 `.pipeline/status.json` 为 `workflow_state: running` 且 `stage: draft_created` 时执行。
2. 沿用当前 `workflow_run_id`，从 `status.article` 读取中文文章。
3. 创建同 slug 的 `-en.mdx`，翻译 title、description、tags 和正文，保留日期、MDX 结构、组件、图片语法与代码块，设置 `lang: "en"`、`draft: true`。
4. 将 `## 参考资料` 翻译为 `## References`，URL 不变，保持 3-7 条 `- [Description](https://...)`。
5. 为双语文章加入互相跳转入口。
6. 更新状态为 `translated`，写入 `translated_article`、`next_stage: images_generated` 并追加 history。
7. 不配图、不构建、不提交 Git，不触发任何自动任务。

成功只返回 `{"status":"ok","stage":"translated","article":"中文路径","translated_article":"英文路径","workflow_run_id":"当前运行 ID"}`。

失败返回 `{"status":"failed","stage":"translated","error":"明确原因"}`。
