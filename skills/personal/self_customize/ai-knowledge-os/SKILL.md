---
name: ai-knowledge-os
description: Route reusable AI work, decisions, prompts, workflows, and conversation digests into Bobby's Notion AI Knowledge OS across Codex and Claude.
metadata:
  short-description: Route reusable AI work into Notion
---

# AI Knowledge OS

Use this skill to interact with Bobby's Notion-based Personal AI Knowledge OS from any supported AI tool.

The system is not a raw chat archive. It captures reusable knowledge that can influence future decisions, workflows, prompts, project management, and AI collaboration.

## Scope

This is a cross-tool skill. It is not owned by a single repo, Obsidian vault, local assistant, or project workspace.

Use it when a result should become reusable memory or a Notion knowledge record. Project-specific work should keep its execution artifacts in that project, then capture only the reusable summary, decision, workflow, or reference link in Notion.

## Distribution Model

This skill folder is the canonical source. Tool-specific locations should point to this folder or be generated from it:

- Codex: symlink from `~/.codex/skills/ai-knowledge-os` to this folder.
- Claude Code: symlink from the relevant `.claude/skills/ai-knowledge-os` to this folder.
- Claude App / Cloud: upload a packaged `.skill` or `.zip` generated from this folder.

Do not maintain copied edits in Codex, Claude, or package-output folders. Regenerate tool-specific outputs after changing this source.

## Quick Start

1. Decide whether the content passes the save filter.
2. Fetch the AI Knowledge OS Operating Manual and relevant destination schema.
3. Route each extracted item to the correct module.
4. Write temporary drafts to Inbox / Review Queue when allowed.
5. Draft formal records for user approval before writing to long-term modules.
6. Return the destination, Notion links, and any follow-up review needed.

For page IDs, database IDs, property names, and default property values, read `references/notion-map.md`.

## When To Trigger

Trigger this skill when the user asks to:

- save, record, log, archive, capture, or write something into Notion;
- extract reusable knowledge from a conversation;
- update the AI Knowledge OS, Conversation Digest, Prompt Library, Reusable Assets, Project Knowledge, Identity & Preferences, Thinking Models, AI Workflow, or Inbox / Review Queue;
- turn an AI workflow, prompt, checklist, template, skill, project decision, or implementation pattern into a reusable knowledge record;
- finish substantial repo, website, document, spreadsheet, browser, Gmail, Drive, or automation work that produced reusable decisions or process knowledge;
- inspect or maintain the Notion AI Knowledge OS structure.

Soft-trigger this skill at the end of substantial work when the output clearly creates reusable system knowledge. In that case, mention the suggested capture briefly or write only to Inbox / Review Queue if the user has already established auto-draft capture for the current task.

Do not trigger for ordinary status updates, transient debugging noise, raw chat logs, secrets, credentials, or content that does not pass the save filter.

## Project Context

When used from another project, include enough context for future retrieval:

- project name or workspace path;
- repo URL, branch, commit, PR, or local file path when relevant;
- related Google Drive file, Notion page, browser target, or external URL;
- what changed, what was decided, and what should be reused later;
- what should not be preserved because it is temporary, sensitive, or too low value.

Do not copy whole source files, logs, transcripts, or raw conversations into Notion. Link to durable artifacts and summarize the reusable part.

## Save Filter

Save only if at least two are true:

- The item is likely to be reused in future work, learning, family, or AI collaboration.
- It affects a decision, working style, rule, preference, or system design.
- It can become a prompt, workflow, template, checklist, framework, skill, project record, or long-term memory.

If value is uncertain but plausible, route to Inbox / Review Queue as a draft.

## Source Of Truth

Before writing or making routing decisions, fetch these Notion pages when relevant:

- AI Knowledge OS root page
- AI Knowledge OS Operating Manual
- AI Knowledge OS Writing Rule
- Cross-Tool Capture Protocol
- AI Knowledge OS Module Reference Map

If a local reference in this skill conflicts with freshly fetched Notion content, trust the freshly fetched Notion content and mention the drift.

## Routing Rules

Route by content type:

- Conversation-level reusable summary -> Conversation Digest
- Uncertain extracted item -> Inbox / Review Queue
- Prompt body or prompt update -> Prompt Library
- Template, checklist, framework, report structure -> Reusable Assets
- Project decision, risk, issue, requirement, meeting conclusion, action -> Project Knowledge
- Stable user preference, constraint, role context, working style -> Identity & Preferences
- Reusable reasoning model -> Thinking Models
- Cross-tool process, automation workflow, tool cooperation rule -> AI Workflow
- Markdown or Obsidian migration concern -> Migration Rules - Notion to Obsidian
- PPT, Excel, PDF, Google Doc, Sheet, Slide, report, or attachment -> Google Drive, then link from Notion
- Code, script, repo automation, implementation history -> GitHub or local repo, then link from Notion if reusable

If an item belongs in multiple modules, update or draft all relevant modules rather than forcing a single destination.

## Approval Rules

Temporary capture can be written without repeated approval when the item passes the save filter:

- Inbox / Review Queue items
- Draft prompt candidates
- Draft workflow candidates
- Draft skill candidates
- Draft templates or checklists
- Incremental extraction updates
- File reference records

Formal archive or promotion requires user approval before writing to long-term destinations:

- Conversation Digest
- Prompt Library
- Reusable Assets
- Project Knowledge
- Identity & Preferences
- Thinking Models
- AI Workflow
- Migration Rules
- final system rules or proven prompts

When approval is required, show the proposed record and target destination first. After approval, write it to Notion and return the Notion link.

## Incremental Extraction

Within the same conversation:

1. Do not re-extract from the beginning.
2. Identify the previous extraction point, existing Conversation Digest, or Session ID.
3. Extract only new content since the last extraction.
4. Update the existing digest or related records instead of creating duplicates.
5. Preserve the same Session ID unless the user starts a new thread or project.

Use the Session ID format:

```text
YYYY-MM-DD_tool_topic_shortname
```

Examples:

```text
2026-04-25_codex_ai-knowledge-os-skill
2026-04-25_claude_ai-knowledge-os-skill
```

## Standard Inputs

Collect or infer:

- source material: current conversation, pasted notes, Notion page, local file, repo result, Drive file, or GitHub link;
- source tool: Codex, Claude, Claude Code, ChatGPT, or another explicit tool name;
- source project or workspace;
- session link if available;
- session ID;
- date;
- target audience;
- intended destination when explicit;
- whether this is draft capture or formal archive.

## Standard Output

When writing or drafting, produce:

- destination module and reason;
- record title;
- concise summary;
- context;
- key insight or decision;
- reasoning;
- reusable value;
- related areas or links;
- next action;
- metadata block with source tracking;
- project or artifact links when relevant;
- Notion page link after a successful write.

If Notion tools are unavailable, provide a Markdown fallback and clearly state that nothing was written.

## Notion Tool Workflow

1. Use Notion search/fetch to find existing related records and avoid duplicates.
2. Fetch the destination data source before creating or updating database pages.
3. Use the exact property names and allowed values from the fetched schema.
4. For updates, fetch the existing page first and use targeted content updates.
5. Never delete or replace child pages/databases without explicit user confirmation.
6. Confirm what changed and include links.

When creating or updating Notion content, follow the active Notion tool's Markdown and block-formatting requirements.

## Self Improvement

This is a `self_customize` skill. Maintain it only from the canonical folder `skills/personal/self_customize/ai-knowledge-os` in the `ai-skills-hub` repo through Codex or Claude Code.

Claude App / Claude.ai uploads are read-only release snapshots. Maintain skill changes only from the canonical repo source through Codex or Claude Code.
