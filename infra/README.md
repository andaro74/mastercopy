# infra

⚠️ **This deploys real AWS media services and spends real money.**

Ground rules (enforced by hooks where possible):
- Everything carries cost-allocation tag `project=mastercopy`.
- AWS Budgets alarm at $50/month with SNS notification exists before anything
  else deploys.
- `make destroy-dev` tears down everything with an hourly meter.
- MediaLive exists only inside `make event-window` (TTL-tagged, scheduled
  teardown) — ADR-004.
- CI deploys authenticate via GitHub OIDC to a scoped role. No long-lived
  keys in repo secrets.

Stack (CDK, lands M01+): S3 ingest/renditions, MediaConvert queue + role,
DynamoDB (manifests, checkpoints), Lambda executor (no Bedrock permissions),
MediaPackage VOD, MediaTailor config, CloudFront, and the two IAM planes the
whole thesis rests on (agent role vs. executor role).
