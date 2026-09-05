#!/usr/bin/env python3
"""Pre-commit guard - CLAUDE.md hard rules 2 and 3, made mechanical.

Two refusals:

* A spec under ``specs/`` may not be edited once its freeze tag exists.
  The tag is read from the copy in HEAD, so removing the "Frozen at tag"
  line in the same commit does not unfreeze the spec.
* The README progression table may not carry a number in an evidence column
  unless the row links to an artifact that exists under ``milestones/M*/``
  or ``evals/history/``.

Exit 2 blocks. Stdlib only: this runs as a git hook and as a Claude Code
PreToolUse hook, neither of which has the project venv.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


FREEZE_PATTERN = re.compile(r"Frozen at tag `([^`]+)`|Freezes at tag `([^`]+)`")
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
ARTIFACT_PREFIXES = ("milestones/", "evals/history/")
EVIDENCE_COLUMNS = {"golden titles", "vmaf envelope", "$ journaled", "status"}


def repo_root() -> Path:
    return Path(
        _git("rev-parse", "--show-toplevel", check=True).strip()
    )


def _git(*args: str, check: bool = False) -> str:
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, encoding="utf-8"
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout if result.returncode == 0 else ""


def frozen_spec_violations() -> list[str]:
    """Refuse edits to a spec whose milestone tag has already been cut."""
    existing_tags = set(_git("tag", "--list").split())
    if not existing_tags:
        return []

    staged = [
        line
        for line in _git("diff", "--cached", "--name-only").splitlines()
        if line.startswith("specs/")
    ]

    violations = []
    for path in staged:
        head_copy = _git("show", f"HEAD:{path}")
        if not head_copy:
            continue  # new spec — freezing applies from its own tag onward
        match = FREEZE_PATTERN.search(head_copy)
        if not match:
            continue
        tag = match.group(1) or match.group(2)
        if tag in existing_tags:
            violations.append(
                f"{path} is frozen at tag `{tag}`, which already exists. "
                f"Frozen specs are never edited - open a new versioned spec "
                f"(CLAUDE.md hard rule 2)."
            )
    return violations


def _table_rows(markdown: str) -> tuple[list[str], list[str]]:
    """Return (header cells, raw rows) for the progression table."""
    header: list[str] = []
    rows: list[str] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if header:
                break  # table ended
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not header:
            lowered = {cell.lower() for cell in cells}
            if EVIDENCE_COLUMNS & lowered:
                header = cells
            continue
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue  # separator row
        rows.append(stripped)
    return header, rows


def readme_table_violations(root: Path) -> list[str]:
    """Every number in an evidence column needs an artifact behind it."""
    markdown = _git("show", ":README.md")
    if not markdown:
        return []
    return table_violations(markdown, root)


def table_violations(markdown: str, root: Path) -> list[str]:
    header, rows = _table_rows(markdown)
    if not header:
        print(
            "pre-commit: progression table not found in README.md - "
            "skipping the artifact check.",
            file=sys.stderr,
        )
        return []

    evidence_indexes = [
        index
        for index, cell in enumerate(header)
        if cell.lower() in EVIDENCE_COLUMNS
    ]

    violations = []
    for row in rows:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        claimed = [
            header[index]
            for index in evidence_indexes
            if index < len(cells) and any(char.isdigit() for char in cells[index])
        ]
        if not claimed:
            continue

        linked = [
            link
            for link in LINK_PATTERN.findall(row)
            if link.startswith(ARTIFACT_PREFIXES) and (root / link).exists()
        ]
        if not linked:
            label = cells[0] if cells else "?"
            violations.append(
                f"README progression table row {label!r} puts a number in "
                f"{', '.join(claimed)} with no linked artifact under "
                f"milestones/M*/ or evals/history/ (CLAUDE.md hard rule 3)."
            )
    return violations


def main() -> int:
    try:
        root = repo_root()
    except RuntimeError as error:
        print(f"pre-commit: {error}", file=sys.stderr)
        return 2

    violations = frozen_spec_violations() + readme_table_violations(root)
    if violations:
        print("\nCommit refused:\n", file=sys.stderr)
        for violation in violations:
            print(f"  - {violation}", file=sys.stderr)
        print("", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
