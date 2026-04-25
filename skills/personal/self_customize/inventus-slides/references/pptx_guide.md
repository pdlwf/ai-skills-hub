# Inventus PPTX Generation Guide

## Setup

PptxGenJS is pre-installed at `/tmp/pptx_work/`. Always run node scripts from there.

```bash
cd /tmp/pptx_work && node my_script.js
```

If not installed: `mkdir -p /tmp/pptx_work && cd /tmp/pptx_work && npm init -y && npm install pptxgenjs`

## Boilerplate

```javascript
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const FOREST="003837", INV_BLK="181B1B", INV_WHT="F5F9F7", OCEAN="003446";
const LIFE="90B59B", EUCALYPT="E0EDE6", LT_OCEAN="708990", MINT="E2F0F3";

// Asset path — resolves from skill install location automatically
const SKILL_ASSETS = path.join(__dirname, "..", "assets");  // when run from a skill subdir
// OR use absolute path if running ad-hoc:
// const SKILL_ASSETS = "/tmp/inventus-slides/assets";

const logoWhite = "image/png;base64," + fs.readFileSync(`${SKILL_ASSETS}/logo_white.png`).toString("base64");
const logoDark  = "image/png;base64," + fs.readFileSync(`${SKILL_ASSETS}/logo_dark.png`).toString("base64");
const bgTex     = "image/png;base64," + fs.readFileSync(`${SKILL_ASSETS}/bg_texture.png`).toString("base64");

async function build() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";   // 13.33" × 7.5" — always use WIDE for Inventus
  pres.title  = "Presentation Title";
  await pres.writeFile({ fileName: "/path/to/output.pptx" });
}
build().catch(console.error);
```

---

## Slide Patterns

### 1. Dark Cover Slide

```javascript
const s = pres.addSlide();
s.background = { color: FOREST };
s.addImage({ data: bgTex, x: 7.5, y: 1.1, w: 5.83, h: 6.4, transparency: 78 });
s.addImage({ data: logoWhite, x: 10.2, y: 0.3, w: 2.8, h: 0.41 });
s.addShape(pres.shapes.LINE, { x: 0.5, y: 1.05, w: 12.33, h: 0, line: { color: "1A5250", width: 0.75 } });
s.addText("Slide Title Here", { x: 0.5, y: 0.22, w: 9.4, h: 0.72, fontSize: 36, bold: true, color: "FFFFFF", fontFace: "Calibri", align: "left", margin: 0 });
s.addText("Executive Briefing  ·  April 2026", { x: 0.5, y: 0.75, w: 6, h: 0.28, fontSize: 12, color: EUCALYPT, fontFace: "Calibri", align: "left", margin: 0 });
s.addText("One or two sentences framing the situation.", { x: 0.5, y: 1.2, w: 8.8, h: 0.72, fontSize: 13.5, color: EUCALYPT, fontFace: "Calibri", align: "left", margin: 0 });
s.addText("Sources: ...", { x: 0.5, y: 7.2, w: 12.33, h: 0.22, fontSize: 8.5, color: "2A6260", fontFace: "Calibri", align: "left", margin: 0 });
```

### 2. Stat Cards (on dark cover)

```javascript
// 4-card: cW=2.9, gap=0.17  |  3-card: cW=3.9, gap=0.2  |  2-card: cW=5.9, gap=0.5
const stats = [
  { val: "~8×", label: "Price surge", sub: "Jun '25 $14 → Q2 '26 est. $125" },
  { val: "18+", label: "Months of shortage", sub: "Persists through late 2027" },
  { val: "+85%", label: "NAND allocation spike", sub: "Q1 2026 vs prior quarter" },
  { val: "+21%", label: "AI server storage YoY", sub: "2025 → 2026 growth" },
];
const cW=2.9, cH=2.1, cY=2.4, gap=0.17, sx=0.5;
stats.forEach((s, i) => {
  const cx = sx + i*(cW+gap);
  slide.addShape(pres.shapes.RECTANGLE, { x: cx, y: cY, w: cW, h: cH, fill: { color: OCEAN }, line: { color: "1A4A48", width: 1 } });
  slide.addShape(pres.shapes.RECTANGLE, { x: cx, y: cY, w: cW, h: 0.055, fill: { color: LIFE }, line: { type: "none" } });
  slide.addText(s.val, { x: cx+0.2, y: cY+0.12, w: cW-0.25, h: 0.92, fontSize: 48, bold: true, color: "FFFFFF", fontFace: "Calibri", align: "left", margin: 0 });
  slide.addText(s.label, { x: cx+0.2, y: cY+1.06, w: cW-0.25, h: 0.42, fontSize: 12, bold: true, color: EUCALYPT, fontFace: "Calibri", align: "left", margin: 0 });
  slide.addText(s.sub, { x: cx+0.2, y: cY+1.5, w: cW-0.25, h: 0.44, fontSize: 10, color: LIFE, fontFace: "Calibri", align: "left", margin: 0 });
});
```

