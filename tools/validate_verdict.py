"""Validate a MasterCopy SPEC-00 verdict without external dependencies."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


LADDER_SOURCES = {"default", "ungoverned-agent", "governed-agent"}
VERDICTS = {"PASS", "FAIL"}
REQUIRED_TOP_LEVEL = {
    "run_id",
    "date",
    "milestone",
    "git_sha",
    "ladder_source",
    "titles",
    "totals",
    "verdict",
}
REQUIRED_TITLE = {
    "title_id",
    "content_class",
    "renditions",
    "vmaf_min",
    "delivered_bits_total",
    "mediaconvert_normalized_minutes",
    "usd_actual",
    "envelope_pass",
}
REQUIRED_RENDITION = {"rung", "vmaf", "bitrate_kbps", "codec"}
REQUIRED_TOTALS = {
    "titles_pass",
    "titles_total",
    "bits_vs_default_pct",
    "usd_vs_default_pct",
}


class VerdictValidationError(ValueError):
    """Raised when a verdict does not satisfy SPEC-00."""


def _require_keys(value: dict[str, Any], required: set[str], location: str) -> None:
    missing = sorted(required - value.keys())
    if missing:
        raise VerdictValidationError(
            f"{location} is missing required fields: {', '.join(missing)}"
        )


def _number(value: Any, location: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise VerdictValidationError(f"{location} must be a number")


def validate_verdict(verdict: Any) -> None:
    if not isinstance(verdict, dict):
        raise VerdictValidationError("verdict must be a JSON object")

    _require_keys(verdict, REQUIRED_TOP_LEVEL, "verdict")
    if not isinstance(verdict["run_id"], str) or not verdict["run_id"]:
        raise VerdictValidationError("run_id must be a non-empty string")
    if not isinstance(verdict["git_sha"], str) or not verdict["git_sha"]:
        raise VerdictValidationError("git_sha must be a non-empty string")
    if not isinstance(verdict["milestone"], str) or not verdict["milestone"]:
        raise VerdictValidationError("milestone must be a non-empty string")
    try:
        date.fromisoformat(verdict["date"])
    except (TypeError, ValueError) as error:
        raise VerdictValidationError("date must use YYYY-MM-DD format") from error
    if verdict["ladder_source"] not in LADDER_SOURCES:
        raise VerdictValidationError("ladder_source is not a supported value")
    if verdict["verdict"] not in VERDICTS:
        raise VerdictValidationError("verdict must be PASS or FAIL")
    if not isinstance(verdict["titles"], list) or not verdict["titles"]:
        raise VerdictValidationError("titles must be a non-empty array")

    totals = verdict["totals"]
    if not isinstance(totals, dict):
        raise VerdictValidationError("totals must be an object")
    _require_keys(totals, REQUIRED_TOTALS, "totals")
    for field in ("titles_pass", "titles_total"):
        if not isinstance(totals[field], int) or isinstance(totals[field], bool):
            raise VerdictValidationError(f"totals.{field} must be an integer")
    for field in ("bits_vs_default_pct", "usd_vs_default_pct"):
        _number(totals[field], f"totals.{field}")

    if totals["titles_total"] != len(verdict["titles"]):
        raise VerdictValidationError("totals.titles_total must match titles length")
    if not 0 <= totals["titles_pass"] <= totals["titles_total"]:
        raise VerdictValidationError("totals.titles_pass is outside the title count")

    passing_titles = 0
    for title_index, title in enumerate(verdict["titles"]):
        location = f"titles[{title_index}]"
        if not isinstance(title, dict):
            raise VerdictValidationError(f"{location} must be an object")
        _require_keys(title, REQUIRED_TITLE, location)
        for field in ("title_id", "content_class"):
            if not isinstance(title[field], str) or not title[field]:
                raise VerdictValidationError(
                    f"{location}.{field} must be a non-empty string"
                )
        if not isinstance(title["renditions"], list) or not title["renditions"]:
            raise VerdictValidationError(f"{location}.renditions must be non-empty")
        _number(title["vmaf_min"], f"{location}.vmaf_min")
        _number(
            title["delivered_bits_total"],
            f"{location}.delivered_bits_total",
        )
        _number(
            title["mediaconvert_normalized_minutes"],
            f"{location}.mediaconvert_normalized_minutes",
        )
        _number(title["usd_actual"], f"{location}.usd_actual")
        if not isinstance(title["envelope_pass"], bool):
            raise VerdictValidationError(f"{location}.envelope_pass must be boolean")
        passing_titles += title["envelope_pass"]

        for rendition_index, rendition in enumerate(title["renditions"]):
            rendition_location = f"{location}.renditions[{rendition_index}]"
            if not isinstance(rendition, dict):
                raise VerdictValidationError(f"{rendition_location} must be an object")
            _require_keys(rendition, REQUIRED_RENDITION, rendition_location)
            _number(rendition["vmaf"], f"{rendition_location}.vmaf")
            _number(
                rendition["bitrate_kbps"],
                f"{rendition_location}.bitrate_kbps",
            )
            if not all(isinstance(rendition[field], str) and rendition[field] for field in ("rung", "codec")):
                raise VerdictValidationError(
                    f"{rendition_location}.rung and codec must be non-empty strings"
                )

    if totals["titles_pass"] != passing_titles:
        raise VerdictValidationError(
            f"totals.titles_pass ({totals['titles_pass']}) disagrees with the "
            f"{passing_titles} title(s) whose envelope_pass is true"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a SPEC-00 verdict JSON file")
    parser.add_argument("path", type=Path)
    arguments = parser.parse_args()
    try:
        with arguments.path.open(encoding="utf-8") as verdict_file:
            validate_verdict(json.load(verdict_file))
    except (OSError, json.JSONDecodeError, VerdictValidationError) as error:
        print(f"FAIL: {error}")
        return 1
    print(f"PASS: {arguments.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
