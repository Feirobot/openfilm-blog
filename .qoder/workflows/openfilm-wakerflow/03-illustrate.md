# WakerFlow 节点 03：配图入稿

目标 Waker：画师-海外（`89087fa3cd33`）

1. 仅当状态为 `workflow_state: running` 且 `stage: translated` 时执行。
2. 读取双语文章，设计 1-3 张有技术信息的主题插画；首图必须为 1:1，其他图可为 16:9 或 4:3。
3. ImageGen 最多调用一次。成功时保存源图；遇到 provider、格式、鉴权或服务端错误时不得重试，改写 SVG 源文件。
4. SVG 只能作为转换源，不能直接上传或插入文章。
5. 只使用 `.pipeline/publish-media.js` 转换为 WebP、上传 R2 并验证公开 URL 与 Content-Type。运行前将 `OPENFILM_CF_MCP_CONFIG` 设置为当前海外画师的 `.mcp.json` 绝对路径。
6. 只使用 `.pipeline/insert-blog-images.py` 将图片和双语 alt 插入文章并推进状态。
7. 发布或入稿脚本失败时立即停止，保持 `stage: translated`，在 history 追加 `illustration_failed`。
8. 不调用 MCP、Wrangler、npm/npx 安装或替代上传路径，不触发任何自动任务。

成功只返回 `{"status":"ok","stage":"images_generated","image_count":1,"cover_ratio":"1:1","r2_verified":true,"workflow_run_id":"当前运行 ID"}`，其中数量使用实际值。

失败返回 `{"status":"failed","stage":"images_generated","error":"明确原因"}`。
