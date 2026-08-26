# ADR-002 — AVC by default; HEVC only as budgeted experiments

Date: 2026-08-26 · Status: accepted

## Context
MediaConvert bills in normalized minutes with compounding multipliers (codec,
resolution, passes, frame rate). HEVC/4K/multi-pass experiments can cost an
order of magnitude more per minute than the AVC baseline.

## Decision
Golden-set scoring runs AVC. The agent may propose HEVC only in a manifest
marked `experiment: true` with a spend cap.

## Consequences
+ Cost predictability; the headline comparison stays apples-to-apples.
- Leaves some per-title savings unexplored; recorded as future work rather
  than claimed.
