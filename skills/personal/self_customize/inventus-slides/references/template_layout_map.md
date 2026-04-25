# Inventus Template Layout Map

Canonical bundled template:
- `assets/Inventus_Template.pptx`

Source of the bundled template:
- Derived from `New Inventus PPT Template January 2026v1_blank.pptx`
- Sample and instructional slides were removed
- One clean starter slide using `1_Empty Slide` remains so the deck opens as a valid PPTX
- The bundled template is intentionally trimmed to a small approved layout set only

## Operating Rule

When generating an Inventus PPTX and the bundled template is available:
- start from `assets/Inventus_Template.pptx`
- preserve the theme, master, layouts, and built-in logo treatment
- use only the retained approved layouts from the bundled template:
  - `Inventus Brand Colors`
  - `Cover Slide`
  - `Agenda/Contents Slide`
  - `Bullet point slide Abstract`
  - `Empty Slide with Logo`
  - `1_Empty Slide`
  - `Thank You Slide`
- for most content pages, build a custom composition on top of a blank branded canvas rather than forcing a weak built-in content layout
- delete the starter empty slide if it is not needed in the final deck

## Template Notes

- The original blank source deck's slide 2 is the brand color guidance reference.
- The original blank source deck's slide 4 is the default agenda reference.
- The bundled template intentionally omits those instructional/sample slides from the working starter file; the guidance is captured here and in the skill docs.
- For internal management and CEO-facing decks, prefer cover / agenda / branded blank canvases and clean custom layouts over image-heavy marketing layouts.

## Recommended Layout Mapping

| Story Need | Preferred Layout | Notes |
|-----------|------------------|-------|
| Opening claim / cover | `Cover Slide` | Default opener for executive decks. Use concise title, subtitle, and presenter metadata only if useful. |
| Agenda / contents | `Agenda/Contents Slide` | Default agenda structure unless the user explicitly wants no agenda or the deck is too short. |
| Executive summary | `Empty Slide with Logo` | Preferred default for a clean custom summary layout. |
| KPI summary / headline numbers | `Empty Slide with Logo` | Build custom stat cards rather than forcing a weak preset. |
| Data-led analysis | `Empty Slide with Logo` | Preferred default for chart + insight composition. |
| Comparison / tradeoff | `Empty Slide with Logo` or `1_Empty Slide` | Build a clean custom comparison layout matched to the narrative. |
| Timeline / roadmap / milestones | `Empty Slide with Logo` or `1_Empty Slide` | Build a custom timeline that fits the content. |
| Three to six grouped points | `Empty Slide with Logo` | Use custom cards rather than preset boxes. |
| Light abstract divider / softer content page | `Bullet point slide Abstract` | Optional variant when the built-in abstract image genuinely helps the page. |
| Closing / final slide | `Thank You Slide` | Default closer unless a summary slide works better as the final slide. |
| Fully custom content without built-in graphics | `1_Empty Slide` | Use when you want the cleanest possible canvas. |
| Fully custom content with built-in logo | `Empty Slide with Logo` | Best default canvas for custom content that still feels template-native. |

Avoid by default:
- using `Bullet point slide Abstract` as the default for dense management content
- image-heavy layouts unless they materially improve the message

## Internal Management Defaults

Prefer these first:
- `Inventus Brand Colors` as a reference slide only
- `Cover Slide`
- `Agenda/Contents Slide`
- `Bullet point slide Abstract` when a softer visual separator is actually useful
- `Empty Slide with Logo`
- `1_Empty Slide`
- `Thank You Slide`

## Practical Selection Rules

- Project schedule or milestone review:
  use `Empty Slide with Logo` or `1_Empty Slide` and build a clean custom timeline
- Executive metric snapshot:
  start with `Empty Slide with Logo` and build custom stat cards
- Risks / decisions / action owners:
  start with `Empty Slide with Logo` and build 3-4 clean cards
- Data trend with interpretation:
  start with `Empty Slide with Logo` and build a custom chart-plus-insight layout
- Short internal update:
  `Cover Slide` -> `Agenda/Contents Slide` if needed -> `Empty Slide with Logo` content pages -> `Thank You Slide`

## Common Inventus Deck Types

These are the most common presentation intents this template package should support.

### 1. Project Manager Performance Review

Typical purpose:
- show delivery ownership and execution quality
- summarize what was achieved, what was recovered, and what is still at risk
- communicate management value, not just task completion

Suggested slide flow:
- `Cover Slide`
- `Agenda/Contents Slide` if the deck is more than a few slides
- `Empty Slide with Logo` for KPI summary
- `Empty Slide with Logo` for major contributions / achievements / interventions
- `Empty Slide with Logo` for management takeaway
- `Thank You Slide`

Recommended content areas:
- milestone delivery performance
- issue closure / risk reduction
- cross-functional coordination
- supplier / stakeholder management
- schedule recovery or decision-making impact

### 2. Project Progress Review

Typical purpose:
- report program status clearly across the major workstreams
- show schedule, blockers, decisions, and next steps
- keep management attention on the few items that matter most

