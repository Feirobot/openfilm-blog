# RSS 订阅源验证报告

**验证时间**: 2026-06-15  
**验证目标**: https://openfilm.cc/rss.xml  
**本地项目**: /root/AIwork/openfilm-blog

---

## 1. RSS 格式验证

| 检查项 | 结果 | 说明 |
|--------|------|------|
| XML 声明 | PASS | `<?xml version="1.0" encoding="UTF-8"?>` |
| RSS 版本 | PASS | RSS 2.0 |
| `<channel>` 结构 | PASS | 正确闭合 |
| title | PASS | `Openfilm` |
| link | PASS | `https://openfilm.cc/` |
| description | PASS | `Notes, essays, and experiments from Openfilm.` |
| lastBuildDate | **FAIL** | **线上版本缺失此字段** |
| Item 数量 | PASS | 21 个 item |
| Item 必填字段 | PASS | 所有 item 均含 title, link, guid, description, pubDate |

## 2. RSS Item 清单

| # | 标题 | 链接 | 发布日期 |
|---|------|------|----------|
| 1 | The Complete Guide to Film Scanning: Four Paths from Negative to Digital File | /posts/film-scanning-complete-guide-en/ | 2026-06-15 |
| 2 | 胶片扫描完全指南：从底片到数字文件的四条路径 | /posts/film-scanning-complete-guide-zh/ | 2026-06-15 |
| 3 | Advanced Film Processing: The Complete Guide to Push, Pull & Cross Processing | /posts/film-push-pull-cross-processing-guide-en/ | 2026-06-14 |
| 4 | 胶片冲洗进阶：迫冲、迫减与交叉冲洗完全指南 | /posts/film-push-pull-cross-processing-guide-zh/ | 2026-06-14 |
| 5 | The 2026 Film Stock Guide: From Color to Black & White | /posts/film-stock-guide-2026-en/ | 2026-06-13 |
| 6 | 2026 年胶片选择指南：从彩色到黑白的全面推荐 | /posts/film-stock-guide-2026-zh/ | 2026-06-13 |
| 7 | A Practical Guide to Film Street Photography | /posts/film-street-photography-guide-en/ | 2026-06-12 |
| 8 | 胶片街头摄影实战指南：从胶片选择到区域对焦 | /posts/film-street-photography-guide-zh/ | 2026-06-12 |
| 9 | QoderWake Linux 服务器部署与配置完全指南 | /posts/qoderwake-linux-deployment-guide-zh/ | 2026-06-12 |
| 10 | The Summer Film Photography Survival Guide | /posts/summer-film-photography-guide-en/ | 2026-06-12 |
| 11 | 夏日胶片摄影生存指南 | /posts/summer-film-photography-guide-zh/ | 2026-06-12 |
| 12 | When Disposable Cameras Clogged the Film Lab Queue | /posts/disposable-camera-processing-crisis-en/ | 2026-06-11 |
| 13 | 当一次性相机塞满了冲扫店的排队队列 | /posts/disposable-camera-processing-crisis-zh/ | 2026-06-11 |
| 14 | The Film Photography Revival of 2026 | /posts/film-photography-revival-2026-en/ | 2026-06-10 |
| 15 | 2026 年胶片复兴：当年轻人重新拥抱模拟摄影 | /posts/film-photography-revival-2026-zh/ | 2026-06-10 |
| 16 | Live Photos - Bring Your Photos to Life | /posts/live-photos-introduction-en/ | 2026-06-03 |
| 17 | 实况照片 - 让你的照片动起来 | /posts/live-photos-introduction-zh/ | 2026-06-03 |
| 18 | 一次性相机与被误读的胶片感 | /posts/disposable-cameras-and-the-film-look/ | 2026-05-27 |
| 19 | Disposable Cameras and the Misunderstood Film Look | /posts/disposable-cameras-and-the-film-look-en/ | 2026-05-27 |
| 20 | 为什么胶片依然重要 | /posts/why-film-still-matters/ | 2026-05-27 |
| 21 | Why Film Still Matters in 2026 | /posts/why-film-still-matters-en/ | 2026-05-27 |

## 3. 文章数量一致性

| 来源 | 数量 | 说明 |
|------|------|------|
| 源文件 (src/content/posts/) | 22 个文件 | 含 1 个 draft |
| Draft 文章 | 1 个 | `home-film-developing-guide-zh.mdx` (draft: true) |
| 已发布文章 | 21 篇 | 正确排除 draft |
| RSS Item | 21 个 | 与已发布文章数量一致 |
| 构建页面 | 21 个文章页 | 10 en + 11 zh |

