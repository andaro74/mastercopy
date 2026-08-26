# SPEC-00 — Verdict schema

> Freezes at tag `m00a`. Every surface that displays a score (CI gate,
> dashboard, README progression table) reads this schema and nothing else.

## Purpose

One scored run = one verdict file in `evals/history/`, named
`YYYY-MM-DD-mXX-<runid>.json`. Deciding this schema before any pipeline
exists is what makes M00b's ungoverned baseline comparable with M04's
governed agent.

## Draft shape (finalize during M00a)

```json
{
  "run_id": "",
  "date": "",
  "milestone": "",
  "git_sha": "",
  "ladder_source": "default | ungoverned-agent | governed-agent",
  "titles": [
    {
      "title_id": "meridian-sports-regional-final",
      "content_class": "sports",
      "renditions": [
        {"rung": "1080p", "vmaf": 0.0, "bitrate_kbps": 0, "codec": "avc"}
      ],
      "vmaf_min": 0.0,
      "delivered_bits_total": 0,
      "mediaconvert_normalized_minutes": 0.0,
      "usd_actual": 0.0,
      "envelope_pass": true
    }
  ],
  "totals": {
    "titles_pass": 0,
    "titles_total": 0,
    "bits_vs_default_pct": 0.0,
    "usd_vs_default_pct": 0.0
  },
  "verdict": "PASS | FAIL"
}
```

## Rules

1. `usd_actual` comes from Cost Explorer via the `project=mastercopy` tag —
   never estimated.
2. `envelope_pass` is deterministic against SPEC-01 envelopes. No judgment
   calls, no LLM (ADR-003).
3. A verdict file is append-only history. Corrections are new runs.
