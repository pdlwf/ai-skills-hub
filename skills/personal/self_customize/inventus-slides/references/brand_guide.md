# Inventus Brand Guide — Slides

## Palette

```
Green Forest  #003837   RGB(0,56,55)     — Primary brand, dark slide backgrounds
Inventus Black #181B1B  RGB(24,27,27)    — Headlines and body on light slides
Inventus White #F5F9F7  RGB(245,249,247) — Light slide background
Dark Ocean     #003446  RGB(0,52,70)     — Stat card fill, secondary dark surfaces
Inventus Life  #90B59B  RGB(144,181,155) — Accent stripe on cards, supporting text on dark
Eucalyptus     #E0EDE6  RGB(224,237,230) — Body text on dark slides, light card borders
Light Ocean    #708990  RGB(112,137,144) — Muted labels, axis text, captions
Mint           #E2F0F3  RGB(226,240,243) — Backgrounds, hover states, dividers
```

Avoid: pure black (#000000), pure white (#FFFFFF), any red/orange tones — they are off-brand.

## Typography

| Context | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Slide title (dark bg) | Calibri (PPTX) / DM Sans (HTML) | 30–38pt | Bold | FFFFFF |
| Slide title (light bg) | Calibri / DM Sans | 28–34pt | Bold | 181B1B |
| Subtitle / meta | Calibri / DM Sans | 12–14pt | Regular Italic | E0EDE6 / 708990 |
| Stat number | Calibri / DM Sans | 44–54pt | Bold | FFFFFF |
| Card label | Calibri / DM Sans | 11–13pt | Bold | E0EDE6 / 181B1B |
| Card body | Calibri / DM Sans | 10–12pt | Regular | 708990 |
| Source line | Calibri / DM Sans | 8–9pt | Regular | 2A6260 / 90B59B |

PP Neue Montreal Book is the official brand font but is not bundled with Windows/macOS. Always substitute Calibri for PPTX and DM Sans (Google Fonts) for HTML.

## Logo Usage

- **On dark (Forest / Dark Ocean)**: use `logo_white.png`
- **On light (Inventus White / Mint)**: use `logo_dark.png`
- Minimum width: 1.5" in PPTX, 120px in HTML
- Always top-right corner. Never rotate, recolor, or add drop shadows.
- Clear space: at minimum 0.15" (PPTX) / 12px (HTML) on all sides

## Layout Motifs

**Left green stripe** — Forest #003837, 0.18" wide × full slide height. Place on every light content slide to echo the dark cover.

**Background texture** — `assets/bg_texture.png`, right-side bleed (starts at x=7.5"), transparency 75–80%. Only on dark slides.

**Card accent bar** — Forest #003837, 0.065–0.07" wide × card height, left edge of every insight/info card. The single most recognizable Inventus motif.

**Sage top stripe on stat cards** — Inventus Life #90B59B, 0.055" tall × full card width, top edge of Dark Ocean stat cards.

## HTML CSS Variables

```css
:root {
  --inv-forest:    #003837;
  --inv-black:     #181B1B;
  --inv-white:     #F5F9F7;
  --inv-ocean:     #003446;
  --inv-life:      #90B59B;
  --inv-eucalypt:  #E0EDE6;
  --inv-lt-ocean:  #708990;
  --inv-mint:      #E2F0F3;
  --font-main: 'DM Sans', system-ui, sans-serif;
}
```

Import DM Sans: `@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');`

## Chart Color Sequence

1. `003837` (Forest) — primary series
2. `003446` (Dark Ocean) — secondary series
3. `708990` (Light Ocean) — tertiary series
4. `90B59B` (Inventus Life) — quaternary series

Chart area background: always match slide background (`F5F9F7` on light slides).
Grid lines: `E0EDE6` at 0.5–0.75pt. No category grid lines. Axis labels: `708990`.
