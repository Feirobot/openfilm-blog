# Openfilm Blog

**中文**：关于胶片、媒体与值得品味之物的博客 ｜ **EN**: Notes on film, media, and things worth savoring.

🌐 **Live Site**: [https://openfilm.cc](https://openfilm.cc)

- 🇨🇳 **中文版**: [https://openfilm.cc/zh/](https://openfilm.cc/zh/)
- 🇬🇧 **English**: [https://openfilm.cc/en/](https://openfilm.cc/en/)

---

## 📝 文章 / Articles

### 中文文章
- [一次性相机与被误读的胶片感](https://openfilm.cc/zh/posts/disposable-cameras-and-the-film-look/)
- [为什么胶片依然重要](https://openfilm.cc/zh/posts/why-film-still-matters/)
- [实况照片 - Live Photos 介绍](https://openfilm.cc/zh/posts/live-photos-introduction-zh/)

### English Articles
- [Disposable Cameras and the Misunderstood Film Look](https://openfilm.cc/en/posts/disposable-cameras-and-the-film-look-en/)
- [Why Film Still Matters in 2026](https://openfilm.cc/en/posts/why-film-still-matters-en/)
- [Live Photos - Bring Your Photos to Life](https://openfilm.cc/en/posts/live-photos-introduction-en/)

---

## 🛠️ Tech Stack

- **Framework**: [Astro 6](https://astro.build/)
- **Content**: MDX (Markdown + JSX)
- **Deployment**: [Cloudflare Pages](https://pages.cloudflare.com/)
- **Web Component**: [live-photo-component](https://www.npmjs.com/package/live-photo-component)

## 🌐 多语言架构 / i18n Architecture

本项目采用**文件名后缀**方案实现中英双语：

- 中文文章：文件名以 `-zh` 结尾或不包含 `-en`
- 英文文章：文件名以 `-en` 结尾

**路由结构**：
- `/zh/...` → 中文页面
- `/en/...` → English pages
- `/` → 自动根据浏览器语言重定向

## 🚀 Local Development

```bash
npm install
npm run dev
```

## 📦 Build

```bash
npm run build
```

### Cloudflare Pages Settings

- **Framework preset**: `Astro`
- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Production domain**: `openfilm.cc`

---

📧 **Contact**: [openfilm.cc](https://openfilm.cc)
