# AI Skills Context
_Auto-generated 2026-04-14 14:02 — paste into Claude chat to load all skills_

## create-plan
_Turn a user prompt into a single, actionable coding task plan. Use when the user explicitly asks for a plan related to a coding task._

```
---
name: create-plan
description: Create a concise plan. Use when a user explicitly asks for a plan related to a coding task.
metadata:
  short-description: Create a plan
---

# Create Plan

## Goal

Turn a user prompt into a **single, actionable plan** delivered in the final assistant message.

## Minimal workflow

Throughout the entire workflow, operate in read-only mode. Do not write or update files.

1. **Scan context quickly**
   - Read `README.md` and any obvious docs (`docs/`, `CONTRIBUTING.md`, `ARCHITECTURE.md`).
   - Skim relevant files (the ones most likely touched).
   - Identify constraints (language, frameworks, CI/test commands, deployment shape).

2. **Ask follow-ups only if blocking**
   - Ask **at most 1–2 questions**.
   - Only ask if you cannot responsibly plan without the answer; prefer multiple-choice.
   - If unsure but not blocked, make a reasonable assumption and proceed.

3. **Create a plan using the template below**
   - Start with **1 short paragraph** describing the intent and approach.
   - Clearly call out what is **in scope** and what is **not in scope** in short.
```

## docx
_Create, edit, and analyze Word documents (.docx). Supports tracked changes, redlining, raw XML editing, text extraction, and document-to-image conversion._

```
---
name: docx
description: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks"
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX creation, editing, and analysis

## Overview

A user may ask you to create, edit, or analyze the contents of a .docx file. A .docx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks.

## Workflow Decision Tree

### Reading/Analyzing Content
Use "Text extraction" or "Raw XML access" sections below

### Creating New Document
Use "Creating a new Word document" workflow

### Editing Existing Document
- **Your own document + simple changes**
  Use "Basic OOXML editing" workflow

- **Someone else's document**
  Use **"Redlining workflow"** (recommended default)

- **Legal, academic, business, or government docs**
  Use **"Redlining workflow"** (required)

```

## excel-date-understanding
_Interpret messy schedule dates in spreadsheets — normalize values, recover task hierarchy, extract note-embedded dates, detect anomalies, and produce structured project-date facts. Depends on xlsx skill for workbook I/O._

```
---
name: excel-date-understanding
description: Use when working with spreadsheet files that contain project schedule dates needing semantic interpretation, normalization, hierarchy recovery, note extraction, conditional-format logic extraction, and row-level date analysis. This skill depends on `xlsx` for workbook access and modification.
---

# Excel Date Understanding

## Use This Skill When

Use this skill when the user is working with spreadsheet schedules and needs help to:

- understand messy date columns
- normalize inconsistent date values
- parse date ranges
- extract dates from note text
- recover parent-child task hierarchy from merged cells
- interpret note columns such as `remark`, `update`, or `feedback`
- interpret conditional formatting tied to schedule status
- extract structured project-date facts
- derive row-level date analysis such as overdue, due soon, or completed late
- compare the same logical task across multiple scenario sheets
- detect suspicious but parseable schedule dates

Do not use this skill for spreadsheet work that is purely mechanical and does not depend on date semantics. Use the built-in `xlsx` skill alone for that when available.

## Dependency

This skill sits above the built-in `xlsx` skill.

- `xlsx` handles workbook I/O, formatting, formulas, merged-cell metadata, and conditional-format definitions
```

## frontend-slides
_Create distinctive HTML presentations from scratch or by converting PowerPoint decks to web slides._

```
---
name: frontend-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
origin: ECC
---

# Frontend Slides

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser.

Inspired by the visual exploration approach showcased in work by [zarazhangrui](https://github.com/zarazhangrui).

## When to Activate

- Creating a talk deck, pitch deck, workshop deck, or internal presentation
- Converting `.ppt` or `.pptx` slides into an HTML presentation
- Improving an existing HTML presentation's layout, motion, or typography
- Exploring presentation styles with a user who does not know their design preference yet

## Non-Negotiables

1. **Zero dependencies**: default to one self-contained HTML file with inline CSS and JS.
2. **Viewport fit is mandatory**: every slide must fit inside one viewport with no internal scrolling.
3. **Show, don't tell**: use visual previews instead of abstract style questionnaires.
4. **Distinctive design**: avoid generic purple-gradient, Inter-on-white, template-looking decks.
5. **Production quality**: keep code commented, accessible, responsive, and performant.

Before generating, read `STYLE_PRESETS.md` for the viewport-safe CSS base, density limits, preset catalog, and CSS gotchas.

## Workflow
```

