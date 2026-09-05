# SPEC-00 — Verdict schema

> **Frozen at tag `m00a`.** Every surface that displays a score (CI gate,
> dashboard, README progression table) reads this schema and nothing else.
> Changes go in `SPEC-00-v2`, never here (CLAUDE.md hard rule 2).

## Purpose

One scored run = one verdict file in `evals/history/`, named
`YYYY-MM-DD-mXX-<runid>.json`. Deciding this schema before any pipeline
exists is what makes M00b's ungoverned baseline comparable with M04's
governed agent.

The normative implementation is [`tools/validate_verdict.py`](../tools/validate_verdict.py).
If this document and that validator disagree, the disagreement is a bug in
one of them — fix it, don't route around it.

## Shape

```json
{
  "run_id": "2026-09-04-m00a-a1b2c3",
  "date": "2026-09-04",
  "milestone": "m00a",
  "git_sha": "d46ec63",
  "ladder_source": "default",
  "titles": [
    {
      "title_id": "meridian-sports-regional-final",
      "content_class": "sports",
      "renditions": [
        {"rung": "1080p", "vmaf": 95.4, "bitrate_kbps": 5000, "codec": "avc"}
      ],
      "vmaf_min": 95.4,
      "delivered_bits_total": 900000000,
      "mediaconvert_normalized_minutes": 2.5,
      "usd_actual": 0.0378,
      "envelope_pass": true
    }
  ],
  "totals": {
    "titles_pass": 1,
    "titles_total": 1,
    "bits_vs_default_pct": 0.0,
    "usd_vs_default_pct": 0.0
  },
  "verdict": "PASS"
}
```

## Fields

All fields are required. Unknown extra fields are permitted and ignored —
additive experiments must not break a frozen reader.

| Field | Type | Constraint |
|-------|------|------------|
| `run_id` | string | non-empty |
| `date` | string | `YYYY-MM-DD` |
| `milestone` | string | non-empty, e.g. `m00b` |
| `git_sha` | string | non-empty; the commit the run scored |
| `ladder_source` | string | `default` \| `ungoverned-agent` \| `governed-agent` |
| `titles` | array | non-empty |
| `totals` | object | see below |
| `verdict` | string | `PASS` \| `FAIL` |

### `titles[]`

| Field | Type | Constraint |
|-------|------|------------|
| `title_id` | string | non-empty; SPEC-01 catalog id |
| `content_class` | string | non-empty; SPEC-01 content class |
| `renditions` | array | non-empty |
| `vmaf_min` | number | lowest VMAF across this title's rungs |
| `delivered_bits_total` | number | sum across rungs |
| `mediaconvert_normalized_minutes` | number | as billed |
| `usd_actual` | number | Cost Explorer actual, never an estimate |
| `envelope_pass` | boolean | deterministic against SPEC-01 |

### `titles[].renditions[]`

| Field | Type | Constraint |
|-------|------|------------|
| `rung` | string | non-empty, e.g. `1080p` |
| `vmaf` | number | |
| `bitrate_kbps` | number | |
| `codec` | string | non-empty, e.g. `avc` |

### `totals`

| Field | Type | Constraint |
|-------|------|------------|
| `titles_pass` | integer | `0 <= titles_pass <= titles_total` |
| `titles_total` | integer | must equal `len(titles)` |
| `bits_vs_default_pct` | number | negative = fewer bits than the default ladder |
| `usd_vs_default_pct` | number | negative = cheaper than the default ladder |

## Rules

1. `usd_actual` comes from Cost Explorer via the `project=mastercopy` tag —
   never estimated.
2. `envelope_pass` is deterministic against SPEC-01 envelopes. No judgment
   calls, no LLM (ADR-003).
3. A verdict file is append-only history. Corrections are new runs.
4. Arithmetic must be self-consistent: `totals.titles_total` equals the
   number of titles, and `totals.titles_pass` equals the number of titles
   whose `envelope_pass` is `true`. A verdict that disagrees with its own
   titles is rejected before anyone gets to argue about it.
5. `bits_vs_default_pct` and `usd_vs_default_pct` are signed percentage
   deltas against the M01 default-ladder run. For a `default` run they are
   `0.0` by definition.
6. Whether a run's `verdict` may be `PASS` while individual titles fail their
   envelopes is a scoring policy question, decided in SPEC-01 and enforced by
   the M03 harness. This schema only guarantees the numbers are consistent.
