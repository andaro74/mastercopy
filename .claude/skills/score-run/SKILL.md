# score-run

Run the eval suite against the current build and record an append-only
verdict.

1. `make score` — computes per-title VMAF (local ffmpeg/libvmaf), delivered
   bits, MediaConvert normalized minutes, and USD actuals (Cost Explorer,
   tag-scoped).
2. Emit one SPEC-00 verdict JSON to `evals/history/YYYY-MM-DD-mXX-<runid>.json`.
3. Never edit or delete an existing verdict file. Corrections are new runs
   with a note.
4. Print the totals block and the PASS/FAIL verdict; exit nonzero on FAIL
   (this is what the CI gate consumes).
