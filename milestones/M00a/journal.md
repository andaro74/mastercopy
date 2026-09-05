# M00a — Foundation: specs frozen, a gate that can fail

> Status: **OPEN**. This file is completed by `.claude/skills/close-milestone`.
> The milestone does not close until every scope item below is done and the
> close procedure runs clean (CLAUDE.md hard rule 7).

## Scope

| Item | State |
|------|-------|
| Repo skeleton | done (`d46ec63`) |
| SPEC-00 finalized and frozen | done — [SPEC-00](../../specs/SPEC-00-verdict-schema.md) is normative, with [`tools/validate_verdict.py`](../../tools/validate_verdict.py) as its implementation |
| CI gate demonstrated to FAIL on a bad verdict | done locally — six bad fixtures in [`tests/fixtures/`](../../tests/fixtures/), asserted red by [`tests/test_verdict_gate.py`](../../tests/test_verdict_gate.py) |
| CI gate wired as a **required** status check | blocked — needs the branch pushed and branch protection configured on `main` |
| Hooks active | done — [`.claude/hooks/`](../../.claude/hooks/), wired for both humans (git) and the agent (`PreToolUse`) |
| Budgets alarm + cost tags live | blocked — [`infra/bootstrap_budget.py`](../../infra/bootstrap_budget.py) is written and dry-runs clean; creating the real budget and activating the `project` cost allocation tag is a human decision |

## The four questions
_(completed at close — see ../TEMPLATE-journal.md)_

## Notes toward the close

- The verdict schema froze against a validator rather than against prose, so
  the freeze has teeth: `tests/test_verdict_gate.py` re-validates every file
  ever written to `evals/history/`, which means a future schema drift breaks
  CI rather than quietly reinterpreting old runs.
- The pre-commit guard was tested by trying to commit a fabricated M03 row
  (`12/12`, `93.1`, `$41.20`) with no artifact behind it. It refused. That is
  hard rule 3 working before there is anything to be tempted about.
- `usd_actual` cannot be sourced until the `project` cost allocation tag is
  activated in Billing, so no verdict in this repo can carry a real dollar
  figure yet. Recorded here so the first one that does has a date attached.
