# Demo walkthrough (lands at M06)

One 10-minute path, two exits.

**Minutes 0–5 — the executive cut (no code on screen):**
1. A playable Meridian stream (CloudFront + real player).
2. The dashboard: same VMAF, fewer bits, fewer actual dollars — every row
   linking to a real MediaConvert job and a verdict file.
3. An SCTE-35 ad break fires; MediaTailor swaps the ad.
4. The approval gate: a pending agent manifest, approved by a human click.

> **Executives may exit here.** Quality, money, monetization, control.

**Minutes 5–10 — engineers continue:**
5. `curl` the HLS manifest; read the ladder as text.
6. The Ladder Manifest internals + the Cedar policy that scopes the executor.
7. A scored eval run end-to-end (`make score` → verdict file).
8. One ADR reversal, with the measurement that forced it.
