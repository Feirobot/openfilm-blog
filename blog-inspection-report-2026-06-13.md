# Openfilm Blog 内容巡检报告

**巡检日期**: 2026-06-13  
**巡检范围**: `/src/content/posts/` 全部 18 篇文章  
**站点地址**: https://openfilm.cc

---

## 一、链接检查

### 1.1 检查概况

| 指标 | 数量 |
|------|------|
| 扫描文章数 | 18 |
| 提取外部链接（去重） | 37 |
| 正常 (200) | 30 |
| 被反爬虫拦截 (403) | 7 |
| 死链 (4xx/5xx) | 0 |
| 重定向链接 | 2 |

### 1.2 死链清单

**无确认死链。** 所有 37 个外部链接均返回 200 或 403。

### 1.3 反爬虫拦截链接 (403)

以下链接返回 403，经浏览器 User-Agent 复测仍为 403，判断为网站反爬虫/Cloudflare 保护，**非死链**，但建议定期人工复核：

| URL | 所在文章 |
|-----|---------|
| `https://www.diyphotography.net/why-gen-zs-disposable-camera-trend-is-slowing-film-processing-times/` | disposable-camera-processing-crisis-en/zh |
| `https://www.ilfordphoto.com/choosing-your-first-ilford-film/` | film-stock-guide-2026-en/zh |
| `https://www.keh.com/expert-advice/camera-gear/buying-guides/what-film-stocks-sell-the-most-the-keh-tilt-shift-report/` | film-stock-guide-2026-en/zh |
| `https://www.lomography.com/magazine/159354-how-to-process-c41-at-home` | home-film-developing-guide-zh |
| `https://www.lomography.com/magazine/350418-10-tips-for-better-street-photography-on-film` | film-street-photography-guide-en/zh |
| `https://www.npmjs.com/package/live-photo-component` | live-photos-introduction-en/zh |
| `https://www.uniquephoto.com/photoinsider/beginner-recommendations-film-cameras-for-street-photography` | film-street-photography-guide-en/zh |

### 1.4 重定向链接

| 原始 URL | 重定向目标 | 所在文章 |
|----------|-----------|---------|
| `https://unpkg.com/live-photo-component/dist/live-photo.umd.js` | `https://unpkg.com/live-photo-component@1.0.0/dist/live-photo.umd.js` | live-photos-introduction-en/zh |
| `https://unpkg.com/live-photo-component/dist/styles.css` | `https://unpkg.com/live-photo-component@1.0.0/dist/styles.css` | live-photos-introduction-en/zh |

> **建议**: unpkg 重定向到版本化 URL 是正常行为，但建议锁定版本号以避免意外 breaking change：  
> `https://unpkg.com/live-photo-component@1.0.0/dist/live-photo.umd.js`

---

## 二、资源检查

### 2.1 图片资源

| URL | 状态 | 所在文章 |
|-----|------|---------|
| `https://eatbbqcici.oss-cn-shenzhen.aliyuncs.com/images/eatbbq/2025/09/MVIMG_20241231_161000-scaled.jpg` | 200 OK | live-photos-introduction-en/zh |
| `https://eatbbqcici.oss-cn-shenzhen.aliyuncs.com/images/eatbbq/2025/09/MVIMG_20250405_132341-scaled.jpg` | 200 OK | live-photos-introduction-en/zh |
| `https://eatbbqcici.oss-cn-shenzhen.aliyuncs.com/images/eatbbq/2026/05/DSCF2490.00_00_05_34.Still001.jpg` | 200 OK | live-photos-introduction-en/zh |

### 2.2 视频资源

| URL | 状态 | 所在文章 |
|-----|------|---------|
| `https://eatbbqcici.oss-cn-shenzhen.aliyuncs.com/images/eatbbq/2025/09/VID_20250912_234046.mp4` | 200 OK | live-photos-introduction-en/zh |
| `https://eatbbqcici.oss-cn-shenzhen.aliyuncs.com/images/eatbbq/2025/09/VID_20250912_234608.mp4` | 200 OK | live-photos-introduction-en/zh |
| `https://eatbbqcici.oss-cn-shenzhen.aliyuncs.com/images/eatbbq/2026/05/4月28日.mp4` | 200 OK | live-photos-introduction-en/zh |

### 2.3 资源检查结论

**全部 6 个资源链接（3 图片 + 3 视频）均可正常访问，无失效资源。**

> 所有资源均托管在阿里云 OSS（eatbbqcici.oss-cn-shenzhen.aliyuncs.com），建议关注 OSS 存储费用与 Bucket 权限配置。

---

## 三、SEO 健康检查

### 3.1 Frontmatter 完整性

| 文章 | title | description | pubDate | updatedDate | draft | lang |
|------|-------|-------------|---------|-------------|-------|------|
| disposable-camera-processing-crisis-en | OK | OK | OK | OK | false | - |
| disposable-camera-processing-crisis-zh | OK | OK | OK | OK | false | - |
| disposable-cameras-and-the-film-look-en | OK | OK | OK | **缺失** | false | en |
| disposable-cameras-and-the-film-look.md | OK | OK | OK | **缺失** | - | zh |
| film-photography-revival-2026-en | OK | OK | OK | OK | false | - |
| film-photography-revival-2026-zh | OK | OK | OK | OK | false | - |
| film-stock-guide-2026-en | OK | OK | OK | OK | false | - |
| film-stock-guide-2026-zh | OK | OK | OK | OK | false | - |
| film-street-photography-guide-en | OK | OK | OK | OK | false | - |
| film-street-photography-guide-zh | OK | OK | OK | OK | false | - |
| home-film-developing-guide-zh | OK | OK | OK | OK | **true** | - |
| live-photos-introduction-en | OK | OK | OK | **缺失** | false | en |
| live-photos-introduction-zh | OK | OK | OK | **缺失** | false | zh |
| qoderwake-linux-deployment-guide-zh | OK | OK | OK | OK | false | zh |
| summer-film-photography-guide-en | OK | OK | OK | OK | false | - |
| summer-film-photography-guide-zh | OK | OK | OK | OK | false | - |
| why-film-still-matters-en | OK | OK | OK | **缺失** | false | en |
| why-film-still-matters.md | OK | OK | OK | **缺失** | - | zh |

