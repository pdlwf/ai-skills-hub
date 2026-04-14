# Date Cases

## Purpose

This file captures the kinds of spreadsheet date values the skill should understand.

## Clean Full Dates

- `2026-03-20`
- `2026/03/20`
- `2026.03.20`
- `20 Mar 2026`
- `March 20, 2026`

Expected behavior:

- normalize to `YYYY-MM-DD`
- granularity = `day`

## Partial Dates

- `2026-03`
- `Mar 2026`
- `2026 Q1`
- `2026`

Expected behavior:

- preserve partial precision
- do not invent missing month or day values
- use granularity metadata such as `month`, `quarter`, or `year`

## Date Ranges With Omitted Repeated Parts

- `2026/7/23-30`
- `2026/7/23～30`
- `2026/7/23--30`

Expected behavior:

- interpret as a date range, not a single date
- recognize multiple range separators, not only `-`
- use the left side as the anchor
- inherit omitted repeated parts on the right side from the left side
- normalize to:
  - start = `2026-07-23`
  - end = `2026-07-30`
- granularity = `day-range`

Interpretation logic:

- left side provides full context: year = `2026`, month = `07`, day = `23`
- right side only provides `30`
- the separator may be `-`, `～`, `--`, or other recognized range markers
- because only the day is present on the right side, inherit year and month from the left side
- resulting meaning: start on `2026-07-23`, end on `2026-07-30`

Separator handling rule:

- first detect whether a symbol is acting as a range separator rather than part of one date token
- normalize recognized separators into one internal `range` concept before parsing
- initial supported separators should include:
  - `-`
  - `--`
  - `~`
  - `～`
  - `to`

Suggested rule name:

- `range_separator_normalization`

Suggested output:

```json
{
  "original_value": "2026/7/23-30",
  "interpreted_value": {
    "start": "2026-07-23",
    "end": "2026-07-30"
  },
  "source_layer": "cell_text",
  "output_type": "date_range",
  "granularity": "day-range",
  "confidence": "high",
  "anomaly_flag": false,
  "anomaly_reason": null,
  "warning": null,
  "reason": "The right side omits year and month, so it inherits them from the left-side anchor date."
}
```

Edge case:

- if the separator appears inside a single date token rather than between two date expressions, do not treat it as a range automatically

## Human-Understandable But Messy

- `Mar 20th`
- ` 2026 / 3 / 20 `
- `2026年3月20日`
- `20-Mar-26`
- `20260320`

Expected behavior:

- normalize when interpretation is strong
- keep a confidence level
- preserve the original raw value

## Ambiguous Cases

- `03/04/2026`
- `04/03/26`
- `03/04/05`
- `20/03`

Expected behavior:

- do not silently guess without a locale rule or surrounding context
- mark as ambiguous when needed
- expose a warning

## Excel-Specific Cases

- Excel serial dates such as `45371`
- cells formatted as dates but stored as numbers
- cells displayed as dates but underlying formula returns a serial number

Expected behavior:

- inspect both stored value and visible formatting when relevant
- convert serial dates correctly
- avoid treating plain numbers as dates without evidence

## Suggested Output Fields

- `original_value`
- `interpreted_value`
- `source_layer`
- `output_type`
- `granularity`
- `confidence`
- `anomaly_flag`
- `anomaly_reason`
- `warning`
