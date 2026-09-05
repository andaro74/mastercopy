# Hooks

The repo's discipline, made mechanical. Both guards are stdlib-only Python so
they run without the project venv, and both are wired twice: once for humans
(git hooks) and once for the agent (Claude Code `PreToolUse`).

| Guard | Enforces | Fires on |
|-------|----------|----------|
| [`pre_deploy.py`](pre_deploy.py) | Budgets alarm exists; no MediaLive resource without a TTL tag (ADR-004, infra/README.md) | `make deploy-dev`, `make event-window`, `cdk deploy` |
| [`pre_commit.py`](pre_commit.py) | No edits to a spec whose freeze tag exists; no README progression-table number without a linked artifact (CLAUDE.md hard rules 2 and 3) | every commit |

[`guard_bash.py`](guard_bash.py) is the `PreToolUse` dispatcher: it matches the
Bash command about to run and routes it to the guard a human would have hit.
It only matches a guarded verb at a *command position*, and strips heredoc
bodies first -- otherwise writing documentation about a guarded command trips
the guard, which is exactly how that rule was discovered. Teardown
(`make destroy-dev`) is deliberately never blocked: a spending guardrail
should not stand in the way of spending less.

## Enabling them

Claude Code hooks are already active via [`../settings.json`](../settings.json).
Git hooks need one local command per clone:

```
git config core.hooksPath .githooks
```

The guarded make targets also call `pre_deploy.py` directly, so the guard
holds even when neither hook system is installed.

## Failure posture

`pre_deploy.py` **fails closed**: no credentials, missing permissions, or an
API error all refuse the deploy. A money guardrail that degrades to "probably
fine" is not a guardrail. `pre_commit.py` fails closed on its own errors but
treats a missing README table as a warning -- deleting the table also deletes
the claims it would have policed.

Known limitation: the MediaLive check covers the caller's default region only.

Tests: [`../../tests/test_hooks.py`](../../tests/test_hooks.py).
