# AI Knowledge OS Notion Map

Use this reference only when a task needs exact Notion destinations, properties, or page IDs.

This reference is global for supported AI tools. It can be used from any project; do not assume the active workspace is the Obsidian vault.

## Core Pages

- AI Knowledge OS root: `34d2b57a7982811d9cd5f4639b0b3b58`
- Operating Manual: `34d2b57a798281bd894ef1e6900fce58`
- AI Knowledge OS Writing Rule: `34d2b57a7982811b95c1e5a55b9bf9ba`
- Cross-Tool Capture Protocol: `34d2b57a79828175af77c85523fba4dd`
- Conversation Extraction Prompt: `34d2b57a798281e28dd4f8a01323a316`
- Module Reference Map: `34d2b57a79828151bb20e48c776ef536`
- Identity & Preferences: `34d2b57a7982817f9ec1d438fa8927f7`
- Thinking Models: `34d2b57a798281748e85de991ef6dacc`
- AI Workflow: `34d2b57a798281129346f979460c8d03`
- Migration Rules - Notion to Obsidian: `34d2b57a7982814bacb5f1e2f98c3a21`
- Google Drive File Index ID: `1qaxC31EDlCcv-pGuMVEpECftk4QrbX5A0576WDP2_xA`

## Data Sources

Multi-select properties are SQLite text fields in this connector. Pass them as JSON array strings, for example `"[\"AI Workflow\",\"Prompt Library\"]"`, not as native JSON arrays.

Use the current assistant as the source tool in page body metadata: `Codex`, `Claude`, `Claude Code`, `ChatGPT`, or another explicit tool name. For database select properties, fetch the live schema first and use the closest allowed option.

### Inbox / Review Queue

- Data source: `collection://d7045b40-3fd8-4b37-b34b-da66a50c12fd`
- Use for: temporary capture, uncertain value, draft prompts, draft workflows, draft skill candidates.
- Title property: `Name`
- Common properties:
  - `Status`: `Inbox`, `Reviewing`, `Archived`, `Discarded`
  - `Type`: `Conversation`, `Idea`, `Decision`, `Asset`, `Project Note`
  - `Output Type`: `Idea Discussion`, `Workflow`, `Prompt`, `Template`, `Skill`, `Project Record`
  - `Destination`: JSON array string using `Conversation Digest`, `Identity & Preferences`, `Reusable Assets`, `Project Knowledge`, `Thinking Models`, `AI Workflow`, `Prompt Library`, `Migration Rules`
  - `Tool`: use the current tool name when the live schema allows it
  - `Source`: use `Manual` unless a better source option exists
  - `Tags`: JSON array string; usually include `knowledge-os` and optionally `ai-workflow`, `prompt`, `personal-memory`, `project-management`
  - `Session ID`: text
  - `Session Link`: URL
  - `date:Created Date:start`: ISO date
  - `date:Created Date:is_datetime`: `0`

### Conversation Digest

- Data source: `collection://51992f37-832c-4036-8975-e9e0b745798b`
- Use for: approved conversation-level reusable records and incremental digest updates.
- Title property: `Name`
- Common properties:
  - `Save Decision`: `Save`, `Review Later`, `Discard`
  - `Output Type`: `Idea Discussion`, `Workflow`, `Prompt`, `Template`, `Skill`, `Project Record`
  - `Main Area`: `AI Workflow`, `Project Management`, `Learning`, `Family`, `Personal System`
  - `Tool`: use the current tool name when the live schema allows it
  - `Source`: use `Manual` unless a better source option exists
  - `Tags`: JSON array string using `knowledge-os`, `ai-workflow`, `notion`, `obsidian`, `personal-memory`, `project-management`
  - `Session ID`: text
  - `Session Link`: URL
  - `date:Date:start`: ISO date
  - `date:Date:is_datetime`: `0`

### Prompt Library

- Data source: `collection://ca0a562b-a108-42f7-b726-89a43e76db4f`
- Use for: approved reusable prompts and system-level prompt rules.
- Title property: `Name`
- Common properties:
  - `Status`: `Draft`, `Useful`, `Proven`, `Deprecated`
  - `Prompt Type`: `Thinking`, `Extraction`, `Workflow`, `Report`, `Coding`, `Review`, `Meeting`
  - `Scenario`: `Idea Discussion`, `Knowledge Extraction`, `Workflow Design`, `Report Template`, `Skill Creation`, `Project Management`
  - `Execution Mode`: `Extract Only`, `Draft Then Approve`, `Write After Approval`, `Auto Write`
  - `Approval Required`: `__YES__` or `__NO__`
  - `Target Tool`: JSON array string using `Codex`, `Claude`, or another supported tool when relevant and allowed by schema
  - `Tags`: JSON array string using `knowledge-os`, `prompt`, `workflow`, `cursor`, `claude`, `chatgpt`, `codeium`
  - `Related Pages`: text
  - `Related Rules`: text
  - `Source Session ID`: text
  - `Source Session Link`: URL

### Reusable Assets

- Data source: `collection://823476d6-3711-42e2-9be8-776c2fc912ba`
- Use for: approved templates, checklists, frameworks, report structures, and reusable non-prompt assets.
- Title property: `Name`
- Common properties:
  - `Status`: `Draft`, `Useful`, `Proven`, `Deprecated`
  - `Asset Type`: `Prompt`, `Template`, `Checklist`, `Framework`, `Report Structure`, `Email Copy`
  - `Scenario`: `AI Workflow`, `Project Management`, `Reporting`, `Learning`, `Family`, `Coding`
  - `Tags`: JSON array string using `codex`, `claude`, `chatgpt`, `prompt`, `presentation`, `mom`
  - `date:Last Used:start`: ISO date when applicable
  - `date:Last Used:is_datetime`: `0`

### Project Knowledge

- Data source: `collection://f98acc41-eec9-499a-92ba-2c041e2d4853`
- Use for: approved project-specific decisions, risks, issues, requirements, conclusions, and next actions.
- Title property: `Name`
- Common properties:
  - `Project`: `PD1`, `SD1`, `SL`, `AI System`, `General PM`
  - `Type`: `Risk`, `Decision`, `Issue`, `Requirement`, `Meeting Conclusion`, `Next Action`
  - `Status`: `Open`, `Tracking`, `Closed`, `Reference`
  - `Tags`: JSON array string using `odm`, `risk`, `decision`, `schedule`, `reporting`, `tooling`
  - `Owner`: text
  - `date:Date:start`: ISO date
  - `date:Date:is_datetime`: `0`

## Default Draft Record Body

Use this structure for Inbox drafts and approval previews:

```markdown
## Context

## Key Insight

## Decision / Conclusion

## Reasoning

## Reusable Value

## Related Areas

## Next Action

---
type:
status:
tags:
created:
updated:
source_tool:
source_project:
workspace_path:
session_link:
session_id:
notion_destination:
approval_status:
related_drive_file:
related_github_repo:
related_prompt:
related_workflow:
```

## Drift Handling

This map was derived from the Notion workspace on 2026-04-25. Before writing, fetch the target page or data source and trust the live schema over this file.
