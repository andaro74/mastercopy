# ADR-003 — No LLM judge on core metrics

Date: 2026-08-26 · Status: accepted

## Context
beaconpave M03 calibrated an LLM judge and measured it unfit to move scores
(every axis demoted). MasterCopy's core metrics — VMAF, bits, normalized
minutes, dollars — have reference measurements available.

## Decision
Core metrics are computed, never judged. If LLM judging is ever introduced, it
applies only to the agent's written rationale, in a separate axis that cannot
affect PASS/FAIL, and only after published calibration.

## Consequences
+ The strongest evals story in the portfolio: ground truth without judge risk.
- The rationale's quality is initially unscored; acceptable.