Suggested slide flow:
- `Cover Slide`
- `Agenda/Contents Slide`
- `Empty Slide with Logo` for executive readout
- `Empty Slide with Logo` or `1_Empty Slide` for master schedule / milestone timeline
- `Empty Slide with Logo` for module-by-module progress
- `Empty Slide with Logo` for key metrics / risks / actions
- `Thank You Slide`

Core modules usually expected:
- hardware
- software
- mechanical / structure
- quality / validation
- certification / regulatory
- packaging
- accessories

Other modules worth considering depending on the program:
- supply chain / material readiness
- sourcing / vendor status
- manufacturing / factory readiness
- cost / BOM / margin impact
- testing / reliability
- operations / launch readiness

### 3. Memory Supply Situation Analysis

Typical purpose:
- explain market movement, supply constraints, pricing trend, and business impact
- help management make sourcing, pricing, or inventory decisions

Suggested slide flow:
- `Cover Slide`
- `Agenda/Contents Slide` if needed
- `Empty Slide with Logo` for price trend / allocation trend / forecast
- `Empty Slide with Logo` for insights, implications, and risks
- `Empty Slide with Logo` for decision recommendation
- `Thank You Slide`

Preferred storytelling pattern:
- market fact
- implication to Inventus
- near-term scenario
- recommended action

### 4. Process Optimization / Before-After Review

Typical purpose:
- show how the old process worked
- explain what changed
- quantify the improvement after optimization

Suggested slide flow:
- `Cover Slide`
- `Agenda/Contents Slide` if needed
- `Empty Slide with Logo` for pain points in the previous process
- `1_Empty Slide` or `Empty Slide with Logo` for process flow / comparison visual
- `Empty Slide with Logo` for before-vs-after metrics
- `Empty Slide with Logo` for management takeaway and next rollout step
- `Thank You Slide`

Preferred evidence types:
- cycle time reduction
- fewer escalations / defects / delays
- improved decision speed
- clearer ownership or reduced handoff waste

## Content Prioritization Guidance

For these deck types, the default audience is internal management.
That means:
- start with status, impact, and decision relevance
- keep decorative imagery to a minimum
- prefer clean executive summaries, timelines, number cards, and chart-led slides
- use image-heavy layouts only when the visual materially improves understanding

## Default Deck Flows

These flows are the default starting structures for the four most common Inventus presentation types.
They are intentionally simple, reusable, and management-friendly.

### A. Project Manager Performance Review

Recommended default flow:
1. `Cover Slide`
2. `Agenda/Contents Slide` if needed
3. `Empty Slide with Logo` for KPI snapshot
4. `Empty Slide with Logo` for key contributions / ownership / interventions
5. `Empty Slide with Logo` for risks handled / decisions enabled / recoveries made
6. `Empty Slide with Logo` for management takeaway
7. `Thank You Slide`

Suggested narrative:
- what was delivered
- where PM ownership changed the outcome
- what risks were controlled or reduced
- what management should remember about performance

### B. Project Progress Review

Recommended default flow:
1. `Cover Slide`
2. `Agenda/Contents Slide`
3. `Empty Slide with Logo` for executive status
4. `Empty Slide with Logo` or `1_Empty Slide` for program timeline / milestone path
5. `Empty Slide with Logo` for module progress
6. `Empty Slide with Logo` for risks / actions / metrics
7. `Thank You Slide`

Suggested narrative:
- overall status
- milestone path
- module-by-module progress
- top risks / support needed / next actions

Typical module grouping:
- hardware
- software
- mechanical / structure
- quality / validation
- certification / regulatory
- packaging
- accessories
- optional: supply chain / sourcing / factory / cost / testing / launch readiness

### C. Memory Supply Situation Analysis

Recommended default flow:
1. `Cover Slide`
2. `Agenda/Contents Slide` if needed
3. `Empty Slide with Logo` for market trend / price movement / allocation view
4. `Empty Slide with Logo` for implications, risks, and scenarios
5. `Empty Slide with Logo` for recommendation / decision framing
6. `Thank You Slide`

Suggested narrative:
- what changed in the market
- why it matters to Inventus
- likely next scenario
- what action management should consider

### D. Process Optimization / Before-After Review

Recommended default flow:
1. `Cover Slide`
2. `Agenda/Contents Slide` if needed
3. `Empty Slide with Logo` for old-process pain points
4. `1_Empty Slide` or `Empty Slide with Logo` for before / after process comparison
5. `Empty Slide with Logo` for quantified results
6. `Empty Slide with Logo` for rollout recommendation / next-step decision
7. `Thank You Slide`

Suggested narrative:
- what was wrong before
- what changed
- what improved
- what should be standardized next

## Flow Selection Rule

When the user's request clearly matches one of the four common deck types above:
- start from the corresponding default flow
- trim or expand the flow based on deck length and content availability
- only deviate when the user's material clearly needs a different structure

If the request does not clearly match one of the four patterns:
- build a custom flow using the same management-first principles
- still prefer the template as a style carrier, but use custom composition on branded blank canvases before relying on weak built-in content layouts

## What Not To Do

- Do not manually paste the Inventus logo if the chosen layout already contains it.
- Do not rebuild the theme colors by hand when working from the bundled template.
- Do not default to image-heavy layouts for internal management updates.
- Do not keep the starter empty slide in the final deck unless it was intentionally used.
