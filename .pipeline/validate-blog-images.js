#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import sharp from "sharp";

const ALLOWED_COLORS = new Set([
  "#F7F6F3", "#FFFFFF", "#1F1F1F", "#2B2B2B", "#374151",
  "#4A4A4A", "#6B6B6B", "#8A8880", "#9A9890", "#B8B6B0",
  "#D3D1CB", "#E3E2DE", "#EAE8E2", "#D97757", "#3A7CA5",
  "#C04B3A",
]);
const CJK = /[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/u;

function parseArgs(argv) {
  const result = { files: [] };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === "--locale") result.locale = argv[++i];
    else result.files.push(argv[i]);
  }
  return result;
}

function attr(source, name) {
  const match = source.match(new RegExp(`\\b${name}=(?:"([^"]*)"|'([^']*)')`, "i"));
  return match ? (match[1] ?? match[2]) : null;
}

function decodeText(source) {
  return source
    .replace(/<[^>]+>/g, "")
    .replaceAll("&amp;", "&")
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&quot;", "\"")
    .replaceAll("&apos;", "'")
    .trim();
}

function estimatedWidth(text, fontSize) {
  let units = 0;
  for (const character of text) {
    if (CJK.test(character)) units += 1;
    else if (/\s/.test(character)) units += 0.32;
    else if (/[A-Z0-9]/.test(character)) units += 0.62;
    else units += 0.54;
  }
  return units * fontSize;
}

function overlaps(a, b) {
  return Math.min(a.right, b.right) > Math.max(a.left, b.left)
    && Math.min(a.bottom, b.bottom) > Math.max(a.top, b.top);
}

function validateLocale(text, locale, file, errors) {
  if (locale === "en" && CJK.test(text)) {
    errors.push(`${file}: English artwork contains CJK text: ${text}`);
  }
  if (locale === "zh" && !CJK.test(text)) {
    errors.push(`${file}: Chinese artwork has no Chinese text`);
  }
}

async function validateSvg(file, locale, index) {
  const source = await fs.readFile(file, "utf8");
  const errors = [];
  const root = source.match(/<svg\b([^>]*)>/i);
  if (!root) return [`${file}: missing SVG root`];
  if (attr(root[1], "data-openfilm-style") !== "technical-v1") {
    errors.push(`${file}: data-openfilm-style must be technical-v1`);
  }
  if (attr(root[1], "data-locale") !== locale) {
    errors.push(`${file}: data-locale must be ${locale}`);
  }
  if (!/Helvetica Neue|Arial|Noto Sans/i.test(attr(root[1], "font-family") || "")) {
    errors.push(`${file}: root font-family must use the OpenFilm sans-serif stack`);
  }
  if (/<(?:linearGradient|radialGradient|filter|image)\b/i.test(source)) {
    errors.push(`${file}: gradients, filters, and embedded images are not allowed`);
  }
  const colors = [...source.matchAll(/#[0-9a-f]{6}\b/gi)].map((match) => match[0].toUpperCase());
  for (const color of new Set(colors)) {
    if (!ALLOWED_COLORS.has(color)) errors.push(`${file}: color ${color} is outside the OpenFilm palette`);
  }

  const viewBox = (attr(root[1], "viewBox") || "").trim().split(/\s+/).map(Number);
  if (viewBox.length !== 4 || viewBox.some((value) => !Number.isFinite(value))) {
    return [...errors, `${file}: invalid viewBox`];
  }
  const [, , width, height] = viewBox;
  const ratio = width / height;
  if (index === 0 && Math.abs(ratio - 1) > 0.01) {
    errors.push(`${file}: first image must be 1:1`);
  }
  if (index > 0 && Math.min(Math.abs(ratio - (16 / 9)), Math.abs(ratio - (4 / 3))) > 0.03) {
    errors.push(`${file}: secondary image must be 16:9 or 4:3`);
  }

  const texts = [...source.matchAll(/<text\b([^>]*)>([\s\S]*?)<\/text>/gi)];
  if (!texts.length) errors.push(`${file}: infographic contains no text`);
  const allText = texts.map((match) => decodeText(match[2])).join(" ");
  validateLocale(allText, locale, file, errors);
  const boxes = [];
  for (const match of texts) {
    const attributes = match[1];
    const text = decodeText(match[2]);
    if (!text) continue;
    const x = Number(attr(attributes, "x"));
    const y = Number(attr(attributes, "y"));
    const fontSize = Number(attr(attributes, "font-size"));
    const maxWidth = Number(attr(attributes, "data-max-width"));
    if (![x, y, fontSize, maxWidth].every(Number.isFinite) || maxWidth <= 0) {
      errors.push(`${file}: every text element needs numeric x, y, font-size, and data-max-width`);
      continue;
    }
    if (
      locale === "zh"
      && !CJK.test(text)
      && attr(attributes, "data-technical-token") !== "true"
    ) {
      errors.push(`${file}: Chinese artwork contains an untranslated text element: ${text}`);
    }
    const measuredWidth = estimatedWidth(text, fontSize);
    if (measuredWidth > maxWidth) {
      errors.push(`${file}: text exceeds data-max-width (${Math.ceil(measuredWidth)} > ${maxWidth}): ${text}`);
    }
    const anchor = attr(attributes, "text-anchor") || "start";
    const left = anchor === "middle" ? x - measuredWidth / 2 : anchor === "end" ? x - measuredWidth : x;
    const right = left + measuredWidth;
    const box = {
      left,
      right,
      top: y - fontSize,
      bottom: y + fontSize * 0.3,
      text,
      overlapOk: attr(attributes, "data-overlap-ok") === "true",
    };
    if (left < 48 || right > width - 48 || box.top < 40 || box.bottom > height - 40) {
      errors.push(`${file}: text violates the outer safe area: ${text}`);
    }
    boxes.push(box);
  }
  for (let i = 0; i < boxes.length; i += 1) {
    for (let j = i + 1; j < boxes.length; j += 1) {
      if (!boxes[i].overlapOk && !boxes[j].overlapOk && overlaps(boxes[i], boxes[j])) {
        errors.push(`${file}: text overlap detected: "${boxes[i].text}" / "${boxes[j].text}"`);
      }
    }
  }

  const metadata = await sharp(file, { failOn: "error" }).metadata();
  if (!metadata.width || !metadata.height) errors.push(`${file}: Sharp could not render the SVG`);
  return errors;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!["zh", "en"].includes(args.locale) || args.files.length < 1 || args.files.length > 3) {
    throw new Error("usage: validate-blog-images.js --locale <zh|en> <1-3 SVG files>");
  }
  const files = args.files.map((file) => path.resolve(file));
  const errors = [];
  for (let index = 0; index < files.length; index += 1) {
    if (path.extname(files[index]).toLowerCase() !== ".svg") {
      errors.push(`${files[index]}: only SVG sources are accepted for localized technical infographics`);
      continue;
    }
    errors.push(...await validateSvg(files[index], args.locale, index));
  }
  if (errors.length) {
    console.error(JSON.stringify({ ok: false, locale: args.locale, errors }, null, 2));
    process.exit(1);
  }
  console.log(JSON.stringify({
    ok: true,
    locale: args.locale,
    count: files.length,
    style: "technical-v1",
    layout: "passed",
    language: "passed",
  }));
}

main().catch((error) => {
  console.error(JSON.stringify({ ok: false, error: error.message }));
  process.exit(1);
});
