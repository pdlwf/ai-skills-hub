#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"

REQUIRED_FILES = [
    ROOT / "SKILL.md",
    REFERENCES / "rule-schema.md",
    REFERENCES / "rule-library.md",
    REFERENCES / "workbook-findings.md",
    REFERENCES / "project-date-fact-schema.md",
    REFERENCES / "derived-date-analysis-schema.md",
    REFERENCES / "cross-scenario-comparison-schema.md",
    REFERENCES / "schedule-anomaly-schema.md",
    REFERENCES / "worked-examples.md",
    REFERENCES / "maintenance-and-learning.md",
    REFERENCES / "update-log.md",
]

ALLOWED_RULE_CATEGORIES = {
    "single_date",
    "date_range",
    "partial_date",
    "date_text_extraction",
    "excel_serial_date",
    "date_detection",
    "ambiguity_resolution",
    "anomaly_detection",
    "conditional_format_signal",
    "scenario_comparison",
    "state_token",
}

FACT_REQUIRED = {
    "sheet",
    "row",
    "parent_item",
    "task_key",
    "task",
    "owner",
    "planned_date",
    "actual_date",
    "date_status",
    "source_signals",
}

FACT_DATE_STATUS = {
    "done",
    "completed_late",
    "upcoming",
    "overdue",
    "in_progress_or_delayed",
    "unresolved",
}

FACT_SOURCE_SIGNALS = {
    "cell_value",
    "cell_text",
    "display_format",
    "conditional_formatting",
    "status_text",
    "merged_hierarchy",
    "neighboring_context",
}

ANALYSIS_REQUIRED = {
    "sheet",
    "row",
    "task",
    "analysis_date",
    "due_soon_window_days",
    "window_source",
    "derived_status",
    "days_to_due",
    "days_overdue",
    "slip_days",
    "analysis_signals",
}

DERIVED_STATUS = {
    "done_on_time",
    "completed_late",
    "upcoming",
    "upcoming_due_soon",
    "overdue",
    "delayed_in_progress",
    "unresolved",
}

WINDOW_SOURCES = {"workbook_rule", "user_input", "skill_default"}

ANALYSIS_SIGNALS = {
    "planned_date",
    "actual_date",
    "actual_date_blank",
    "conditional_format_due_soon",
    "conditional_format_delay",
    "status_text_manageable",
    "note_push_out",
    "note_completion",
    "neighboring_context",
}

COMPARISON_REQUIRED = {
    "task_key",
    "task",
    "comparison_type",
    "compared_sheets",
    "scenario_values",
    "match_confidence",
    "warning",
}

ANOMALY_REQUIRED = {
    "anomaly_id",
    "rule_id",
    "sheet",
    "row",
    "cell_ref",
    "severity",
    "confidence",
    "suspected_issue",
    "interpreted_value",
    "evidence",
    "suggested_check",
}

LEVELS = {"low", "medium", "high"}


def fail(message: str) -> None:
    ERRORS.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


def parse_json_blocks(path: Path):
    text = path.read_text()
    blocks = re.findall(r"```json\n(.*?)\n```", text, flags=re.S)
    out = []
    for idx, block in enumerate(blocks, 1):
        try:
            out.append(json.loads(block))
        except json.JSONDecodeError as exc:
            fail(f"{path.name}: invalid JSON block #{idx}: {exc}")
    return out


def classify(block):
    if "date_status" in block:
        return "fact"
    if "derived_status" in block:
        return "analysis"
    if "comparison_type" in block:
        return "comparison"
    if "anomaly_id" in block:
        return "anomaly"
    return "unknown"


def validate_fact(obj, label):
    missing = FACT_REQUIRED - set(obj)
    if missing:
        fail(f"{label}: missing fact fields {sorted(missing)}")
    if obj.get("date_status") not in FACT_DATE_STATUS:
        fail(f"{label}: invalid fact date_status {obj.get('date_status')!r}")
    for signal in obj.get("source_signals", []):
        if signal not in FACT_SOURCE_SIGNALS:
            fail(f"{label}: invalid source_signal {signal!r}")


def validate_analysis(obj, label):
    missing = ANALYSIS_REQUIRED - set(obj)
    if missing:
        fail(f"{label}: missing analysis fields {sorted(missing)}")
    if obj.get("derived_status") not in DERIVED_STATUS:
        fail(f"{label}: invalid derived_status {obj.get('derived_status')!r}")
    if obj.get("window_source") not in WINDOW_SOURCES:
        fail(f"{label}: invalid window_source {obj.get('window_source')!r}")
    for signal in obj.get("analysis_signals", []):
        if signal not in ANALYSIS_SIGNALS:
            fail(f"{label}: invalid analysis_signal {signal!r}")


def validate_comparison(obj, label):
    missing = COMPARISON_REQUIRED - set(obj)
    if missing:
        fail(f"{label}: missing comparison fields {sorted(missing)}")
    if obj.get("match_confidence") not in LEVELS:
        fail(f"{label}: invalid match_confidence {obj.get('match_confidence')!r}")


def validate_anomaly(obj, label):
    missing = ANOMALY_REQUIRED - set(obj)
    if missing:
        fail(f"{label}: missing anomaly fields {sorted(missing)}")
    if obj.get("severity") not in LEVELS:
        fail(f"{label}: invalid severity {obj.get('severity')!r}")
    if obj.get("confidence") not in LEVELS:
        fail(f"{label}: invalid confidence {obj.get('confidence')!r}")
    if obj.get("rule_id") not in RULE_IDS:
        fail(f"{label}: unknown anomaly rule_id {obj.get('rule_id')!r}")


def validate_rule_categories():
    text = (REFERENCES / "rule-library.md").read_text()
    categories = re.findall(r"`rule_category`: `([^`]+)`", text)
    for category in categories:
        if category not in ALLOWED_RULE_CATEGORIES:
            fail(f"rule-library.md: unsupported rule_category {category!r}")
    return set(re.findall(r"`rule_id`: `([^`]+)`", text))


def validate_maintenance_paths():
    text = (REFERENCES / "maintenance-and-learning.md").read_text()
    numbered = re.findall(r"`\d{2}-[^`]+`", text)
    for token in numbered:
        fail(f"maintenance-and-learning.md: obsolete numbered path reference {token}")


ERRORS = []
WARNINGS = []

for required in REQUIRED_FILES:
    if not required.exists():
        fail(f"missing required file: {required}")

RULE_IDS = validate_rule_categories()
validate_maintenance_paths()

for idx, block in enumerate(parse_json_blocks(REFERENCES / "worked-examples.md"), 1):
    kind = classify(block)
    label = f"worked-examples.md block #{idx}"
    if kind == "fact":
        validate_fact(block, label)
    elif kind == "analysis":
        validate_analysis(block, label)
    elif kind == "comparison":
        validate_comparison(block, label)
    elif kind == "anomaly":
        validate_anomaly(block, label)
    else:
        warn(f"{label}: unclassified JSON block")

if WARNINGS:
    print("WARNINGS:")
    for item in WARNINGS:
        print(f"- {item}")

if ERRORS:
    print("ERRORS:")
    for item in ERRORS:
        print(f"- {item}")
    sys.exit(1)

print("Skill validation passed.")
