---
name: inventus-slides
description: Create management-grade Inventus-branded PPTX or HTML presentations with predefined brand, layout, logo, and visual style rules.
---

# Inventus Slides

You already know the brand. No style discovery, no color picker, no font debates — just great presentations from the start.

**Before touching any code**, do two things in order:
1. Read `memory/preferences.md` — apply any saved user preferences immediately, without asking
2. Read `references/brand_guide.md` (brand rules + color palette) and `references/pptx_guide.md` (PptxGenJS patterns + slide code templates)

---

## Workflow

### Step 1 — Choose Output Mode

Pick based on context. Only ask if genuinely ambiguous.

| Signal | Mode |
|--------|------|
| "management", "share", "send", "deck" | **PPTX** (default) |
| "browser", "present live", "animate", "web" | **HTML** |
| No signal | **PPTX** |

### Step 1A — Prefer Template-First PPTX Mode

When working in **PPTX** and an Inventus template is available, use **template-first mode** by default.

Template-first mode means:
- Start from the provided Inventus `.pptx` or `.potx` template, not from a blank presentation
- Preserve the template's theme, master, layouts, logo treatment, and recurring visual elements
- Treat the Inventus template as a compact brand system rather than a full library of ready-made content pages
- Use the retained blank/branded layouts as the default canvas, then compose the content page using `frontend-slides` principles

Use template-first mode whenever one of these is true:
- the user provides an Inventus template file
- the skill bundles a canonical Inventus template in `assets/`
- the current task is an internal management or executive deck where template consistency matters more than custom visual invention

Only fall back to from-scratch PPTX generation when:
- no suitable Inventus template is available
- the template lacks a layout that can reasonably support the story
- the user explicitly asks for a custom visual treatment instead of the standard Inventus template

#### Template-First Rules

- **Do not manually paste or redraw the Inventus logo** when it already exists in the template layout. Treat the template's built-in logo as the source of truth.
- **Treat the template's brand-colour guidance slide as authoritative** when generating from that template.
- **Use the template's agenda slide by default** unless the user asks for a different opening structure or the deck is too short to justify one.
- **The bundled template keeps only a small approved layout set.** Default working set: `Cover Slide`, `Agenda/Contents Slide`, `Bullet point slide Abstract`, `Empty Slide with Logo`, `1_Empty Slide`, and `Thank You Slide`, plus the `Inventus Brand Colors` reference layout.
- **For most content pages, prefer `Empty Slide with Logo` plus a clean custom composition.** Use `1_Empty Slide` only when the logo would interfere with the composition.
- **Use `Bullet point slide Abstract` sparingly.** It is an optional visual variant, not the default content canvas.
- **Use `frontend-slides` principles for PPTX page composition too.** Keep one idea per slide, strong hierarchy, generous whitespace, and narrative-fit layouts rather than template-looking filler.
- **Choose layout type based on the content shape.** Example: schedules may need a custom timeline; summary metrics may need stat cards; comparisons may need a custom two-column layout; charts should be chosen by agent judgment based on the story.
- **For internal management / CEO decks, prefer cleaner template layouts over decorative image-heavy ones.** Avoid Android / CERT / product imagery unless it materially improves the message.
- **When the request matches a common Inventus deck type, start from the default deck flow in `references/template_layout_map.md` before inventing a new structure.**

#### Recommended Layout Mapping

When a template contains named layouts, use a simple semantic mapping first:

| Story Need | Preferred Template Layout |
|-----------|----------------------------|
| Cover / opening statement | `Cover Slide` |
| Agenda / contents | `Agenda/Contents Slide` |
| KPI summary / headline numbers | `Empty Slide with Logo` |
| Executive summary | `Empty Slide with Logo` |
| Comparison / tradeoff | `Empty Slide with Logo` or `1_Empty Slide` |
| Schedule / roadmap / milestones | `Empty Slide with Logo` or `1_Empty Slide` |
| Data narrative / chart-led slide | `Empty Slide with Logo` |
| Light abstract content page | `Bullet point slide Abstract` |
| Closing / thank-you | `Thank You Slide` |

If no template layout fits perfectly, use the blank branded canvas and build a custom composition before switching to full from-scratch construction.

For recurring Inventus use cases such as:
- project manager performance reviews
- project progress reviews
- memory supply analysis
- process optimization / before-after reviews

use the default flow guidance in `references/template_layout_map.md` as the first structural draft.

### Step 2 — Architect the Slides Before Writing Code

This is the most important step. A great Inventus deck has a clear *visual rhythm* — the reader feels the argument building before they read a word.

