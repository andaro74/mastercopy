#!/usr/bin/env python3
"""Pre-deploy guard - no deploy without a Budgets alarm, no untagged MediaLive.

infra/README.md and ADR-004, made mechanical:

* A Budgets alarm scoped to this project must exist before anything deploys.
* Every MediaLive channel and input in the region must carry a TTL tag, so a
  forgotten channel cannot bill per hour indefinitely.

**Fails closed.** If the guard cannot prove the guardrails are in place — no
credentials, no permissions, an API error — the deploy does not happen. A
money guardrail that degrades to "probably fine" is not a guardrail.

Exit 2 blocks. Stdlib only; shells out to the aws CLI.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys


BUDGET_NAME_HINT = os.environ.get("MASTERCOPY_BUDGET_NAME", "mastercopy")
TTL_TAG_KEYS = {"ttl", "ttl-hours", "ttlhours", "expires", "expiry"}


class GuardError(RuntimeError):
    """The guard could not verify a guardrail. Treated as a failure."""


def _aws(*args: str):
    if shutil.which("aws") is None:
        raise GuardError(
            "the aws CLI is not on PATH, so the deploy guardrails cannot be "
            "verified"
        )
    result = subprocess.run(
        ["aws", *args], capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        raise GuardError(
            f"`aws {' '.join(args)}` failed: {result.stderr.strip().splitlines()[-1]}"
            if result.stderr.strip()
            else f"`aws {' '.join(args)}` failed"
        )
    if not result.stdout.strip():
        return None
    return json.loads(result.stdout)


def check_budget() -> list[str]:
    identity = _aws("sts", "get-caller-identity", "--output", "json")
    account_id = identity["Account"]

    budgets = _aws(
        "budgets",
        "describe-budgets",
        "--account-id",
        account_id,
        "--output",
        "json",
    )
    names = [budget["BudgetName"] for budget in (budgets or {}).get("Budgets", [])]
    matching = [name for name in names if BUDGET_NAME_HINT.lower() in name.lower()]

    if matching:
        return []
    return [
        f"no AWS Budgets alarm matching {BUDGET_NAME_HINT!r} exists in account "
        f"{account_id}. Run `make bootstrap-budget` first - the Budgets alarm "
        f"exists before anything else deploys (infra/README.md). "
        f"Budgets found: {', '.join(names) or 'none'}."
    ]


def _untagged(resources, kind: str) -> list[str]:
    violations = []
    for resource in resources:
        tags = {key.lower(): value for key, value in (resource.get("Tags") or {}).items()}
        if not (TTL_TAG_KEYS & tags.keys()):
            label = resource.get("Name") or resource.get("Id") or resource.get("Arn")
            violations.append(
                f"MediaLive {kind} {label!r} has no TTL tag. MediaLive runs only "
                f"inside `make event-window`, TTL-tagged with a scheduled "
                f"teardown (ADR-004)."
            )
    return violations


def check_medialive_ttl() -> list[str]:
    channels = _aws("medialive", "list-channels", "--output", "json") or {}
    inputs = _aws("medialive", "list-inputs", "--output", "json") or {}
    return _untagged(channels.get("Channels", []), "channel") + _untagged(
        inputs.get("Inputs", []), "input"
    )


def main() -> int:
    try:
        violations = check_budget() + check_medialive_ttl()
    except GuardError as error:
        print(
            f"\nDeploy refused - the guard could not verify the guardrails:\n\n"
            f"  - {error}\n\n"
            f"This guard fails closed on purpose. Fix the access or the "
            f"configuration; do not route around it.\n",
            file=sys.stderr,
        )
        return 2
    except (KeyError, ValueError) as error:
        print(f"\nDeploy refused - unexpected AWS response: {error}\n", file=sys.stderr)
        return 2

    if violations:
        print("\nDeploy refused:\n", file=sys.stderr)
        for violation in violations:
            print(f"  - {violation}", file=sys.stderr)
        print("", file=sys.stderr)
        return 2

    print("pre-deploy: Budgets alarm present, no untagged MediaLive resources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
