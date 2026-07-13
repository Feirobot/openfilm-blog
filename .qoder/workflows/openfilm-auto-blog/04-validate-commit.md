# OpenFilm 自动博客工作流 - 04 校验与提交

你是 `启航`。请在公共项目 `/root/AIwork/openfilm-blog` 中执行本阶段。

## 阶段目标

通过固定发布脚本完成双语文章校验、Astro 构建、Git 提交推送，以及 Cloudflare Pages 页面、RSS 和图片验证。

## 状态门禁

1. 读取 `.pipeline/status.json`。
2. 仅当 `workflow_state` 是 `running` 且 `stage` 是 `images_generated` 时执行。
3. 保留当前 `workflow_run_id`；否则输出“当前流水线未到校验提交阶段，跳过”，不修改文件。

## 固定执行路径

只运行以下命令：

```bash
cd /root/AIwork/openfilm-blog
timeout 22m python3 .pipeline/publish-blog.py
```

脚本会自动检查文章和图片、切换 draft、安装锁定依赖、运行 Astro 构建、受限暂存、标准 Git 推送，并在十分钟内验证双语页面、RSS 和全部图片。成功后它会完成状态和 topic 的更新、提交与推送。

## 工具使用规范与熔断

- 本阶段总工具调用上限为 6 次，正常情况只需读取状态、执行脚本、报告结果。
- 禁止手动拆分 npm、git、curl 命令；禁止调用 GitHub MCP；禁止搜索 Node、凭据或替代推送方式。
- 脚本失败时立即停止，原样报告脚本最后一条错误；不得自行重试整个脚本。
- 如果内容提交已推送但部署验证超时，不得回滚或再次推送内容，保留当前进行中状态供人工处理。

## 完成输出

仅报告构建结果、内容提交哈希、推送结果、中英文 URL、RSS 验证结果和当前 stage。
