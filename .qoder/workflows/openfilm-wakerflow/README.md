# OpenFilm WakerFlow

本目录是从四个链式自动任务迁移到单个 WakerFlow 的生产规范。

## 节点

整条 WakerFlow 在柔佛服务器运行，不跨设备调用 Worker：

1. 海外资料员：只读检索国外原始资料，返回结构化证据包。
2. 柔佛胶片编辑：选题避重并生成中文草稿。
3. 柔佛启航：翻译英文。
4. 柔佛画师：按 `OPENFILM-IMAGE-STYLE.md` 制作中英文两套同构技术图解，完成机器与视觉校验后分别上传、入稿。
5. 柔佛启航：校验、构建、提交、推送与线上验证。

## 切换原则

- 首次手动运行必须使用 `dry_run: true`。
- 完整测试成功前，旧自动任务保持原状。
- 完整测试通过后，先给 WakerFlow 添加原定时触发，再停用四个旧自动任务。
- `.pipeline/status.json` 和 `.pipeline/workflow.lock/` 继续用于业务幂等；WakerFlow 负责流程推进。
- WakerFlow 节点不得调用 `.pipeline/trigger-next.sh`。
