# SPEC-02 — Ladder Manifest format

> Freezes at tag `m01`. This is the Cedar contract: written before either the
> agent (producer) or the executor (consumer) exists, so neither drifts toward
> the other.

## Purpose

The manifest is the entire authority boundary of the model. The agent may
write manifests; the executor may replay approved manifests; nothing else
crosses.

## Draft shape (finalize during M00a–M01)

```json
{
  "manifest_id": "",
  "version": 1,
  "title_id": "",
  "proposed_by": {"agent": "", "model_id": "", "trace_id": ""},
  "rationale": "one paragraph, human-readable",
  "ladder": [
    {"rung": "1080p", "codec": "avc", "rate_control": "qvbr",
     "qvbr_level": 7, "max_bitrate_kbps": 0}
  ],
  "experiment": false,
  "estimated_normalized_minutes": 0.0,
  "estimated_usd": 0.0,
  "signature": "",
  "approval": {"state": "pending | approved | rejected",
               "approver": "", "timestamp": ""}
}
```

## Rules

1. Signed and versioned; stored in DynamoDB; immutable once approved.
2. `experiment: true` is required for any non-AVC codec (ADR-002) and caps
   estimated spend.
3. Cedar authorizes executor replay against the approved manifest — blast
   radius (which queues, which buckets) is policy, not convention.
4. The approval pause is a LangGraph interrupt checkpointed to DynamoDB: the
   pause is data, not process.