## pdf
_Comprehensive PDF manipulation — extract text and tables, create new PDFs, merge/split documents, OCR scanned pages, fill forms, add watermarks, and encrypt files._

```
---
name: pdf
description: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations
```

## personalized-coding-framework
_Global coding governance layer. Captures explicit and implicit preferences across sessions, synthesizes them into principles and guardrails, resolves conflicts, and conditions every coding output accordingly._

```
---
name: personalized-coding-framework
description: Global coding governance layer that applies the user’s programming constitution to every coding task. Use for any coding project work (planning, architecture, implementation, refactor, debugging, testing, reviews, and technical writing) to infer or update principles from explicit intent plus interaction signals, resolve preference conflicts, and condition decisions with the current framework.
---

# Personalized Coding Framework

## Operating Goal

Build and maintain a living abstraction layer that governs coding decisions across projects.
Fuse explicit user statements with revealed preferences from interaction outcomes.

## Trigger Conditions

Activate this skill when any of the following occurs:
- Any coding-related task begins and user governance should be applied by default.
- The user states preferences, constraints, or principles.
- The user accepts, rejects, or refines a technical proposal.
- The user asks to update, remove, compare, or inspect preferences.
- A new project starts and top-level governance should be applied.

## Core Workflow

0. Load Persistent State
- Open `state/framework-state.yaml` in this skill folder at the start of each coding task.
- If the file is missing, initialize it from `references/framework-schema.md` defaults.

1. Ingest Signals
- Extract explicit preferences from phrases such as `I want`, `I prefer`, `do not`, `must`, `should`, and equivalents in Chinese (`我希望`, `我不想`, `必须`, `不要`).
- Capture implicit signals from outcomes such as accept/reject, revision depth, and user pushback direction.
```

## playwright
_Automate a real browser from the terminal using playwright-cli — navigation, form filling, snapshots, screenshots, data extraction, and UI-flow debugging. CLI-first, no test spec needed._

```
---
name: "playwright"
description: "Use when the task requires automating a real browser from the terminal (navigation, form filling, snapshots, screenshots, data extraction, UI-flow debugging) via `playwright-cli` or the bundled wrapper script."
---


# Playwright CLI Skill

Drive a real browser from the terminal using `playwright-cli`. Prefer the bundled wrapper script so the CLI works even when it is not globally installed.
Treat this skill as CLI-first automation. Do not pivot to `@playwright/test` unless the user explicitly asks for test files.

## Prerequisite check (required)

Before proposing commands, check whether `npx` is available (the wrapper depends on it):

```bash
command -v npx >/dev/null 2>&1
```

If it is not available, pause and ask the user to install Node.js/npm (which provides `npx`). Provide these steps verbatim:

```bash
# Verify Node/npm are installed
node --version
npm --version

# If missing, install Node.js/npm, then:
npm install -g @playwright/cli@latest
playwright-cli --help
```
```

## pptx
_Create, edit, and analyze PowerPoint presentations (.pptx). Supports scratch creation via html2pptx, template-based workflows, OOXML editing, thumbnail generation, and slide-to-image conversion._

```
---
name: pptx
description: "Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks"
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX creation, editing, and analysis

## Overview

A user may ask you to create, edit, or analyze the contents of a .pptx file. A .pptx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks.

## Reading and analyzing content

### Text extraction
If you just need to read the text contents of a presentation, you should convert the document to markdown:

```bash
# Convert document to markdown
python -m markitdown path-to-file.pptx
```

### Raw XML access
You need raw XML access for: comments, speaker notes, slide layouts, animations, design elements, and complex formatting. For any of these features, you'll need to unpack a presentation and read its raw XML contents.

#### Unpacking a file
`python ooxml/scripts/unpack.py <office_file> <output_dir>`

**Note**: The unpack.py script is located at `skills/pptx/ooxml/scripts/unpack.py` relative to the project root. If the script doesn't exist at this path, use `find . -name "unpack.py"` to locate it.

```

## xlsx
_Create, edit, and analyze spreadsheets (.xlsx, .xlsm, .csv). Supports formulas with zero-error guarantees, financial model color-coding, openpyxl/pandas workflows, and formula recalculation via LibreOffice._

```
---
name: xlsx
description: "Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas"
license: Proprietary. LICENSE.txt has complete terms
---

# Requirements for Outputs

## All Excel files

### Zero Formula Errors
- Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)

### Preserve Existing Templates (when updating templates)
- Study and EXACTLY match existing format, style, and conventions when modifying files
- Never impose standardized formatting on files with established patterns
- Existing template conventions ALWAYS override these guidelines

## Financial models

### Color Coding Standards
Unless otherwise stated by the user or existing template

#### Industry-Standard Color Conventions
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within same workbook
- **Red text (RGB: 255,0,0)**: External links to other files
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated

```
