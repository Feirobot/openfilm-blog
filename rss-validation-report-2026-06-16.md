# RSS 订阅源验证报告

**验证时间**: 2026-06-16 16:01  
**验证目标**: https://openfilm.cc/rss.xml  
**本地项目**: /root/AIwork/openfilm-blog

---

## 1. XML 格式验证

| 检查项 | 结果 |
|--------|------|
| XML 解析 | **通过** |
| RSS 版本 | 2.0 |
| 编码 | UTF-8 |

### Channel 级别字段

| 字段 | 线上 | 本地 | 状态 |
|------|------|------|------|
| title | Openfilm | Openfilm | 一致 |
| link | https://openfilm.cc/ | https://openfilm.cc/ | 一致 |
| description | Notes, essays, and experiments from Openfilm. | Notes, essays, and experiments from Openfilm. | 一致 |
| lastBuildDate | **(缺失)** | Tue, 16 Jun 2026 00:00:00 GMT | **差异** |

---

## 2. RSS Items 清单 (共 23 条)

| # | 标题 | 链接 | 发布日期 |
|---|------|------|----------|
| 1 | The Complete Guide to Film Portrait Photography | .../film-portrait-photography-guide-en/ | 2026-06-16 |
| 2 | 胶片人像摄影完全指南 | .../film-portrait-photography-guide-zh/ | 2026-06-16 |
| 3 | The Complete Guide to Film Scanning | .../film-scanning-complete-guide-en/ | 2026-06-15 |
| 4 | 胶片扫描完全指南 | .../film-scanning-complete-guide-zh/ | 2026-06-15 |
| 5 | Advanced Film Processing: Push, Pull & Cross | .../film-push-pull-cross-processing-guide-en/ | 2026-06-14 |
| 6 | 胶片冲洗进阶：迫冲、迫减与交叉冲洗 | .../film-push-pull-cross-processing-guide-zh/ | 2026-06-14 |
| 7 | The 2026 Film Stock Guide | .../film-stock-guide-2026-en/ | 2026-06-13 |
| 8 | 2026 年胶片选择指南 | .../film-stock-guide-2026-zh/ | 2026-06-13 |
| 9 | A Practical Guide to Film Street Photography | .../film-street-photography-guide-en/ | 2026-06-12 |
| 10 | 胶片街头摄影实战指南 | .../film-street-photography-guide-zh/ | 2026-06-12 |
| 11 | QoderWake Linux 服务器部署与配置完全指南 | .../qoderwake-linux-deployment-guide-zh/ | 2026-06-12 |
| 12 | The Summer Film Photography Survival Guide | .../summer-film-photography-guide-en/ | 2026-06-12 |
| 13 | 夏日胶片摄影生存指南 | .../summer-film-photography-guide-zh/ | 2026-06-12 |
| 14 | When Disposable Cameras Clogged the Film Lab Queue | .../disposable-camera-processing-crisis-en/ | 2026-06-11 |
| 15 | 当一次性相机塞满了冲扫店的排队队列 | .../disposable-camera-processing-crisis-zh/ | 2026-06-11 |
| 16 | The Film Photography Revival of 2026 | .../film-photography-revival-2026-en/ | 2026-06-10 |
| 17 | 2026 年胶片复兴 | .../film-photography-revival-2026-zh/ | 2026-06-10 |
| 18 | Live Photos - Bring Your Photos to Life | .../live-photos-introduction-en/ | 2026-06-03 |
| 19 | 实况照片 - 让你的照片动起来 | .../live-photos-introduction-zh/ | 2026-06-03 |
| 20 | 一次性相机与被误读的胶片感 | .../disposable-cameras-and-the-film-look/ | 2026-05-27 |
| 21 | Disposable Cameras and the Misunderstood Film Look | .../disposable-cameras-and-the-film-look-en/ | 2026-05-27 |
| 22 | 为什么胶片依然重要 | .../why-film-still-matters/ | 2026-05-27 |
| 23 | Why Film Still Matters in 2026 | .../why-film-still-matters-en/ | 2026-05-27 |

---

## 3. 线上 vs 本地对比

| 对比项 | 结果 |
|--------|------|
| Item 数量 | 线上 23 = 本地 23 |
| Item 集合 | 完全一致，无多无少 |
| Item 内容 (title/description/pubDate/guid) | 所有 23 条完全一致 |
| Channel lastBuildDate | **线上缺失，本地有值** |

### 结论

线上 RSS 与本地构建的 RSS 在 23 个 item 层面完全一致。唯一差异是线上版本缺少 `lastBuildDate` 字段。可能原因：
- 线上部署的是稍早版本的构建产物
- CDN 缓存了旧版 rss.xml
- 部署过程中 rss.xml 被覆盖为不含 lastBuildDate 的版本

---

## 4. 链接可访问性验证

**全部 23 条链接均可访问 (HTTP 200)**

| 状态 | 数量 |
|------|------|
| 200 OK | 23 |
| 4xx/5xx 错误 | 0 |
| 连接失败 | 0 |

所有链接格式均为完整 URL（`https://openfilm.cc/posts/...`），符合 RSS 规范。

---

## 5. 文章数量一致性检查

| 来源 | 数量 |
|------|------|
| src/content/posts/ 源文件 | 24 |
| 其中 draft: true | 1 (home-film-developing-guide-zh.mdx) |
| 构建生成的 HTML 页面 | 23 |
| RSS Items | 23 |
| 线上 RSS Items | 23 |

**结论**: 源文件 24 篇，其中 1 篇标记为草稿（`draft: true`），实际发布 23 篇，与 RSS 条目数量完全一致。

---

## 6. 发现的问题与修复建议

### 问题 1: 线上 RSS 缺少 lastBuildDate (低优先级)

- **现象**: 线上 `rss.xml` 的 `<channel>` 中无 `<lastBuildDate>` 字段，本地构建版本有
- **影响**: RSS 阅读器无法判断 feed 最后更新时间，可能影响增量拉取效率
- **建议**: 重新部署最新构建产物到线上，确保 `dist/rss.xml` 覆盖线上版本

### 问题 2: 草稿文章未发布 (信息项，非问题)

- **现象**: `home-film-developing-guide-zh.mdx` 标记为 `draft: true`，未出现在 RSS 和线上页面中
- **影响**: 无（草稿不应出现在 RSS 中，行为正确）
- **建议**: 如文章已就绪，移除 `draft: true` 并重新构建发布

---

## 7. 总结

| 验证维度 | 状态 |
|----------|------|
| XML 格式 | 通过 |
| Channel 字段 | 基本通过 (线上缺 lastBuildDate) |
| Item 完整性 | 通过 (23/23) |
| 线上 vs 本地一致性 | 通过 (item 级别完全一致) |
| 链接可访问性 | 通过 (23/23 全部 200) |
| 链接格式 | 通过 (全部 https://openfilm.cc 完整 URL) |
| 文章数量一致性 | 通过 (23 篇发布文章 = 23 RSS items) |

**整体评估**: RSS 订阅源运行正常，内容完整，链接全部可用。唯一需关注的是线上版本缺少 `lastBuildDate`，建议重新部署。
