# Openfilm Blog 内容巡检报告

**巡检时间**: 2026-06-16  
**巡检范围**: `/src/content/posts/` 全部 24 篇文章  
**文章总数**: 24 篇（12 对中英双语 + 2 篇早期 .md 文章）

---

## 1. 链接检查结果

**检查链接总数**: 54 个外部 URL（排除 localhost 和模板占位符）  
**正常**: 41 个  
**异常**: 13 个

### 1.1 死链 / 不可访问链接（403 - 反爬保护）

以下链接返回 HTTP 403，经浏览器 UA 重试仍为 403。多数为 Cloudflare / 反爬保护，**页面本身可能仍然存在**，但自动化访问被拒绝：

| # | URL | 所在文章 | 风险等级 |
|---|-----|---------|---------|
| 1 | `https://rangefinderonline.com/news-features/tips-techniques/best-natural-light-for-photography/` | film-portrait-photography-guide-{en,zh} | 中 |
| 2 | `https://thedarkroom.com/pushing-and-pulling-film/` | film-push-pull-cross-processing-guide-{en,zh} | 中 |
| 3 | `https://www.diyphotography.net/why-gen-zs-disposable-camera-trend-is-slowing-film-processing-times/` | disposable-camera-processing-crisis-{en,zh} | 中 |
| 4 | `https://www.ilfordphoto.com/choosing-your-first-ilford-film/` | film-stock-guide-2026-{en,zh} | 中 |
| 5 | `https://www.keh.com/expert-advice/camera-gear/buying-guides/what-film-stocks-sell-the-most-the-keh-tilt-shift-report/` | film-stock-guide-2026-{en,zh} | 中 |
| 6 | `https://www.lomography.com/magazine/159354-how-to-process-c41-at-home` | home-film-developing-guide-zh | **高** |
| 7 | `https://www.lomography.com/magazine/197248-pushing-pulling-cross-processing-what` | film-push-pull-cross-processing-guide-{en,zh} | **高** |
| 8 | `https://www.lomography.com/magazine/350418-10-tips-for-better-street-photography-on-film` | film-street-photography-guide-{en,zh} | **高** |
| 9 | `https://www.npmjs.com/package/live-photo-component` | live-photos-introduction-{en,zh} | 低 |
| 10 | `https://www.uniquephoto.com/photoinsider/beginner-recommendations-film-cameras-for-street-photography` | film-street-photography-guide-{en,zh} | 中 |

### 1.2 超时链接（网络不可达）

| # | URL | 所在文章 | 风险等级 |
|---|-----|---------|---------|
| 1 | `https://www.reddit.com/r/AnalogCommunity/comments/11sppa4/...` | film-scanning-complete-guide-{en,zh} | 低（Reddit 讨论帖） |
| 2 | `https://www.reddit.com/r/AnalogCommunity/comments/1svfblh/...` | film-scanning-complete-guide-{en,zh} | 低（Reddit 讨论帖） |
| 3 | `https://www.reddit.com/r/photography/comments/5z8zb2/...` | film-portrait-photography-guide-{en,zh} | 低（Reddit 讨论帖） |

> **说明**: Reddit 链接从当前服务器环境（中国大陆）无法访问，属于网络限制而非链接失效。在面向海外读者的浏览器中大概率正常。

### 1.3 重定向链接

| # | URL | 行为 | 所在文章 | 风险等级 |
|---|-----|------|---------|---------|
| 1 | `https://pellica.app/blog/film-photography-revival-2026/` | 正常 200（但域名 pellica.app 与本站关联） | 6 篇文章引用 | 低 |

### 1.4 Lomography 地理重定向（特别说明）

Lomography 的 3 条链接返回 302 重定向到 `lomography.cn`（中国区域名），原文内容可能无法访问。**建议**: 手动在浏览器中验证这些链接是否仍指向原始英文内容。

---

## 2. 资源检查结果

### 2.1 图片资源