**The Sandwich Framework** (proven on the Memory Supply Crisis deck):

```
[DARK]  Cover slide — Green Forest bg, bold white claim, 3–4 stat callouts
[LIGHT] Content slide(s) — data / narrative / recommendations
[DARK]  Closing slide (for decks >3 slides) — single CTA or key takeaway
```

The dark–light–dark rhythm creates visual momentum and feels premium. Never put two dark slides back to back (unless doing a deliberate section break).

**Before coding, write out the slide plan in plain text:**
```
Slide 1 (dark cover): "Global Memory Supply Crisis" — 4 stat cards
Slide 2 (light data): Price chart + 3 insight cards + allocation mini-stats
```
Show this plan to yourself — does each slide do exactly ONE thing? If a slide tries to do two things, split it.

### Step 3 — Apply the Inventus Slide Vocabulary

Use the right slide type for each job. See `references/pptx_guide.md` for code for each type.

| Slide Type | Use When | Key Elements |
|------------|----------|--------------|
| **Dark Cover** | Opening; section breaks | Forest bg, white title, Eucalyptus subtitle, stat cards, white logo top-right, texture bleed |
| **Chart + Insight Panel** | One key dataset + its implications | Left: bar/line chart; Right: 3 insight cards w/ Forest left accent |
| **Stat Grid** | Showing scale/severity at a glance | 3–4 large-number cards on Dark Ocean bg, sage top stripe |
| **Insight Trio** | Recommendations or findings | 3 Forest-accented cards on white, equal width |
| **Comparison Two-Column** | Options, before/after, scenarios | Light bg, two Forest-bordered columns |
| **Timeline** | Roadmap, history, milestones | Horizontal flow on light bg, Forest milestone dots |
| **Data Table** | Structured multi-row data | Alternating Eucalyptus/White rows, Forest header |
| **Dark Closing** | Last slide, CTA, summary | Forest bg, single bold statement, white logo |

### Step 4 — Content Density Rules

These rules are what separate a crisp executive deck from a wall of text.

- **One idea per slide.** If you need a "Part A / Part B" heading, it's two slides.
- **Stat cards**: value + one-line label + one-line source/context. Never more.
- **Insight cards**: bold title (5 words max) + 1–2 sentence body. Resist the urge to write paragraphs.
- **Charts**: title axis labels and data labels — no legend if only one series. Let the data breathe.
- **Source lines**: always at the bottom in muted color. Required if any data was sourced externally.

### Step 5 — Generate

For **PPTX**, choose one of two paths:

1. **Template-first PPTX mode** (preferred)
   - Load the provided or bundled Inventus template
   - Use the retained template-native layouts only: cover / agenda / bullet-abstract / blank canvases / thank-you
   - Use `Empty Slide with Logo` as the default canvas for most content pages
   - Use `1_Empty Slide` only when a totally clean canvas is compositionally better
   - Preserve the template's built-in theme colours, logos, and recurring brand elements
   - Build the content-page composition using `frontend-slides` principles adapted to PPTX
   - Remove instructional/example slides and keep the final deck template-native

2. **From-scratch PPTX mode** (fallback only)
   - Follow `references/pptx_guide.md`
   - Use PptxGenJS with the LAYOUT_WIDE preset
   - Run from `/tmp/pptx_work/` (where pptxgenjs is already installed)
   - Save output to the user's workspace folder

Prefer template-first mode whenever possible. Use from-scratch mode only when the template is unavailable or clearly unsuitable for the requested story.

For **HTML**: follow the frontend-slides approach with the Inventus CSS variables from `references/brand_guide.md`. Use DM Sans from Google Fonts (closest web match to PP Neue Montreal). The CSS custom properties replace all ad-hoc color values.

### Step 6 — QA

After generating, do a visual check:
1. Run `qlmanage -t -s 2000 -o /tmp/ file.pptx` (macOS) to get a thumbnail of slide 1
2. Open the thumbnail and check: logo visible? Colors on-brand? Text not clipped?
3. For multi-slide decks, open in Keynote or PowerPoint and click to slide 2+
4. Fix any issues before delivering

### Step 7 — Save Feedback to Memory

**This is how the skill learns over time.** After delivering a deck, if the user gives any feedback — even casual remarks like "I like this better without italic subtitles" or "can we always do 3 cards not 4" — save it to `memory/preferences.md`.

Format:
```
- [YYYY-MM-DD] CATEGORY: What the user prefers and why (if known)
```

