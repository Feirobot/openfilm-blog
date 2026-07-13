#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import sharp from "sharp";

const REPO = process.env.OPENFILM_REPO || "/root/AIwork/openfilm-blog";
const CONFIG = "/root/.qoder-alpha/extensions/d9b25b78e908/.mcp.json";
const BUCKET = "openfilm";
const PUBLIC_BASE = "https://media.openfilm.cc";

function parseArgs(argv) {
  const result = { files: [] };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === "--slug") result.slug = argv[++i];
    else if (argv[i] === "--manifest") result.manifest = argv[++i];
    else if (argv[i] === "--date") result.date = argv[++i];
    else if (argv[i] === "--self-test") result.selfTest = true;
    else if (argv[i] === "--self-test-upload") result.selfTestUpload = true;
    else result.files.push(argv[i]);
  }
  return result;
}

async function cloudflareContext() {
  const config = JSON.parse(await fs.readFile(CONFIG, "utf8"));
  const authorization = config?.mcpServers?.["cloudflare-mcp"]?.headers?.Authorization;
  if (!authorization?.startsWith("Bearer ")) throw new Error("Cloudflare authorization is unavailable");
  const response = await fetch("https://api.cloudflare.com/client/v4/accounts?per_page=50", {
    headers: { Authorization: authorization },
    signal: AbortSignal.timeout(60000),
  });
  const payload = await response.json();
  if (!response.ok || !payload.success) throw new Error(`Cloudflare account lookup failed (${response.status})`);
  const configured = process.env.OPENFILM_CF_ACCOUNT_ID;
  const account = configured ? payload.result.find((item) => item.id === configured) : payload.result[0];
  if (!account || (!configured && payload.result.length !== 1)) {
    throw new Error("Set OPENFILM_CF_ACCOUNT_ID when the token can access multiple accounts");
  }
  return { authorization, accountId: account.id };
}

async function upload(context, key, file) {
  const bytes = await fs.readFile(file);
  const encodedKey = key.split("/").map(encodeURIComponent).join("/");
  const endpoint = `https://api.cloudflare.com/client/v4/accounts/${context.accountId}/r2/buckets/${BUCKET}/objects/${encodedKey}`;
  const response = await fetch(endpoint, {
    method: "PUT",
    headers: { Authorization: context.authorization, "Content-Type": "image/webp" },
    body: bytes,
    signal: AbortSignal.timeout(60000),
  });
  if (!response.ok) throw new Error(`R2 upload failed for ${key} (${response.status})`);
  const url = `${PUBLIC_BASE}/${key}`;
  const verification = await fetch(url, { method: "HEAD", signal: AbortSignal.timeout(60000) });
  const contentType = verification.headers.get("content-type") || "";
  if (!verification.ok || !contentType.startsWith("image/webp")) {
    throw new Error(`Public verification failed for ${url} (${verification.status}, ${contentType || "no content-type"})`);
  }
  return url;
}

async function removeObject(context, key) {
  const encodedKey = key.split("/").map(encodeURIComponent).join("/");
  const endpoint = `https://api.cloudflare.com/client/v4/accounts/${context.accountId}/r2/buckets/${BUCKET}/objects/${encodedKey}`;
  const response = await fetch(endpoint, {
    method: "DELETE",
    headers: { Authorization: context.authorization },
    signal: AbortSignal.timeout(60000),
  });
  if (!response.ok) throw new Error(`R2 health object cleanup failed (${response.status})`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const context = await cloudflareContext();
  if (args.selfTest) {
    console.log(JSON.stringify({ ok: true, service: "cloudflare-r2", bucket: BUCKET }));
    return;
  }
  if (args.selfTestUpload) {
    const healthDir = path.join(REPO, ".pipeline", "generated", ".health");
    const healthFile = path.join(healthDir, "probe.webp");
    const key = `pipeline-health/${Date.now()}-probe.webp`;
    await fs.mkdir(healthDir, { recursive: true });
    await sharp({ create: { width: 2, height: 2, channels: 3, background: "#ffffff" } }).webp().toFile(healthFile);
    try {
      await upload(context, key, healthFile);
      await removeObject(context, key);
    } finally {
      await fs.rm(healthFile, { force: true });
    }
    console.log(JSON.stringify({ ok: true, upload: "verified", cleanup: "verified", bucket: BUCKET }));
    return;
  }
  if (!args.slug || !/^[a-z0-9][a-z0-9-]*$/.test(args.slug) || !args.manifest) {
    throw new Error("usage: publish-media.js --slug <slug> --manifest <file> [--date YYYYMMDD] <1-3 source images>");
  }
  if (args.files.length < 1 || args.files.length > 3) throw new Error("Provide 1 to 3 source images");

  const date = args.date || new Date().toLocaleDateString("en-CA", { timeZone: "Asia/Shanghai" }).replaceAll("-", "");
  const outputDir = path.join(REPO, ".pipeline", "generated", args.slug);
  await fs.mkdir(outputDir, { recursive: true });
  const images = [];

  for (let i = 0; i < args.files.length; i += 1) {
    const source = path.resolve(args.files[i]);
    const output = path.join(outputDir, `${date}-${i + 1}.webp`);
    let pipeline = sharp(source, { failOn: "error" });
    if (i === 0) {
      pipeline = pipeline.resize(1200, 1200, { fit: "cover", position: "attention" });
    } else {
      pipeline = pipeline.resize(1600, 1600, { fit: "inside", withoutEnlargement: true });
    }
    await pipeline.webp({ quality: 82, effort: 5 }).toFile(output);
    const metadata = await sharp(output).metadata();
    const key = `images/${args.slug}/${date}-${i + 1}.webp`;
    const url = await upload(context, key, output);
    images.push({ url, local: output, width: metadata.width, height: metadata.height, key });
  }

  const manifestPath = path.resolve(args.manifest);
  await fs.mkdir(path.dirname(manifestPath), { recursive: true });
  await fs.writeFile(manifestPath, `${JSON.stringify({ slug: args.slug, images }, null, 2)}\n`, "utf8");
  console.log(JSON.stringify({ ok: true, count: images.length, manifest: manifestPath, urls: images.map((item) => item.url) }));
}

main().catch((error) => {
  console.error(JSON.stringify({ ok: false, error: error.message }));
  process.exit(1);
});