| URL | 状态 | 所在文章 |
|-----|------|---------|
| `eatbbqcici.oss-cn-shenzhen.aliyuncs.com/.../MVIMG_20241231_161000-scaled.jpg` | 200 OK | live-photos-introduction-{en,zh} |
| `eatbbqcici.oss-cn-shenzhen.aliyuncs.com/.../MVIMG_20250405_132341-scaled.jpg` | 200 OK | live-photos-introduction-{en,zh} |
| `eatbbqcici.oss-cn-shenzhen.aliyuncs.com/.../DSCF2490.00_00_05_34.Still001.jpg` | 200 OK | live-photos-introduction-{en,zh} |

**结论**: 全部图片资源可正常访问。

### 2.2 视频资源

| URL | 状态 | 所在文章 |
|-----|------|---------|
| `eatbbqcici.oss-cn-shenzhen.aliyuncs.com/.../VID_20250912_234046.mp4` | 200 OK | live-photos-introduction-{en,zh} |
| `eatbbqcici.oss-cn-shenzhen.aliyuncs.com/.../VID_20250912_234608.mp4` | 200 OK | live-photos-introduction-{en,zh} |
| `eatbbqcici.oss-cn-shenzhen.aliyuncs.com/.../4月28日.mp4` | 200 OK | live-photos-introduction-{en,zh} |

**结论**: 全部视频资源可正常访问。

### 2.3 CDN / JS 资源

| URL | 状态 | 所在文章 |
|-----|------|---------|
| `unpkg.com/live-photo-component/dist/live-photo.umd.js` | 200 OK | live-photos-introduction-{en,zh} |
| `unpkg.com/live-photo-component/dist/styles.css` | 200 OK | live-photos-introduction-{en,zh} |

**结论**: 全部 CDN 资源正常。

---

## 3. SEO 健康检查

### 3.1 Frontmatter 完整性

| 文章 | title | description | pubDate | updatedDate | draft | tags | 状态 |
|------|-------|-------------|---------|-------------|-------|------|------|
| disposable-cameras-and-the-film-look.md | OK | OK | OK | -- | -- | OK | 缺少 updatedDate |
| why-film-still-matters.md | OK | OK | OK | -- | -- | OK | 缺少 updatedDate |
| disposable-camera-processing-crisis-{en,zh} | OK | OK | OK | OK | false | OK | 完整 |
| film-photography-revival-2026-{en,zh} | OK | OK | OK | OK | false | OK | 完整 |
| film-portrait-photography-guide-{en,zh} | OK | OK | OK | OK | false | OK | 完整 |
| film-push-pull-cross-processing-guide-{en,zh} | OK | OK | OK | OK | false | OK | 完整 |
| film-scanning-complete-guide-{en,zh} | OK | OK | OK | OK | false | OK | 完整 |
| film-stock-guide-2026-{en,zh} | OK | OK | OK | OK | false | OK | 完整 |
| film-street-photography-guide-{en,zh} | OK | OK | OK | OK | false | OK | 完整 |
| home-film-developing-guide-zh | OK | OK | OK | OK | **true** | OK | 草稿状态 |
| live-photos-introduction-{en,zh} | OK | OK | OK | -- | false | OK | 缺少 updatedDate |
| qoderwake-linux-deployment-guide-zh | OK | OK | OK | OK | false | OK | 完整 |
| summer-film-photography-guide-{en,zh} | OK | OK | OK | OK | false | OK | 完整 |
| why-film-still-matters-en.mdx | OK | OK | OK | -- | false | OK | 缺少 updatedDate |

**SEO 问题汇总**:
- 4 篇文章缺少 `updatedDate` 字段（早期 .md 和 live-photos 文章）
- 1 篇文章处于 `draft: true` 状态（home-film-developing-guide-zh）
- 所有文章的 `title` 和 `description` 均完整

### 3.2 RSS Feed 验证

| 检查项 | 结果 |
|--------|------|
| XML 格式 | 有效 |
| RSS 版本 | 2.0 |
| Channel title | "Openfilm" |
| Channel description | 有 |
| Channel link | `https://openfilm.cc/` |
| lastBuildDate | `Tue, 16 Jun 2026 00:00:00 GMT` |
| Item 总数 | 23 篇 |
| 每个 item 含 title | 23/23 |
| 每个 item 含 link | 23/23 |
| 每个 item 含 guid | 23/23 |
| 每个 item 含 pubDate | 23/23 |
| 每个 item 含 description | 23/23 |
| 草稿文章排除 | 正确（home-film-developing-guide-zh 未出现） |

