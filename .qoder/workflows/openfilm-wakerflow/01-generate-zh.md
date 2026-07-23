# WakerFlow 节点 01：中文选题与草稿

目标 Waker：胶片编辑-海外（`b646dd76692e`）

## 输入

- WakerFlow 运行参数中的 `topic`。
- 上一节点返回的海外研究 JSON。

## 执行

1. 第一条命令必须是 `python3 .pipeline/workflow-lock.py acquire`。
2. 锁被占用或状态仍为 `running` 时，返回 `WORKFLOW_SKIPPED`，不得检索、写文件或启动新一轮。
3. 读取全部 `*-zh.mdx` 的 slug、title、description 和 tags，一次性完成选题避重。
4. 指定 `topic` 时，以该主题为约束；未指定时，从海外研究候选中选择与历史文章差异最大的角度。
5. 仅使用海外研究中 `accessed: true` 的来源；如需补充国内来源，仍须确保最终参考资料为 3-7 条直接页面。
6. 创建 `{english-slug}-zh.mdx`，frontmatter 包含 `title`、`description`、`pubDate`、`updatedDate`、`draft: true`、`tags`、`lang: "zh"`。
7. 正文建议 1000-1800 字，至少包含 3 个具体技术点和 1 个文化或审美判断。
8. 文末使用 `## 参考资料`，每条严格为 `- [描述](https://直接链接)`，总数 3-7。
9. 不翻译、不配图、不提交 Git。
10. 更新 `.pipeline/status.json`：保留锁创建的 `workflow_run_id`，设置 `workflow_state: running`、`stage/current_stage: draft_created`、`next_stage: translated`，写入 `article`，追加包含避重结论的 history。

## 固定术语

film photography=胶片摄影；film stock=胶片型号；emulsion=乳剂；grain=颗粒；latitude=宽容度；dynamic range=动态范围；exposure=曝光；metering=测光；negative=负片；slide/reversal film=反转片；push processing=增感冲洗；pull processing=减感冲洗；contact sheet=接触印相；darkroom=暗房；developer=显影液；fixer=定影液；stop bath=停显液；scanning=扫描；color cast=偏色；archival storage=档案保存；medium format=中画幅；large format=大画幅；rangefinder=旁轴相机；SLR=单反相机。

## 返回

成功时只返回：

```json
{"status":"ok","stage":"draft_created","article":"相对路径","title":"标题","workflow_run_id":"当前运行 ID"}
```

失败时返回 `{"status":"failed","stage":"draft_created","error":"明确原因"}`，不要触发任何其他自动任务。