Categories to use: `STAT_CARDS`, `TYPOGRAPHY`, `LAYOUT`, `COLORS`, `CHART`, `CONTENT_DENSITY`, `OTHER`

On every future invocation, silently apply all saved preferences before generating. Don't announce them unless the user asks — just do it.

---

## Logo Placement Rules

| Slide Background | Logo to Use | Position |
|-----------------|-------------|----------|
| Dark (Forest / Dark Ocean) | `assets/logo_white.png` | Top-right, x=10.2", y=0.3", w=2.8", h=0.41" |
| Light (Inventus White) | `assets/logo_dark.png` | Top-right, x=10.2", y=0.3", w=2.8", h=0.41" |

These rules apply to **from-scratch PPTX generation** and **HTML builds**.

When using a real Inventus template:
- do **not** add a second manual logo if the layout already includes one
- do **not** override the template's logo treatment unless the user explicitly asks

If a deck is being built from scratch, load logos from the `assets/` folder relative to this skill. The `pptx_guide.md` shows the exact base64-loading snippet.

---

## Dos and Don'ts

**Do:**
- Let the stat numbers speak — huge font, minimal label
- Use the Forest green left-accent bar on insight cards (it's the brand's signature motif)
- Apply the background texture (`assets/bg_texture.png`) on dark slides at 75–80% transparency, right-side bleed only
- Keep the Forest green vertical stripe (0.18" wide, full height) on light content slides as the left-edge motif
- Source every data point at the bottom of the slide

**Don't:**
- Use the red accent from the old version — Inventus palette has no red
- Mix dark and light randomly — respect the sandwich rhythm
- Use more than 3 colors in any chart — Forest, Dark Ocean, Inventus Black is the set
- Forget to use `LAYOUT_WIDE` (13.33" × 7.5") — standard 10"×5.625" looks wrong with this brand
- Leave placeholder text — always fill every element before saving

---

## Quick Reference: Brand Colors

| Name | Hex | Role |
|------|-----|------|
| Green Forest | `003837` | Primary brand, dark slide bg, left accent bar |
| Inventus Black | `181B1B` | Body text on light slides |
| Inventus White | `F5F9F7` | Light slide background |
| Dark Ocean | `003446` | Stat card fill, secondary dark |
| Inventus Life | `90B59B` | Card top accent stripe, secondary text on dark |
| Eucalyptus | `E0EDE6` | Body text on dark slides, card borders |
| Light Ocean | `708990` | Muted labels, captions, axis text |
| Mint | `E2F0F3` | Very light backgrounds, hover states |

Full palette with CMYK values: see `assets/brand_colors.png`.

---

## Environment Notes

This skill is designed to run in both Claude-style `.skill` packaging and Codex folder-based skills. Key paths should be resolved relative to the skill directory so the same contents work in either environment:

| Resource | Path |
|----------|------|
| Brand assets | `<skill_dir>/assets/` — always resolve relative to this SKILL.md |
| Bundled template | `<skill_dir>/assets/Inventus_Template.pptx` |
| PptxGenJS | `/tmp/pptx_work/` — install once with `cd /tmp/pptx_work && npm install pptxgenjs` if missing |
| User preferences | `<skill_dir>/memory/preferences.md` |
| Template layout map | `<skill_dir>/references/template_layout_map.md` |
| Output (default) | Ask the user, or infer from context |

**Bundled template package**
- `assets/Inventus_Template.pptx` is the cleaned starter template for template-first Inventus PPTX work
- `references/template_layout_map.md` maps story types to the real template layout names
- Treat the bundled template as the default starting point for Inventus PPTX work

**If pptxgenjs is not installed** (fresh environment), run:
```bash
mkdir -p /tmp/pptx_work && cd /tmp/pptx_work && npm init -y && npm install pptxgenjs
```

**Asset path resolution** — in your node scripts, set SKILL_ASSETS to the directory containing this SKILL.md file plus `/assets`:
```javascript
const path = require("path");
const SKILL_ASSETS = path.join(__dirname, "assets");  // works from any install location
```

**Cross-runtime note**: Keep all assets bundled with the skill and always resolve paths relative to `SKILL.md`. The same skill contents should remain usable whether loaded from a Claude `.skill` archive or from a Codex skill folder.

## Self Improvement

This is a `self_customize` skill. Maintain it only from the canonical folder `skills/personal/self_customize/inventus-slides` in the `ai-skills-hub` repo through Codex or Claude Code.

Claude App / Claude.ai uploads are read-only release snapshots. Maintain skill changes only from the canonical repo source through Codex or Claude Code.
