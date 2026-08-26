# SPEC-01 — Golden catalog and acceptance envelopes

> Freezes at tag `m01` (needs real clips to exist first). After that, the
> catalog never changes; new ideas go in a v2 set scored separately.

## Purpose

12–15 short fictional titles (2–3 min each) spanning content classes that
stress encoding differently. Each title gets an acceptance envelope the agent
must meet: minimum VMAF at every rung, total bits <= default ladder.

## Content classes (draft)

| Class | Why it stresses encoding | Titles |
|-------|--------------------------|--------|
| Live-action sports | high motion, crowds | Meridian Sports: Regional Final (THE specimen), +1 |
| Animation | flat regions, hard edges | 2 titles |
| Talking-head news | low motion, faces | 2 titles |
| Film-grain drama | noise vs. detail | 2 titles |
| Screen content | text legibility | 1–2 titles |

## Envelope shape (finalize at m01)

Per title: `vmaf_min_per_rung`, `bits_budget = default ladder actuals`,
`codec_allowlist = [avc]` (HEVC only via budgeted-experiment manifests,
ADR-002).

## Sourcing rule

All clips are original/synthetic or license-free. No third-party copyrighted
footage enters the repo or the buckets.
