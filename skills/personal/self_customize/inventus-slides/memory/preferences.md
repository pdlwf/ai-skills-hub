# Inventus Slides — User Preferences

This file stores preferences and feedback learned from past sessions.
The runtime should read this file at the start of every skill invocation and apply these preferences automatically.

<\!-- PREFERENCES_START -->
- [2026-04-16] LAYOUT: When an Inventus PPT template is provided, use it primarily as a brand/style carrier; for content pages prefer `Empty Slide with Logo` or `1_Empty Slide` plus custom composition rather than relying on weak built-in content layouts.
- [2026-04-16] OTHER: The Inventus globe logo is part of the provided PPT theme/template; do not manually paste or redraw the logo on each slide when working from that template.
- [2026-04-16] COLORS: Treat the template's brand color guidance slide as authoritative when generating decks from that template.
- [2026-04-16] LAYOUT: Use the template's agenda slide as the default agenda structure unless the user asks for a different opening flow.
- [2026-04-16] CHART: Keep chart-form selection flexible; chart type should remain agent judgment based on the story rather than a fixed default.
- [2026-04-16] CONTENT_DENSITY: For internal management or CEO-facing decks, avoid decorative Android/CERT/product imagery unless it materially improves the message.
- [2026-04-16] LAYOUT: The old weak content layouts such as `Chart Slide`, `Boxes with Numbers (4)`, `Summary Slide`, and `Numbers Slide` should not be used; prefer cleaner custom layouts that still match Inventus brand style.
- [2026-04-16] TEMPLATE: In the bundled Inventus template, keep only the approved working layouts: `Inventus Brand Colors`, `Cover Slide`, `Agenda/Contents Slide`, `Bullet point slide Abstract`, `Empty Slide with Logo`, `1_Empty Slide`, and `Thank You Slide`.
- [2026-04-16] LAYOUT: For most real content pages, default to `Empty Slide with Logo`; use `1_Empty Slide` only when the built-in logo interferes with the composition, and use `Bullet point slide Abstract` only as an occasional visual variant.
<\!-- PREFERENCES_END -->

---

## How to Update

When the user gives feedback during a session (e.g. "make the titles bigger", "I prefer 3 cards not 4",
"stop using italic subtitles"), save it here so it applies to every future deck.

Use this format for each preference:
```
- [DATE] TOPIC: preference detail
  Example: [2026-04-15] STAT_CARDS: User prefers 3 cards max on cover slides, not 4
```
