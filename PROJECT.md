# PROJECT.md — MasterCopy full specification

> Status: draft, to be completed and frozen during M00a. CLAUDE.md holds the
> operational rules; this file holds the fiction, the architecture, and the
> invariants.

## 1. The fiction

**Meridian Media Group** operates **Beacon**, a DTC streaming service with two
brands: **Meridian News** and **Meridian Sports** (shared fictional universe
with [beaconpave](https://github.com/andaro74/beaconpave)). MasterCopy is
Meridian's content supply chain. The catalog is 12–15 short fictional titles
spanning content classes chosen to stress encoding differently: live-action
sports (high motion), animation (flat regions, sharp edges), talking-head news
(low motion, faces), film-grain drama (noise), screen content (text).

Recurring specimen: **Meridian Sports: Regional Final** — followed through
every milestone.

## 2. The problem

A fixed ABR ladder overspends bits on easy content and underserves hard
content. Per-title encoding fixes this, but letting a model configure
production encoders directly is an operational and audit non-starter. The
demo's claim: an agent can capture per-title savings **while remaining
provably unable to touch production**.

## 3. The idea

> The agent proposes the ladder. The pipeline disposes.

Non-determinism is an asset in exactly one place — analyzing content and
proposing an encoding recipe, where the search space is large and judgment
helps. It is a liability everywhere else. The model emits a **signed,
versioned Ladder Manifest** (SPEC-02). Execution is deterministic replay by
Lambda whose role has no `bedrock:InvokeModel`; authorization is Cedar policy
the model cannot reach; a human approves at an interrupt checkpointed to
DynamoDB (the pause is data, not process — same property as
agentic-pii-erasure).

## 4. Architecture (to be drawn: arrows carry payloads, not just direction)

mezzanine (S3) → probe/complexity tools (MCP) → agent (LangGraph on Bedrock,
AgentCore identity/gateway/tracing) → Ladder Manifest (signed, DynamoDB) →
human approval gate → executor (Lambda, Cedar-gated) → MediaConvert job →
renditions (S3) → MediaPackage VOD → MediaTailor (SCTE-35 ad insertion) →
CloudFront → player (CMCD beacons) → VMAF + billing scorers → verdict
(SPEC-00).

M07 adds the live wing: MediaLive → MediaPackage, run only as a TTL-tagged
event window.

## 5. Invariants

1. Agent role: may read, probe, and write manifests. May not create
   MediaConvert jobs, touch MediaLive, or write to rendition buckets.
2. Executor role: may create MediaConvert jobs per an approved manifest. Has
   no Bedrock permissions of any kind.
3. Every scored number traces to an artifact under `evals/history/` or
   `milestones/M*/`.
4. Specs freeze at their milestone tag; changes are new versions.
5. Golden catalog and envelopes (SPEC-01) are fixed before the agent exists.
6. Core metrics (VMAF, bits, normalized minutes, dollars) are computed by
   reference tools, never judged by an LLM (ADR-003).

## 6. Out of scope (deliberate cuts, each with an ADR)

DRM/SPEKE, 4K/UHD, multi-region, reserved pricing, real ad decision servers
(a VAST stub suffices), live-to-VOD harvesting.

## 7. Budget

$200–300 across three months, journaled per milestone. Guardrails: AWS
Budgets alarm at $50/month with SNS notification, `project=mastercopy` cost
allocation tag on everything, `make destroy-dev`, event-window-only MediaLive.
