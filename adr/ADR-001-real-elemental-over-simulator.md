# ADR-001 — Real Elemental services over a simulated delivery chain

Date: 2026-08-26 · Status: accepted

## Context
An earlier design (AirCheck) simulated telemetry to stay keyless. The primary
goal of this project is learning and demonstrating real AWS media
capabilities.

## Decision
Build on real MediaConvert / MediaPackage / MediaTailor / CloudFront /
MediaLive. Accept real cost, governed by budget guardrails.

## Consequences
+ The learning and the demo are real; the bill becomes evidence.
- Costs money; requires the event-window discipline (ADR-004) and budget
  alarms. Iteration on long assets is priced out — short clips only.

## Displaced alternative
Keyless simulator: zero cost, but teaches agentic architecture without
teaching media. Retained as a possible sequel (incident triage over this
repo's real chain).
