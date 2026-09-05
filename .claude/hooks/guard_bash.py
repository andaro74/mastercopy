#!/usr/bin/env python3
"""Claude Code PreToolUse dispatcher for the repo's guardrails.

Git hooks catch humans; this catches the agent. It inspects the Bash command
about to run and routes deploy-shaped and commit-shaped commands to the same
guards a human would hit. Exit 2 blocks the tool call and returns the reason
to the model.

Matching is deliberately narrow. A command only counts if the guarded verb
sits at a *command position* -- start of line, or after a shell separator --
and heredoc bodies are stripped first. Otherwise writing documentation about
a guarded command trips the guard that documents it, which is how this rule
was discovered.

Commands that match nothing exit 0 immediately, so the common case costs a
process start and a regex.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


HOOKS = Path(__file__).resolve().parent

HEREDOC_START = re.compile(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?")
COMMAND_POSITION = r"(?:^|[;&|(]|\n)\s*"

# Teardown is deliberately absent: destroying resources is never blocked by a
# guardrail about spending money.
GUARDS = (
    (
        re.compile(
            COMMAND_POSITION + r"(?:make\s+(?:deploy-dev|event-window)|cdk\s+deploy)\b"
        ),
        "pre_deploy.py",
    ),
    (re.compile(COMMAND_POSITION + r"git\s+commit\b"), "pre_commit.py"),
)


def strip_heredocs(command: str) -> str:
    """Drop heredoc bodies so their contents are never read as commands."""
    lines = command.splitlines()
    kept: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        kept.append(line)
        match = HEREDOC_START.search(line)
        index += 1
        if not match:
            continue
        delimiter = match.group(1)
        while index < len(lines) and lines[index].strip() != delimiter:
            index += 1
        index += 1  # skip the delimiter line itself
    return "\n".join(kept)


def guards_for(command: str) -> list[str]:
    payload = strip_heredocs(command)
    return [script for pattern, script in GUARDS if pattern.search(payload)]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    if payload.get("tool_name") != "Bash":
        return 0
    command = (payload.get("tool_input") or {}).get("command", "")
    if not isinstance(command, str) or not command:
        return 0

    for script in guards_for(command):
        result = subprocess.run(
            [sys.executable, str(HOOKS / script)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode != 0:
            sys.stderr.write(result.stdout + result.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
