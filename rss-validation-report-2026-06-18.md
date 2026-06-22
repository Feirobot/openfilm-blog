# RSS 订阅源验证报告

**验证时间**: 2026-06-18  
**验证目标**: https://openfilm.cc/rss.xml  
**本地项目**: /root/AIwork/openfilm-blog

---

## 1. RSS 格式验证

| 检查项 | 结果 | 说明 |
|--------|------|------|
| XML 声明 | PASS | `<?xml version="1.0" encoding="UTF-8"?>` |
| RSS 版本 | PASS | `version="2.0"` |
| channel > title | PASS | `Openfilm` |
| channel > link | PASS | `https://openfilm.cc/` |
| channel > description | PASS | `Notes, essays, and experiments from Openfilm.` |
| channel > lastBuildDate | **FAIL (线上)** | 线上版本**缺少** `lastBuildDate` 字段 |
| item > title | PASS | 所有 27 个 item 均包含 title |
| item > link | PASS | 所有 27 个 item 均包含 link |
| item > guid | PASS | 所有 27 个 item 均包含 guid (isPermaLink="true") |
| item > description | PASS | 所有 27 个 item 均包含 description |
| item > pubDate | PASS | 所有 27 个 item 均包含 pubDate |

## 2. RSS Item 完整列表 (27 条)

| # | 标题 | 链接 | 发布日期 |
|---|------|------|----------|
| 1 | Film Multiple Exposure Creative Guide: Letting Images Converse Within a Single Frame | .../film-multiple-exposure-creative-guide-en/ | 2026-06-18 |
| 2 | 胶片多重曝光创意指南：让影像在同一个画框中对话 | .../film-multiple-exposure-creative-guide-zh/ | 2026-06-18 |
| 3 | The Complete Guide to Expired Film Photography: Turning 'Spoiled' into Style | .../expired-film-photography-guide-en/ | 2026-06-17 |
| 4 | 过期胶片摄影完全指南：把「变质」变成风格 | .../expired-film-photography-guide-zh/ | 2026-06-17 |
| 5 | The Complete Guide to Film Portrait Photography: From Film Selection to Light Shaping | .../film-portrait-photography-guide-en/ | 2026-06-16 |
| 6 | 胶片人像摄影完全指南：从胶片选择到光影塑造 | .../film-portrait-photography-guide-zh/ | 2026-06-16 |
| 7 | The Complete Guide to Film Scanning: Four Paths from Negative to Digital File | .../film-scanning-complete-guide-en/ | 2026-06-15 |
| 8 | 胶片扫描完全指南：从底片到数字文件的四条路径 | .../film-scanning-complete-guide-zh/ | 2026-06-15 |
| 9 | Advanced Film Processing: The Complete Guide to Push, Pull & Cross Processing | .../film-push-pull-cross-processing-guide-en/ | 2026-06-14 |
| 10 | 胶片冲洗进阶：迫冲、迫减与交叉冲洗完全指南 | .../film-push-pull-cross-processing-guide-zh/ | 2026-06-14 |
| 11 | The 2026 Film Stock Guide: From Color to Black & White | .../film-stock-guide-2026-en/ | 2026-06-13 |
| 12 | 2026 年胶片选择指南：从彩色到黑白的全面推荐 | .../film-stock-guide-2026-zh/ | 2026-06-13 |
| 13 | A Practical Guide to Film Street Photography: From Film Selection to Zone Focusing | .../film-street-photography-guide-en/ | 2026-06-12 |
| 14 | 胶片街头摄影实战指南：从胶片选择到区域对焦 | .../film-street-photography-guide-zh/ | 2026-06-12 |
| 15 | QoderWake Linux 服务器部署与配置完全指南 | .../qoderwake-linux-deployment-guide-zh/ | 2026-06-12 |
| 16 | The Summer Film Photography Survival Guide: Storing, Shooting, and Processing in Heat and Humidity | .../summer-film-photography-guide-en/ | 2026-06-12 |
| 17 | 夏日胶片摄影生存指南：高温高湿下的胶片保存、拍摄与冲洗 | .../summer-film-photography-guide-zh/ | 2026-06-12 |
| 18 | When Disposable Cameras Clogged the Film Lab Queue | .../disposable-camera-processing-crisis-en/ | 2026-06-11 |
| 19 | 当一次性相机塞满了冲扫店的排队队列 | .../disposable-camera-processing-crisis-zh/ | 2026-06-11 |
| 20 | The Film Photography Revival of 2026: Why Young People Are Embracing Analog Photography Again | .../film-photography-revival-2026-en/ | 2026-06-10 |
| 21 | 2026 年胶片复兴：当年轻人重新拥抱模拟摄影 | .../film-photography-revival-2026-zh/ | 2026-06-10 |
| 22 | Live Photos - Bring Your Photos to Life | .../live-photos-introduction-en/ | 2026-06-03 |
| 23 | 实况照片 - 让你的照片动起来 | .../live-photos-introduction-zh/ | 2026-06-03 |
| 24 | 一次性相机与被误读的胶片感 | .../disposable-cameras-and-the-film-look/ | 2026-05-27 |
| 25 | Disposable Cameras and the Misunderstood Film Look | .../disposable-cameras-and-the-film-look-en/ | 2026-05-27 |
| 26 | 为什么胶片依然重要 | .../why-film-still-matters/ | 2026-05-27 |
| 27 | Why Film Still Matters in 2026 | .../why-film-still-matters-en/ | 2026-05-27 |

## 3. 文章数量一致性