### 3.2 SEO 问题清单

| 优先级 | 问题 | 影响文章 | 建议 |
|--------|------|---------|------|
| **中** | `updatedDate` 字段缺失 | 6 篇早期文章 | 补充 `updatedDate`，有利于搜索引擎判断内容新鲜度 |
| **低** | `lang` 字段不一致 | 部分文章有 `lang`，部分缺失 | 建议统一为所有文章添加 `lang` 字段 |
| **信息** | `home-film-developing-guide-zh` 仍为 draft | 1 篇 | 确认是否计划发布，长期 draft 会影响内容覆盖度 |

### 3.3 RSS Feed 检查

| 检查项 | 结果 |
|--------|------|
| RSS 文件存在 | OK (`/dist/rss.xml`) |
| XML 格式正确 | OK |
| RSS 版本 | 2.0 |
| 站点标题 | "Openfilm" |
| 站点描述 | OK |
| 站点链接 | `https://openfilm.cc/` |
| lastBuildDate | 2026-06-13 OK |
| 文章数量 | 17 篇（正确排除 1 篇 draft） |
| 每篇文章含 title | OK |
| 每篇文章含 link | OK |
| 每篇文章含 guid | OK |
| 每篇文章含 description | OK |
| 每篇文章含 pubDate | OK |
| 按 pubDate 倒序排列 | OK |

**RSS Feed 格式完全正确，无问题。**

---

## 四、内容新鲜度分析

### 4.1 文章发布时间分布

| 文章 | pubDate | 距今天数 | 状态 |
|------|---------|---------|------|
| film-stock-guide-2026-en/zh | 2026-06-13 | 0 天 | 最新 |
| film-street-photography-guide-en/zh | 2026-06-12 | 1 天 | 新鲜 |
| qoderwake-linux-deployment-guide-zh | 2026-06-12 | 1 天 | 新鲜 |
| summer-film-photography-guide-en/zh | 2026-06-12 | 1 天 | 新鲜 |
| disposable-camera-processing-crisis-en/zh | 2026-06-11 | 2 天 | 新鲜 |
| film-photography-revival-2026-en/zh | 2026-06-10 | 3 天 | 新鲜 |
| home-film-developing-guide-zh | 2026-06-10 | 3 天 | 新鲜 (draft) |
| live-photos-introduction-en/zh | 2026-06-03 | 10 天 | 新鲜 |
| disposable-cameras-and-the-film-look-en/zh | 2026-05-27 | 17 天 | 新鲜 |
| why-film-still-matters-en/zh | 2026-05-27 | 17 天 | 新鲜 |

### 4.2 新鲜度结论

**全部 18 篇文章均在 90 天更新周期内，无需标记过期内容。**

博客处于活跃更新期，最近两周发布了大量新内容。

---

## 五、修复建议优先级排序

### P0 - 紧急（无需处理）

- 无死链、无失效资源

### P1 - 建议尽快处理

| # | 建议 | 影响范围 | 工作量 |
|---|------|---------|--------|
| 1 | 为 6 篇早期文章补充 `updatedDate` 字段 | SEO 信号完整性 | 低（每篇加一行） |
| 2 | unpkg CDN 链接锁定版本号 | 避免未来 breaking change | 低（2 处 URL 修改） |

### P2 - 建议计划处理

| # | 建议 | 影响范围 | 工作量 |
|---|------|---------|--------|
| 3 | 统一所有文章的 `lang` 字段 | 国际化/SEO | 中 |
| 4 | 确认 `home-film-developing-guide-zh` 发布计划 | 内容覆盖度 | 低 |
| 5 | 人工复核 7 个 403 链接的实际可访问性 | 参考链接有效性 | 中（需浏览器逐一验证） |

### P3 - 持续关注

| # | 建议 | 说明 |
|---|------|------|
| 6 | 定期（每月）复跑链接检查 | 外部链接随时可能失效 |
| 7 | 关注阿里云 OSS 资源可用性 | 所有图片/视频依赖单一 OSS Bucket |

---

## 六、巡检总结

| 维度 | 状态 | 说明 |
|------|------|------|
| 链接健康度 | 良好 | 0 死链，7 个被反爬虫拦截（非死链），2 个重定向 |
| 资源可用性 | 良好 | 全部 6 个图片/视频资源正常 |
| SEO 合规性 | 良好 | 所有文章 title/description 完整，RSS 格式正确 |
| 内容新鲜度 | 优秀 | 全部文章在 17 天内发布，无过期内容 |

**总体评价**: 博客内容状态健康，处于活跃更新期。主要改进空间在于 Frontmatter 字段完整性（`updatedDate`、`lang`）和 CDN 链接版本号锁定。
