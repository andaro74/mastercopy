# Hooks (implemented during M00a–M01)

These make the repo's discipline mechanical:

- **pre-deploy**: refuse `make deploy-dev` if the Budgets alarm is absent, or
  if any MediaLive resource lacks a TTL tag (ADR-004).
- **pre-commit**: fail if the README progression table contains a number with
  no matching artifact in `milestones/M*/` or `evals/history/`; fail if a
  frozen spec under `specs/` is modified after its milestone tag.
