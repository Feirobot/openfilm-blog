import { defineCollection } from "astro:content";

const posts = defineCollection({
  type: "content",
  // No schema - all frontmatter fields will be available
});

export const collections = { posts };
