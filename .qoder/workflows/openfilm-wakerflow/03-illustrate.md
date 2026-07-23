# WakerFlow 节点 03：配图入稿

目标 Waker：画师-海外（`89087fa3cd33`）

1. 仅当状态为 `workflow_state: running` 且 `stage: translated` 时执行。
2. 先完整读取同目录 `OPENFILM-IMAGE-STYLE.md`。该规范是唯一允许的视觉风格，不得根据每篇主题临时更换画风。
3. 读取双语文章，选择 2-3 个相同的关键视觉场景，优先制作 3 组技术信息图。每组必须分别制作中文和英文 SVG，构图相同、文字本地化，不得共用图片 URL。
4. 不调用 ImageGen。参考文章的目标风格是可控 SVG 技术图解；随机位图风格、生成文字乱码和不可校验排版均不适用于本阶段。
5. 中文源文件写入 `.pipeline/generated/{slug}/sources/zh/01.svg` 等路径，英文写入 `sources/en/`。首图必须为 1:1，其他图为 16:9 或 4:3。
6. 生成完成后，必须先分别执行机器校验：

```bash
node .pipeline/validate-blog-images.js --locale zh \
  .pipeline/generated/{slug}/sources/zh/01.svg \
  .pipeline/generated/{slug}/sources/zh/02.svg

node .pipeline/validate-blog-images.js --locale en \
  .pipeline/generated/{slug}/sources/en/01.svg \
  .pipeline/generated/{slug}/sources/en/02.svg
```

按实际数量传入 2-3 个文件。任一校验失败，只修改失败文件并重新校验。

7. 两次机器校验通过后，逐张打开全部 SVG 或渲染图进行视觉复核。必须确认无文字裁切、越界、重叠、乱码、语言混用或事实性图解错误；中英文构图一一对应。无法完成视觉复核时必须失败，不能上传。
8. 只使用 `.pipeline/publish-media.js` 转换为 WebP、上传 R2 并验证公开 URL 与 Content-Type。运行前将 `OPENFILM_CF_MCP_CONFIG` 设置为当前海外画师的 `.mcp.json` 绝对路径。中文、英文分别执行：

```bash
OPENFILM_CF_MCP_CONFIG=/root/.qoder-alpha/extensions/89087fa3cd33/.mcp.json \
node .pipeline/publish-media.js \
  --slug {slug} \
  --manifest .pipeline/generated/{slug}/manifest.json \
  --locale zh \
  .pipeline/generated/{slug}/sources/zh/01.svg \
  .pipeline/generated/{slug}/sources/zh/02.svg

OPENFILM_CF_MCP_CONFIG=/root/.qoder-alpha/extensions/89087fa3cd33/.mcp.json \
node .pipeline/publish-media.js \
  --slug {slug} \
  --manifest .pipeline/generated/{slug}/manifest.json \
  --locale en \
  .pipeline/generated/{slug}/sources/en/01.svg \
  .pipeline/generated/{slug}/sources/en/02.svg
```

9. 只使用 `.pipeline/insert-blog-images.py` 将中文 URL 插入中文文章、英文 URL 插入英文文章，并推进状态。按场景数量分别传入中文和英文 alt：

```bash
python3 .pipeline/insert-blog-images.py \
  --manifest .pipeline/generated/{slug}/manifest.json \
  --zh-alt "中文说明 1" --zh-alt "中文说明 2" \
  --en-alt "English description 1" --en-alt "English description 2"
```

10. 校验、上传或入稿失败时立即停止，保持 `stage: translated`，在 history 追加 `illustration_failed`。不调用 MCP、Wrangler、npm/npx 安装或替代上传路径，不触发任何自动任务。

成功只返回 `{"status":"ok","stage":"images_generated","image_count":2,"image_count_per_locale":2,"image_file_count":4,"cover_ratio":"1:1","style":"technical-v1","layout_validated":true,"language_validated":true,"r2_verified":true,"workflow_run_id":"当前运行 ID"}`，其中 `image_count` 表示每种语言的场景数，数量使用实际值。

失败返回 `{"status":"failed","stage":"images_generated","error":"明确原因"}`。