### 3. Light Content Slide (base)

```javascript
const s = pres.addSlide();
s.background = { color: INV_WHT };
s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.18, h: 7.5, fill: { color: FOREST }, line: { type: "none" } });
s.addImage({ data: logoDark, x: 10.2, y: 0.3, w: 2.8, h: 0.41 });
s.addText("Slide Title", { x: 0.45, y: 0.22, w: 9.5, h: 0.6, fontSize: 30, bold: true, color: INV_BLK, fontFace: "Calibri", align: "left", margin: 0 });
s.addText("Supporting context in italic", { x: 0.45, y: 0.84, w: 10, h: 0.3, fontSize: 12, color: LT_OCEAN, fontFace: "Calibri", italic: true, align: "left", margin: 0 });
s.addShape(pres.shapes.LINE, { x: 0.45, y: 1.2, w: 12.5, h: 0, line: { color: EUCALYPT, width: 1 } });
s.addText("Sources: ...", { x: 0.45, y: 7.22, w: 12.5, h: 0.2, fontSize: 8.5, color: LIFE, fontFace: "Calibri", align: "left", margin: 0 });
```

### 4. Chart + Insight Panel (the power layout)

Add to a light content slide:

```javascript
s.addChart(pres.charts.BAR, [{ name: "Series Name", labels: ["Cat1","Cat2","Cat3","Cat4"], values: [100,200,300,400] }], {
  x: 0.45, y: 1.35, w: 7.2, h: 4.5, barDir: "col",
  chartColors: [FOREST, FOREST, OCEAN, OCEAN],
  chartArea: { fill: { color: INV_WHT }, roundedCorners: false },
  catAxisLabelColor: LT_OCEAN, valAxisLabelColor: LT_OCEAN,
  valGridLine: { color: EUCALYPT, size: 0.75 }, catGridLine: { style: "none" },
  showValue: true, dataLabelPosition: "outEnd",
  dataLabelColor: INV_BLK, dataLabelFontSize: 11, dataLabelFontBold: true, showLegend: false,
});
s.addText("Chart caption", { x: 0.45, y: 5.88, w: 7.2, h: 0.28, fontSize: 9.5, color: LT_OCEAN, fontFace: "Calibri", italic: true, align: "center", margin: 0 });

const insights = [
  { title: "Finding One", body: "One to two sentences." },
  { title: "Finding Two", body: "One to two sentences." },
  { title: "Finding Three", body: "One to two sentences." },
];
const rX=7.9, bW=5.05;
insights.forEach((item, i) => {
  const bY=1.35+i*1.52, bH=1.38;
  s.addShape(pres.shapes.RECTANGLE, { x: rX, y: bY, w: bW, h: bH, fill: { color: "FFFFFF" }, line: { color: EUCALYPT, width: 1 }, shadow: { type: "outer", color: "000000", blur: 6, offset: 3, angle: 135, opacity: 0.06 } });
  s.addShape(pres.shapes.RECTANGLE, { x: rX, y: bY, w: 0.07, h: bH, fill: { color: FOREST }, line: { type: "none" } });
  s.addText(item.title, { x: rX+0.18, y: bY+0.1, w: bW-0.25, h: 0.34, fontSize: 12.5, bold: true, color: INV_BLK, fontFace: "Calibri", align: "left", margin: 0 });
  s.addText(item.body, { x: rX+0.18, y: bY+0.48, w: bW-0.25, h: 0.82, fontSize: 11, color: LT_OCEAN, fontFace: "Calibri", align: "left", margin: 0 });
});
```

