import { createRequire } from "node:module";
import path from "node:path";
import { mkdir, writeFile } from "node:fs/promises";

const require = createRequire(import.meta.url);
let playwright;
try {
  playwright = require("playwright");
} catch {
  const fallbackModule = process.env.PLAYWRIGHT_MODULE;
  if (!fallbackModule) {
    throw new Error("Playwright is not available. Install it in the workspace or set PLAYWRIGHT_MODULE to the Playwright index.js path.");
  }
  playwright = await import(fallbackModule);
  playwright = playwright.default || playwright;
}

const { chromium } = playwright;

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
  node scripts/extract-html-objects.mjs --html /path/to/index.html --out /path/to/scene.json [--chrome /path/to/Chrome] [--selector section.slide]
`);
  process.exit(2);
}

const options = args(process.argv.slice(2));
if (!options.html || !options.out) usage();

const htmlPath = options.html;
const outPath = options.out;
const slideSelector = options.selector || "section.slide";
const chromePath = options.chrome || process.env.CHROME_PATH || "";

function cleanUrl(value) {
  if (!value || value === "none") return "";
  const match = String(value).match(/url\\((['"]?)(.*?)\\1\\)/);
  return match?.[2] || "";
}

await mkdir(path.dirname(outPath), { recursive: true });

const launchOptions = { headless: true };
if (chromePath) launchOptions.executablePath = chromePath;
const browser = await chromium.launch(launchOptions);
const page = await browser.newPage({
  viewport: { width: 1280, height: 720 },
  deviceScaleFactor: 1,
});
await page.goto(`file://${path.resolve(htmlPath)}`, {
  waitUntil: "networkidle",
  timeout: 60000,
});

const scene = await page.evaluate(({ cleanUrlSource, slideSelector }) => {
  const cleanUrl = eval(`(${cleanUrlSource})`);
  const textTags = new Set(["P", "H1", "H2", "H3", "LI"]);

  function px(value) {
    const n = Number.parseFloat(value);
    return Number.isFinite(n) ? n : 0;
  }

  function colorValue(value) {
    if (!value || value === "transparent" || value === "rgba(0, 0, 0, 0)") return "";
    const rgba = value.match(/rgba?\\(([^)]+)\\)/);
    if (!rgba) return value;
    const parts = rgba[1].split(",").map((p) => Number.parseFloat(p.trim()));
    if (parts.length === 4 && parts[3] === 0) return "";
    return value;
  }

  function rectFor(el, slideRect) {
    const r = el.getBoundingClientRect();
    return {
      left: Math.round((r.left - slideRect.left) * 100) / 100,
      top: Math.round((r.top - slideRect.top) * 100) / 100,
      width: Math.round(r.width * 100) / 100,
      height: Math.round(r.height * 100) / 100,
    };
  }

  function isInsideCapturedText(el) {
    let parent = el.parentElement;
    while (parent) {
      if (textTags.has(parent.tagName)) return true;
      parent = parent.parentElement;
    }
    return false;
  }

  function directText(el) {
    let text = "";
    for (const node of el.childNodes) {
      if (node.nodeType === Node.TEXT_NODE) text += node.textContent || "";
    }
    return text.replace(/\\s+/g, " ").trim();
  }

  function explicitZIndex(style) {
    const value = Number.parseInt(style.zIndex, 10);
    return Number.isFinite(value) ? value : 0;
  }

  const slides = [...document.querySelectorAll(slideSelector)].map((slide, slideIndex) => {
    const slideRect = slide.getBoundingClientRect();
    const slideStyle = getComputedStyle(slide);
    const elements = [];

    for (const [order, el] of [...slide.querySelectorAll("*")].entries()) {
      const style = getComputedStyle(el);
      if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0) continue;
      const box = rectFor(el, slideRect);
      if (box.width < 1 || box.height < 1) continue;

      const tag = el.tagName;
      const classes = [...el.classList];
      const backgroundColor = colorValue(style.backgroundColor);
      const backgroundImage = cleanUrl(style.backgroundImage);
      const ownText = directText(el);
      const hasBlockTextDescendant = Boolean(el.querySelector("p,h1,h2,h3,li,div"));
      const hasInlineTextDescendant = Boolean(el.querySelector("span,strong,em,a"));
      const isGenericTextContainer = ownText && !isInsideCapturedText(el) && !hasBlockTextDescendant && !hasInlineTextDescendant;
      const text = (textTags.has(tag) || ((tag === "SPAN" || tag === "STRONG") && !isInsideCapturedText(el)) || isGenericTextContainer)
        ? el.textContent.replace(/\\s+/g, " ").trim()
        : "";

      const base = { order, zIndex: explicitZIndex(style), classes, position: box };

      if (tag === "IMG") {
        elements.push({
          kind: "image",
          tag,
          ...base,
          src: el.currentSrc || el.getAttribute("src"),
          fit: style.objectFit === "cover" ? "cover" : "contain",
          alt: el.getAttribute("alt") || "",
        });
        continue;
      }

      if (backgroundColor) {
        elements.push({
          kind: "shape",
          shape: classes.includes("timeline-arrow") ? "rightArrow" : "rect",
          ...base,
          fill: backgroundColor,
        });
      }

      if (backgroundImage) {
        elements.push({
          kind: "image",
          tag,
          ...base,
          src: backgroundImage,
          fit: "contain",
          alt: classes.join(" ") || "decorative asset",
        });
      }

      if (text) {
        const textFill = colorValue(style.color) || "#000000";
        const isBold = Number(style.fontWeight) >= 600 || style.fontWeight === "bold";
        const textAlign = style.textAlign === "center" || style.textAlign === "right" ? style.textAlign : "left";
        elements.push({
          kind: "text",
          tag,
          ...base,
          text,
          style: {
            color: textFill,
            fontSize: px(style.fontSize),
            fontWeight: style.fontWeight,
            bold: isBold,
            italic: style.fontStyle === "italic",
            alignment: textAlign,
            typeface: style.fontFamily.split(",")[0].replaceAll('"', "").trim() || "Arial",
          },
        });
      }
    }

    return {
      slide: slideIndex + 1,
      background: colorValue(slideStyle.backgroundColor) || "#ffffff",
      elements,
    };
  });

  const firstSlide = document.querySelector(slideSelector);
  const firstSlideRect = firstSlide?.getBoundingClientRect();
  return {
    width: Math.round(firstSlideRect?.width || 1280),
    height: Math.round(firstSlideRect?.height || 720),
    slides,
  };
}, { cleanUrlSource: cleanUrl.toString(), slideSelector });

await browser.close();
await writeFile(outPath, JSON.stringify(scene, null, 2), "utf8");
console.log(JSON.stringify({
  outPath,
  slides: scene.slides.length,
  elements: scene.slides.map((s) => s.elements.length),
}, null, 2));
