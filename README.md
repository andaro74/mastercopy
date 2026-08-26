# MasterCopy

**Agentic per-title encoding on the real AWS Elemental stack — the agent
proposes the ladder, the pipeline disposes.** Same VMAF, fewer dollars, with a
signed manifest and a human gate between the model and production.

Built milestone-by-milestone with Claude Code. Every milestone is branched,
tagged, scored against a fixed golden catalog, journaled, and priced —
**the repo history IS the demo.**

The fictional company is **Meridian Media Group**, operating **Beacon**, a DTC
streaming service (see [beaconpave](https://github.com/andaro74/beaconpave)).
MasterCopy is Meridian's content supply chain: a mezzanine file goes in, a
playable, monetized, measured stream comes out — and an agent decides how each
title is encoded without ever being able to touch production. Everything is
fictional — catalog, brands, company. Fork it and rename it for yours.

> **The agent proposes the ladder. The pipeline disposes.
> VMAF keeps the quality honest. The bill keeps the savings honest.**

## The headline, stated the honest way

Meridian encodes its catalog two ways: a fixed default ladder, and the agent's
per-title proposal. Both are scored with VMAF (a reference metric — no LLM
judge on the core numbers, ADR-003) and both appear on the AWS bill. The claim
this repo exists to earn: **equal perceptual quality, materially fewer
delivered bits, materially fewer dollars — with every number linking to a
recorded artifact.** Until a milestone records those numbers, the table below
says ⬜ and the claim is a promise, not a result.

## Progression

| M | Milestone | Branch | Tag | Golden titles | VMAF envelope | $ journaled | Status |
|---|-----------|--------|-----|---------------|---------------|-------------|--------|
| 00a | Foundation: specs frozen, a gate that can fail | `m00a-foundation` | `m00a` | n/a | n/a | – | ⬜ |
| 00b | Ungoverned baseline (**the control**) | `m00b-ungoverned-baseline` | `m00b` | –/– | – | – | ⬜ |
| 01 | Ingest + default ABR ladder (MediaConvert) — first playable stream | `m01-ingest` | `m01` | –/– | – | – | ⬜ |
| 02 | MCP tool plane + deterministic executor topology | `m02-tool-plane` | `m02` | –/– | – | – | ⬜ |
| 03 | VMAF eval harness + golden catalog scored on default ladder | `m03-evals` | `m03` | –/– | – | – | ⬜ |
| 04 | The agent: signed manifests, Cedar gate, approval interrupt | `m04-agent` | `m04` | –/– | – | – | ⬜ |
| 05 | Packaging + monetization (MediaPackage, MediaTailor, SCTE-35) | `m05-monetize` | `m05` | –/– | – | – | ⬜ |
| 06 | Dashboard + CloudFront player + CMCD beacons | `m06-surface` | `m06` | –/– | – | – | ⬜ |
| 07 | Live capstone: the Meridian Sports event window (MediaLive) | `m07-live` | `m07` | –/– | – | – | ⬜ |

Fill each row at milestone close (see `.claude/skills/close-milestone`). A row
without a linked artifact in `milestones/M*/` or `evals/history/` does not get
a number.

## The two theses

**The media thesis** (for executives): cut the encoding bill without viewers
noticing, and the AI never touches production. The agent's authority ends at a
signed, versioned Ladder Manifest; execution is deterministic replay by an
executor role with no `bedrock:InvokeModel` permission, gated by Cedar policy
the model cannot reach, behind a human approval.

**The method thesis** (for engineers): this is what application development
looks like when an agent writes most of the code — the human's job moves to
specs, gates, and judgment. Specs are frozen before the agent exists
(`specs/`), milestones close by a skill that refuses to close on failing
evals, ADRs record reversals with measurements attached, and dollars spent are
journaled per milestone. `BUILD.md` tells that story; the milestone journals
exhibit it.

## Reading this repo

- New to media services? Start with [`docs/media-101.md`](docs/media-101.md) —
  a translation table from media concepts to systems concepts you already
  know, not a textbook.
- Every milestone journal opens with the same four questions: what exists now,
  what the new AWS service is, why the system needs it, what it means in
  business terms. Skim question 1 and 4 for the executive pass; read 2 and 3
  for the engineering pass.
- One title — *Meridian Sports: Regional Final* — is followed through the
  entire chain as the recurring specimen.
- `docs/demo-walkthrough.md` (lands at M06) is one 10-minute path with a
  marked exit at minute 5 for executives.

## Cost, stated plainly

⚠️ **This repo spends real money, and the live milestone spends it fastest.**
MediaConvert bills per normalized output minute (cheap on short clips,
multiplier surprises on HEVC/4K — ADR-002). MediaLive bills per channel-hour
whether or not you are watching (which is why M07 is an *event window* with a
teardown, ADR-004). Read [`infra/README.md`](infra/README.md), keep the
Budgets alarm on, and run `make destroy-dev` when you are done. Actual dollars
spent are journaled at every milestone close in `milestones/M*/cost.md`.

## Status

Pre-`m00a`. The skeleton and the specs are the first milestone's work; nothing
is scored, nothing is claimed. The empty table above is the accountability
format the rest of the repo will be held to.