**结论**: RSS item 数量与线上文章数量完全一致。

## 4. 线上 vs 本地对比

| 对比项 | 线上版本 | 本地构建版本 | 差异 |
|--------|----------|-------------|------|
| Item 数量 | 21 | 21 | 一致 |
| Item 内容 | - | - | 完全一致 |
| Item 排序 | 按日期降序 | 按日期降序 | 一致 |
| title | Openfilm | Openfilm | 一致 |
| link | https://openfilm.cc/ | https://openfilm.cc/ | 一致 |
| description | 一致 | 一致 | 一致 |
| lastBuildDate | **缺失** | `Mon, 15 Jun 2026 00:00:00 GMT` | **不一致** |

**唯一差异**: 线上 RSS 缺少 `<lastBuildDate>` 字段。本地代码 (`src/pages/rss.xml.ts:13`) 已通过 `customData` 正确生成该字段，说明线上版本是从旧代码部署的，需要重新部署以同步。

## 5. 链接可访问性验证

全部 21 个链接均返回 **HTTP 200**，可正常访问。

| 链接 | 状态码 |
|------|--------|
| https://openfilm.cc/posts/film-scanning-complete-guide-en/ | 200 |
| https://openfilm.cc/posts/film-scanning-complete-guide-zh/ | 200 |
| https://openfilm.cc/posts/film-push-pull-cross-processing-guide-en/ | 200 |
| https://openfilm.cc/posts/film-push-pull-cross-processing-guide-zh/ | 200 |
| https://openfilm.cc/posts/film-stock-guide-2026-en/ | 200 |
| https://openfilm.cc/posts/film-stock-guide-2026-zh/ | 200 |
| https://openfilm.cc/posts/film-street-photography-guide-en/ | 200 |
| https://openfilm.cc/posts/film-street-photography-guide-zh/ | 200 |
| https://openfilm.cc/posts/qoderwake-linux-deployment-guide-zh/ | 200 |
| https://openfilm.cc/posts/summer-film-photography-guide-en/ | 200 |
| https://openfilm.cc/posts/summer-film-photography-guide-zh/ | 200 |
| https://openfilm.cc/posts/disposable-camera-processing-crisis-en/ | 200 |
| https://openfilm.cc/posts/disposable-camera-processing-crisis-zh/ | 200 |
| https://openfilm.cc/posts/film-photography-revival-2026-en/ | 200 |
| https://openfilm.cc/posts/film-photography-revival-2026-zh/ | 200 |
| https://openfilm.cc/posts/live-photos-introduction-en/ | 200 |
| https://openfilm.cc/posts/live-photos-introduction-zh/ | 200 |
| https://openfilm.cc/posts/disposable-cameras-and-the-film-look/ | 200 |
| https://openfilm.cc/posts/disposable-cameras-and-the-film-look-en/ | 200 |
| https://openfilm.cc/posts/why-film-still-matters/ | 200 |
| https://openfilm.cc/posts/why-film-still-matters-en/ | 200 |

**链接格式**: 全部使用完整 URL（`https://openfilm.cc/posts/...`），符合 RSS 规范。

## 6. 总结

### 通过项
- XML 格式正确，符合 RSS 2.0 规范
- Channel 基础字段完整（title, link, description）
- 21 个 item 与 21 篇已发布文章完全对应
- Draft 文章正确排除
- 所有 item 包含完整字段（title, link, guid, description, pubDate）
- 全部 21 个链接可访问（HTTP 200）
- 链接格式均为完整 URL
- 本地构建输出与线上 item 内容完全一致

### 问题项
- **线上 RSS 缺少 `lastBuildDate`** — 本地代码已修复，需重新部署

### 修复建议

1. **重新部署以同步 `lastBuildDate`**  
   本地 `src/pages/rss.xml.ts` 第 13 行已通过 `customData` 正确生成 `<lastBuildDate>`，但线上版本尚未更新。执行 `git push` 触发 Cloudflare 部署即可修复。

2. **Draft 文章管理**  
   `home-film-developing-guide-zh.mdx` 当前为 draft 状态。发布时只需将 frontmatter 中 `draft: true` 改为 `draft: false`，RSS 会自动包含该文章。

3. **可选优化: 添加 `<atom:link>` 自引用**  
   可在 `customData` 中添加 `<atom:link href="https://openfilm.cc/rss.xml" rel="self" type="application/rss+xml"/>` 以符合 RSS Best Practices。
