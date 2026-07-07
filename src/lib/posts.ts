import type { CollectionEntry } from "astro:content";

export type Lang = "zh" | "en";
export type Post = CollectionEntry<"posts">;

export function postSlug(id: string) {
  return id.replace(/\.mdx?$/, "");
}

export function postLang(post: Post): Lang {
  const id = post.id.toLowerCase();
  return id.endsWith("-en") ? "en" : "zh";
}

export function postKey(id: string) {
  return postSlug(id).replace(/-(zh|en)$/i, "");
}

export function postHref(post: Post, lang = postLang(post)) {
  return `/${lang}/posts/${postSlug(post.id)}/`;
}

export function alternatePostHref(post: Post, allPosts: Post[], targetLang: Lang) {
  const key = postKey(post.id);
  const match = allPosts.find((candidate) => {
    return !candidate.data.draft && postLang(candidate) === targetLang && postKey(candidate.id) === key;
  });

  return match ? postHref(match, targetLang) : `/${targetLang}/`;
}

export function publishedPostsForLang(posts: Post[], lang: Lang) {
  return posts
    .filter((post) => !post.data.draft && postLang(post) === lang)
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

export function postCategory(post: Post, lang: Lang) {
  const tags = post.data.tags.map((tag) => tag.toLowerCase());
  const id = post.id.toLowerCase();
  const title = post.data.title.toLowerCase();

  if (tags.some((tag) => tag.includes("暗房") || tag.includes("darkroom")) || id.includes("processing") || id.includes("developing")) {
    return lang === "zh" ? "暗房" : "Darkroom";
  }

  if (
    tags.some((tag) => tag.includes("工具") || tag.includes("tools") || tag.includes("maintenance")) ||
    id.includes("camera") ||
    id.includes("scanning") ||
    title.includes("相机")
  ) {
    return lang === "zh" ? "工具" : "Tools";
  }

  if (
    tags.some((tag) => tag.includes("文化") || tag.includes("culture") || tag.includes("essay") || tag.includes("opinion")) ||
    id.includes("revival") ||
    id.includes("community")
  ) {
    return lang === "zh" ? "文化" : "Culture";
  }

  return lang === "zh" ? "技巧" : "Technique";
}
