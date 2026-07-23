# OpenFilm 自动博客 WakerFlow 生成提示

创建名为“OpenFilm 自动博客发布”的 WakerFlow。

## 目标

把海外资料研究、中文选题与写作、英文翻译、配图入稿、校验发布编排为严格串行的单轮流程。流程中任何阶段失败时立即终止，不能继续派发后续 Worker；一轮未完成时不能启动下一轮。不要调用现有自动任务或 API trigger。

## 运行输入

- `topic`: string，可选，默认空字符串。为空时自主选题；非空时围绕该主题研究和写作。
- `dry_run`: boolean，默认 true。true 时只运行海外研究节点并返回证据包，不写博客；false 时运行完整发布流程。

## Worker 与顺序

1. Phase“海外资料研究”：调用海外资料员 Waker `a45ec168201e`。把 `args.topic` 传入，要求按其 BIBLE 返回严格 JSON。结果不是有效 JSON、`status` 不是 `ok`、候选数不符合要求，立即抛出错误。
2. `dry_run` 为 true 时，在研究阶段后显式 return，返回 `{status, mode, research}`。
3. Phase“中文草稿”：调用柔佛胶片编辑 `b646dd76692e`。指令要求先读取 `/root/AIwork/openfilm-blog/.qoder/workflows/openfilm-wakerflow/01-generate-zh.md`，并把 `args.topic` 与完整研究结果作为输入。解析返回 JSON；`status` 不是 `ok` 时立即抛出错误。
4. Phase“英文翻译”：调用柔佛启航 `dc1ab58b1923`，要求读取同目录 `02-translate-en.md`，并传入上一节点结果。失败立即终止。
5. Phase“配图入稿”：调用柔佛画师 `89087fa3cd33`，要求读取同目录 `03-illustrate.md`，并传入上一节点结果。失败立即终止。
6. Phase“校验发布”：继续调用柔佛启航 `dc1ab58b1923`，要求读取同目录 `04-validate-publish.md`，并传入上一节点结果。构建、Git 推送和线上验证必须全部在柔佛执行。失败立即终止。

## 编排要求

- 所有节点使用 `worker` 串行等待，不使用 parallel、pipeline 批处理、action、workflow 子流程或 askUser。
- 每个阶段用 `phase` 标记，`log` 只记录阶段名、业务 stage、文章路径、图片数量、提交哈希和错误摘要，不记录完整文章、完整研究 JSON 或凭据。
- Worker Result 可能是字符串；为每个结果实现统一的 JSON 提取与校验函数，允许去除外层 Markdown JSON 代码围栏，不允许猜测缺失字段。
- 研究节点失败时不获取仓库锁。中文节点返回 `WORKFLOW_SKIPPED` 或锁冲突时，流程以 `status: skipped` 正常结束，后续节点不得运行。
- 中文节点成功后任一后续阶段失败，保留仓库当前状态和锁供人工恢复，并在最终错误中包含失败阶段与 `workflow_run_id`。
- 脚本必须有显式 `return`。完整成功时返回：
  `{status:"completed", mode:"publish", workflow_run_id, article, translated_article, image_count, commit_hash, published_url, published_url_en, rss_verified}`。
- 不在脚本中硬编码密钥、令牌、API 地址或自动任务 ID。

生成后请展示画布和可编辑脚本，不要自动添加触发器。第一次测试将使用 `dry_run: true`。