### 5. Mini Stat Row (bottom of light slide)

```javascript
const miniStats = [{ label: "Category A", val: "+180–185%" }, { label: "Category B", val: "+165–170%" }, { label: "Category C", val: "+195–200%" }];
const miniY=6.28, mW=1.58, mH=0.85, mGap=0.065, rX=7.9;
miniStats.forEach((m, i) => {
  const mx = rX+i*(mW+mGap);
  s.addShape(pres.shapes.RECTANGLE, { x: mx, y: miniY, w: mW, h: mH, fill: { color: FOREST }, line: { type: "none" } });
  s.addText(m.val, { x: mx, y: miniY+0.08, w: mW, h: 0.38, fontSize: 15, bold: true, color: "FFFFFF", fontFace: "Calibri", align: "center", margin: 0 });
  s.addText(m.label, { x: mx, y: miniY+0.48, w: mW, h: 0.3, fontSize: 9.5, color: EUCALYPT, fontFace: "Calibri", align: "center", margin: 0 });
});
```

### 6. Insight Trio (3-column cards, full width)

```javascript
const findings = [{ num: "01", title: "Title", body: "Two sentences." }, { num: "02", title: "Title", body: "Two sentences." }, { num: "03", title: "Title", body: "Two sentences." }];
const cW=3.9, cH=3.5, cY=1.5, gap=0.27, sx=0.45;
findings.forEach((f, i) => {
  const cx = sx+i*(cW+gap);
  s.addShape(pres.shapes.RECTANGLE, { x: cx, y: cY, w: cW, h: cH, fill: { color: "FFFFFF" }, line: { color: EUCALYPT, width: 1 }, shadow: { type: "outer", color: "000000", blur: 5, offset: 2, angle: 135, opacity: 0.07 } });
  s.addShape(pres.shapes.RECTANGLE, { x: cx, y: cY, w: 0.07, h: cH, fill: { color: FOREST }, line: { type: "none" } });
  s.addText(f.num, { x: cx+0.18, y: cY+0.15, w: 0.5, h: 0.48, fontSize: 22, bold: true, color: FOREST, fontFace: "Calibri", align: "left", margin: 0 });
  s.addText(f.title, { x: cx+0.18, y: cY+0.65, w: cW-0.28, h: 0.44, fontSize: 13, bold: true, color: INV_BLK, fontFace: "Calibri", align: "left", margin: 0 });
  s.addText(f.body, { x: cx+0.18, y: cY+1.15, w: cW-0.28, h: 2.2, fontSize: 11, color: LT_OCEAN, fontFace: "Calibri", align: "left", margin: 0 });
});
```

### 7. Dark Closing Slide

```javascript
const s = pres.addSlide();
s.background = { color: FOREST };
s.addImage({ data: bgTex, x: 7.5, y: 1.1, w: 5.83, h: 6.4, transparency: 78 });
s.addImage({ data: logoWhite, x: 10.2, y: 0.3, w: 2.8, h: 0.41 });
s.addText("Key Takeaway or Call to Action", { x: 0.8, y: 2.4, w: 9, h: 1.2, fontSize: 40, bold: true, color: "FFFFFF", fontFace: "Calibri", align: "left", margin: 0 });
s.addText("Supporting sentence or next step.", { x: 0.8, y: 3.75, w: 8, h: 0.5, fontSize: 16, color: EUCALYPT, fontFace: "Calibri", align: "left", margin: 0 });
```

---

## Common Pitfalls

- **Never use `#` prefix on hex colors** — PptxGenJS silently corrupts the file
- **Never reuse shadow option objects** — PptxGenJS mutates them; create a fresh object each time
- **Always use LAYOUT_WIDE** — standard 10"×5.625" makes the brand look cramped
- **Shadow opacity**: `{ type: "outer", color: "000000", blur: 6, offset: 3, angle: 135, opacity: 0.06 }` — never encode opacity in the hex string