| 来源 | 数量 |
|------|------|
| RSS item 数量 | 27 |
| 构建生成页面数 (build output) | 27 (13 en + 14 zh) |
| **一致性** | **PASS** |

## 4. 线上 vs 本地对比

| 对比项 | 线上版本 | 本地构建版本 | 差异 |
|--------|----------|-------------|------|
| XML 声明 | 有 | 有 | 无差异 |
| title | Openfilm | Openfilm | 无差异 |
| description | Notes, essays... | Notes, essays... | 无差异 |
| link | https://openfilm.cc/ | https://openfilm.cc/ | 无差异 |
| lastBuildDate | **缺失** | Thu, 18 Jun 2026 00:00:00 GMT | **有差异** |
| item 数量 | 27 | 27 | 无差异 |
| item 内容 | 完全一致 | 完全一致 | 无差异 |
| item 排序 | 按日期降序 | 按日期降序 | 无差异 |

**唯一差异**: 线上版本缺少 `<lastBuildDate>` 字段，本地构建版本包含该字段。说明线上部署的是较早版本的构建产物，本地代码已修复此问题但尚未部署。

## 5. 链接可访问性验证

| # | 链接 | HTTP 状态 | 结果 |
|---|------|-----------|------|
| 1 | https://openfilm.cc/posts/film-multiple-exposure-creative-guide-en/ | 200 | PASS |
| 2 | https://openfilm.cc/posts/film-multiple-exposure-creative-guide-zh/ | 200 | PASS |
| 3 | https://openfilm.cc/posts/expired-film-photography-guide-en/ | 200 | PASS |
| 4 | https://openfilm.cc/posts/expired-film-photography-guide-zh/ | 200 | PASS |
| 5 | https://openfilm.cc/posts/film-portrait-photography-guide-en/ | 200 | PASS |
| 6 | https://openfilm.cc/posts/film-portrait-photography-guide-zh/ | 200 | PASS |
| 7 | https://openfilm.cc/posts/film-scanning-complete-guide-en/ | 200 | PASS |
| 8 | https://openfilm.cc/posts/film-scanning-complete-guide-zh/ | 200 | PASS |
| 9 | https://openfilm.cc/posts/film-push-pull-cross-processing-guide-en/ | 200 | PASS |
| 10 | https://openfilm.cc/posts/film-push-pull-cross-processing-guide-zh/ | 200 | PASS |
| 11 | https://openfilm.cc/posts/film-stock-guide-2026-en/ | 200 | PASS |
| 12 | https://openfilm.cc/posts/film-stock-guide-2026-zh/ | 200 | PASS |
| 13 | https://openfilm.cc/posts/film-street-photography-guide-en/ | 200 | PASS |
| 14 | https://openfilm.cc/posts/film-street-photography-guide-zh/ | 200 | PASS |
| 15 | https://openfilm.cc/posts/qoderwake-linux-deployment-guide-zh/ | 200 | PASS |
| 16 | https://openfilm.cc/posts/summer-film-photography-guide-en/ | 200 | PASS |
| 17 | https://openfilm.cc/posts/summer-film-photography-guide-zh/ | 200 | PASS |
| 18 | https://openfilm.cc/posts/disposable-camera-processing-crisis-en/ | 200 | PASS |
| 19 | https://openfilm.cc/posts/disposable-camera-processing-crisis-zh/ | 200 | PASS |
| 20 | https://openfilm.cc/posts/film-photography-revival-2026-en/ | 200 | PASS |
| 21 | https://openfilm.cc/posts/film-photography-revival-2026-zh/ | 200 | PASS |
| 22 | https://openfilm.cc/posts/live-photos-introduction-en/ | 200 | PASS |
| 23 | https://openfilm.cc/posts/live-photos-introduction-zh/ | 200 | PASS |
| 24 | https://openfilm.cc/posts/disposable-cameras-and-the-film-look/ | 200 | PASS |
| 25 | https://openfilm.cc/posts/disposable-cameras-and-the-film-look-en/ | 200 | PASS |
| 26 | https://openfilm.cc/posts/why-film-still-matters/ | 200 | PASS |
| 27 | https://openfilm.cc/posts/why-film-still-matters-en/ | 200 | PASS |

**链接格式检查**: 所有 27 个链接均为完整 URL，以 `https://openfilm.cc/` 开头。PASS

**可访问性**: 27/27 链接返回 HTTP 200。PASS

## 6. 总结

### 整体评估: 良好 (B+)

| 维度 | 状态 |
|------|------|
| XML 格式有效性 | PASS |
| RSS 2.0 规范字段 | PASS (除 lastBuildDate) |
| Item 与文章数量一致性 | PASS (27 = 27) |
| 线上/本地内容一致性 | PASS (仅 lastBuildDate 差异) |
| 链接完整性 | PASS (27/27 可访问) |
| 链接格式 | PASS (全部完整 URL) |

### 发现的问题

1. **[中] 线上 RSS 缺少 lastBuildDate**
   - 线上版本未包含 `<lastBuildDate>` 字段
   - 本地构建版本已修复此问题
   - 原因：线上部署的构建产物来自较早版本，需要重新部署
   - 影响：RSS 阅读器无法判断 feed 最后更新时间，可能影响订阅者获取最新内容

### 修复建议

1. **重新部署** — 将本地最新构建产物部署到 Cloudflare，使线上 RSS 包含 `lastBuildDate` 字段
2. **部署后验证** — 部署完成后再次访问 `https://openfilm.cc/rss.xml` 确认 `lastBuildDate` 已出现
3. **无需其他修复** — RSS 内容、链接、格式均正常
