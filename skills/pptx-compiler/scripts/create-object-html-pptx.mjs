import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";

const workspaceRequire = createRequire(path.join(process.cwd(), "package.json"));
const { Presentation, PresentationFile } = workspaceRequire("@oai/artifact-tool");

function args(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    if (!argv[i].startsWith("--")) continue;
    const key = argv[i].slice(2);
    out[key] = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : "true";
  }
  return out;
}

function usage() {
  console.error(`Usage:
  node scripts/create-object-html-pptx.mjs --scene /path/to/scene.json --out /path/to/output.pptx --qa-dir /path/to/qa [--asset-base /path/to/html-folder]
`);
  process.exit(2);
}

const options = args(process.argv.slice(2));
if (!options.scene || !options.out) usage();

const scenePath = options.scene;
const outputPptx = options.out;
const qaDir = options["qa-dir"] || path.join(path.dirname(outputPptx), "qa");
const assetBase = options["asset-base"] || path.dirname(scenePath);

function normalizeColor(value, fallback = "#000000") {
  if (!value) return fallback;
  const rgba = String(value).match(/rgba?\(([^)]+)\)/);
  if (!rgba) return value;
  const [r, g, b, a] = rgba[1].split(",").map((p) => Number.parseFloat(p.trim()));
  if (Number.isFinite(a) && a === 0) return "none";
  const hex = [r, g, b].map((n) => Math.max(0, Math.min(255, Math.round(n))).toString(16).padStart(2, "0")).join("");
  return `#${hex}`;
}

function contentTypeFromUrl(url) {
  const ext = path.extname(new URL(url, "file:///").pathname).toLowerCase();
  if (ext === ".jpg" || ext === ".jpeg") return "image/jpeg";
  if (ext === ".svg") return "image/svg+xml";
  if (ext === ".webp") return "image/webp";
  return "image/png";
}

async function bytesFor(src) {
  if (/^https?:\/\//i.test(src)) {
    const res = await fetch(src);
    if (!res.ok) throw new Error(`Failed to fetch image ${src}: ${res.status}`);
    return new Uint8Array(await res.arrayBuffer());
  }
  const filePath = src.startsWith("file://") ? new URL(src) : path.resolve(assetBase, src);
  return fs.readFile(filePath);
}

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

await fs.mkdir(path.dirname(outputPptx), { recursive: true });
await fs.mkdir(qaDir, { recursive: true });

const scene = JSON.parse(await fs.readFile(scenePath, "utf8"));
const presentation = Presentation.create({
  slideSize: { width: scene.width, height: scene.height },
});

const imageCache = new Map();
let fullSlideImageCount = 0;

for (const slideScene of scene.slides) {
  const slide = presentation.slides.add();
  slide.background.fill = normalizeColor(slideScene.background, "#ffffff");

  for (const item of slideScene.elements) {
    const position = item.position;
    if (position.width <= 0 || position.height <= 0) continue;

    if (item.kind === "shape") {
      slide.shapes.add({
        geometry: item.shape || "rect",
        position,
        fill: normalizeColor(item.fill, "#ffffff"),
        line: { style: "solid", fill: "none", width: 0 },
      });
      continue;
    }

    if (item.kind === "image") {
      if (!item.src) continue;
      let cached = imageCache.get(item.src);
      if (!cached) {
        cached = {
          blob: await bytesFor(item.src),
          contentType: contentTypeFromUrl(item.src),
        };
        imageCache.set(item.src, cached);
      }
      slide.images.add({
        blob: cached.blob,
        contentType: cached.contentType,
        alt: item.alt || "HTML asset",
        fit: item.fit || "contain",
        position,
      });
      if (position.left === 0 && position.top === 0 && position.width === scene.width && position.height === scene.height) {
        fullSlideImageCount += 1;
      }
      continue;
    }

    if (item.kind === "text") {
      const shape = slide.shapes.add({
        geometry: "textbox",
        position,
        fill: "none",
        line: { style: "solid", fill: "none", width: 0 },
      });
      shape.text = item.text;
      shape.text.style = {
        fontSize: Math.max(4, item.style?.fontSize || 12),
        bold: Boolean(item.style?.bold),
        italic: Boolean(item.style?.italic),
        color: normalizeColor(item.style?.color, "#000000"),
        alignment: item.style?.alignment || "left",
        typeface: item.style?.typeface || "Arial",
        insets: { top: 0, right: 0, bottom: 0, left: 0 },
        wrap: "square",
        autoFit: "shrinkText",
      };
    }
  }
}

for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  await writeBlob(path.join(qaDir, `${stem}.png`), await presentation.export({ slide, format: "png", scale: 1 }));
  await fs.writeFile(path.join(qaDir, `${stem}.layout.json`), await (await slide.export({ format: "layout" })).text());
}

await writeBlob(path.join(qaDir, "montage.webp"), await presentation.export({ format: "webp", montage: true, scale: 1 }));

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(outputPptx);
console.log(JSON.stringify({ outputPptx, qaDir, slides: scene.slides.length, fullSlideImageCount }, null, 2));
