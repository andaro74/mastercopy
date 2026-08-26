# CLAUDE.md — MasterCopy

Lean by design: conventions, commands, guardrails. Prose lives in PROJECT.md.

## What this repo is

Agentic per-title encoding on real AWS Elemental services. The agent proposes
a signed Ladder Manifest; a deterministic executor (no `bedrock:InvokeModel`
permission) replays it behind a Cedar gate and a human approval. Fictional
company: Meridian Media Group. Recurring specimen title:
*Meridian Sports: Regional Final*.

## Commands

```
make install        # deps (uv-managed Python)
make deploy-dev     # CDK deploy, dev stage — requires Budgets alarm (hook-enforced)
make destroy-dev    # tear down everything with an hourly meter
make seed           # upload the golden catalog mezzanines
make score          # run the scored eval suite → evals/history/
make event-window   # THE ONLY way MediaLive runs. TTL-tagged, auto-teardown.
make walkthrough    # replay the demo path
uv run pytest       # unit + contract tests
```

## Hard rules (hooks enforce most of these)

1. **Never run MediaLive outside `make event-window`.** Channels are
   TTL-tagged; the pre-deploy hook refuses untagged channels.
2. **Never edit `specs/` after its milestone tag.** Changes go in a new
   versioned spec. SPEC-00/01/02 freeze at `m00a`/`m01`.
3. **Never write a number into README's progression table without a matching
   artifact** in `milestones/M*/` or `evals/history/`. Pre-commit hook checks.
4. **Golden catalog is fixed after SPEC-01.** New titles → v2 set, scored
   separately.
5. **AVC by default.** HEVC jobs are budgeted experiments, named as such in
   the manifest (ADR-002). No 4K, no DRM (ADR-005).
6. **The executor never thinks; the agent never executes.** Any PR that gives
   the executor role Bedrock permissions, or the agent role
   mediaconvert:CreateJob, fails review by definition.
7. **Milestones close via `.claude/skills/close-milestone` only.** If a step
   fails, the milestone stays open.
8. **Every milestone close journals actual dollars** in
   `milestones/MXX/cost.md` (Cost Explorer, tag `project=mastercopy`).

## Conventions

- Branches: `mXX-shortname` (e.g. `m01-ingest`). Tags: `mXX`. Protected.
- ADRs: `adr/ADR-NNN-*.md`, never renumbered; reversals are dated amendments,
  not rewrites.
- Journals: `milestones/MXX/journal.md` opens with the four questions (see
  `milestones/TEMPLATE-journal.md`), ends with a short "how this milestone was
  built" note (plan-mode summary, agent autonomy, human interventions).
- Verdict schema (SPEC-00) is the only interface between scoring and every
  surface that displays scores (CI gate, dashboard, README).
- Screenshots: `milestones/MXX/screenshots/NN-description.png`.

## Workflow

- Start every milestone in plan mode against its spec.
- Subagents for parallelizable tracks (eval harness vs. infra).
- Verified commits; PRs into protected `main`; the eval gate is a required
  status check from M00a onward.
