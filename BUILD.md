# BUILD.md — how MasterCopy is being built

> Started day one, written as it happens — not reconstructed at the end.

This repo is a worked example of spec-first, gated, agentic development with
[Claude Code](https://www.claude.com/product/claude-code): the human's job is
specs, gates, and judgment; the agent's job is most of the code.

The visible rituals:

- **Specs before agent.** SPEC-00 (verdict schema), SPEC-01 (golden catalog +
  envelopes), SPEC-02 (manifest format) freeze before the agent exists, so
  scoring never chases a moving target.
- **Milestones close by procedure, not mood.** `.claude/skills/close-milestone`
  runs the scored suite, writes history, captures screenshots, updates the
  journal and the README table, and tags — and refuses to close if any step
  fails.
- **ADRs record reversals with measurements**, as dated amendments. The most
  credible pages in the repo are expected to be changes of mind.
- **Dollars are a first-class number.** Every milestone journals actual spend.
- **Hooks enforce what discipline used to**: no un-TTL'd MediaLive, no
  progression-table numbers without artifacts, no deploy without a Budgets
  alarm.

## Session log

| Date | Milestone | Mode | What the agent did | Where the human intervened |
|------|-----------|------|--------------------|----------------------------|
| _(begins with the first m00a session)_ | | | | |