**结论**: RSS Feed 格式完全正确，草稿文章已正确排除。

---

## 4. 内容新鲜度分析

**巡检日期**: 2026-06-16  
**过期阈值**: 90 天（2026-03-18 之前）

| 文章 | 最后修改 | 距今天数 | 状态 |
|------|---------|---------|------|
| film-portrait-photography-guide-{en,zh} | 2026-06-16 | 0 | 最新 |
| film-scanning-complete-guide-{en,zh} | 2026-06-15 | 1 | 最新 |
| film-push-pull-cross-processing-guide-{en,zh} | 2026-06-14 | 2 | 最新 |
| film-stock-guide-2026-{en,zh} | 2026-06-13 | 3 | 最新 |
| film-street-photography-guide-{en,zh} | 2026-06-12 | 4 | 最新 |
| summer-film-photography-guide-{en,zh} | 2026-06-12 | 4 | 最新 |
| qoderwake-linux-deployment-guide-zh | 2026-06-12 | 4 | 最新 |
| disposable-camera-processing-crisis-{en,zh} | 2026-06-11 | 5 | 最新 |
| film-photography-revival-2026-{en,zh} | 2026-06-11 | 5 | 最新 |
| home-film-developing-guide-zh | 2026-06-10 | 6 | 最新（草稿） |
| live-photos-introduction-{en,zh} | 2026-06-10 | 6 | 最新 |
| disposable-cameras-and-the-film-look-{en,.md} | 2026-06-10 | 6 | 最新 |
| why-film-still-matters-{en,.md} | 2026-06-10 | 6 | 最新 |

**结论**: 全部文章均在 90 天以内更新，无过期内容。博客处于活跃更新状态（最近一周密集更新）。

---

## 5. 修复建议（按优先级排序）

### P0 - 建议立即处理

| # | 问题 | 影响范围 | 建议 |
|---|------|---------|------|
| 1 | Lomography 3 条链接 302 重定向到 .cn | 3 篇文章 | 手动验证链接内容是否可达；如不可达，替换为 Web Archive 存档链接或其他等效来源 |

### P1 - 建议本周处理

| # | 问题 | 影响范围 | 建议 |
|---|------|---------|------|
| 2 | 7 个外部链接返回 403（反爬保护） | 6 篇文章 | 在浏览器中逐一验证是否可达；如确认失效，替换为等效来源或添加 Web Archive 备份链接 |
| 3 | home-film-developing-guide-zh 仍为草稿 | 1 篇文章 | 确认内容是否已完善，决定发布或继续编辑 |

### P2 - 建议近期优化

| # | 问题 | 影响范围 | 建议 |
|---|------|---------|------|
| 4 | 4 篇文章缺少 `updatedDate` 字段 | disposable-cameras-and-the-film-look, why-film-still-matters, live-photos-introduction | 补充 `updatedDate` 以与近期文章保持一致的 frontmatter 规范 |
| 5 | 3 个 Reddit 链接从国内不可访问 | 2 篇文章 | 如目标读者包含国内用户，考虑添加国内可访问的替代讨论链接或摘要说明 |

### P3 - 可选优化

| # | 问题 | 影响范围 | 建议 |
|---|------|---------|------|
| 6 | 早期 .md 文章格式不统一 | 2 篇 .md 文章 | 考虑将 `disposable-cameras-and-the-film-look.md` 和 `why-film-still-matters.md` 升级为 .mdx 格式，统一 frontmatter 字段 |

---

## 6. 巡检总结

| 维度 | 状态 | 评分 |
|------|------|------|
| 链接可用性 | 41/54 正常，13 异常（10 个 403 + 3 个超时） | B |
| 资源可用性 | 全部正常（图片 3/3，视频 3/3，CDN 2/2） | A |
| SEO 完整性 | title/description 100% 完整，RSS 格式正确 | A- |
| 内容新鲜度 | 全部文章在 6 天内更新 | A+ |
| Frontmatter 规范 | 4 篇缺 updatedDate，1 篇草稿 | B+ |

**总体评估**: 博客处于活跃更新期，内容新鲜度极佳。主要风险点在于部分外部参考链接可能因反爬保护或地理限制无法访问，建议优先验证 Lomography 相关链接。
