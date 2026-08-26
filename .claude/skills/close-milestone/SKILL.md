# close-milestone

Closing a milestone is a procedure, not a mood. Run steps in order; if any
step fails, the milestone stays OPEN.

1. `make score` — full scored suite for this milestone. Verdict file written
   to `evals/history/`.
2. Journal: complete `milestones/MXX/journal.md` from the template — four
   questions, specimen-title section, "how this was built" note.
3. Cost: complete `milestones/MXX/cost.md` from Cost Explorer
   (`project=mastercopy`). Actuals only; if billing hasn't settled, stop here
   and resume tomorrow.
4. Screenshots into `milestones/MXX/screenshots/`, referenced from the
   journal.
5. README progression table: fill the row. Every number must link to an
   artifact from steps 1–4. Anomalies get footnotes, not rounding.
6. BUILD.md session log: append the row.
7. Commit on the milestone branch, PR to main, required checks green, merge,
   tag `mXX`.
