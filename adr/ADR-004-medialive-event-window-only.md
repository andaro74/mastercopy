# ADR-004 — MediaLive runs only as TTL-tagged event windows

Date: 2026-08-26 · Status: accepted

## Context
MediaLive bills per channel-hour whether or not anyone watches. A forgotten
HD channel is ~hundreds of dollars per month — the single biggest budget risk
in the project.

## Decision
`make event-window` is the only path that creates a channel: TTL-tagged,
scheduled teardown, pre-deploy hook refuses untagged channels. The M07
broadcast is a bounded window whose recorded artifacts become the permanent
demo; one extra window is reserved for running live during presentations.

## Consequences
+ Live milestone lands at tens of dollars, not hundreds.
- No always-on live channel to show; the recording plus the reserved window
  cover it.
