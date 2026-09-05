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

## Bootstrap (run once, before anything else)

```
MASTERCOPY_ALERT_EMAIL=you@example.com make bootstrap-budget
```

`bootstrap_budget.py` creates the SNS topic and the $50/month budget filtered
to the `project=mastercopy` cost allocation tag, alerting at 80% actual and
100% forecasted. It is idempotent and has a `--dry-run`. It lives outside the
CDK app on purpose: the pre-deploy hook blocks the deploy that would otherwise
create the alarm guarding it.

Afterwards, activate the `project` cost allocation tag in Billing > Cost
allocation tags. Until it is active the budget filter matches nothing and
`usd_actual` cannot be sourced from Cost Explorer (SPEC-00 rule 1).

Stack (CDK, lands M01+): S3 ingest/renditions, MediaConvert queue + role,
DynamoDB (manifests, checkpoints), Lambda executor (no Bedrock permissions),
MediaPackage VOD, MediaTailor config, CloudFront, and the two IAM planes the
whole thesis rests on (agent role vs. executor role).
