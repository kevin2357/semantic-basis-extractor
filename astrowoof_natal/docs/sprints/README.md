# AstroWoof Development Sprints

This directory contains short, date-scoped implementation and research
sprints. A sprint is a bounded collaboration session, not a fixed-duration
project-management ceremony. Most sprints are expected to take less than one
day.

## Directory convention

```text
docs/sprints/
  YYYY/
    MM/
      YYYYMMDD-short-name-sprintN/
        PLAN.md
        LOG.md
        results/
          README.md
```

- `sprintN` resets to `sprint1` at the beginning of each date.
- `short-name` states the sprint's subject without trying to encode its entire scope.
- Historical directories may place `sprintN` before the short name. Preserve
  those paths; new sprints use the convention above.
- `PLAN.md` is the current approved scope, phases, controls, and exit criteria.
- `LOG.md` is the chronological execution and decision record.
- `results/` holds durable comparative findings, compact reports, and links to large or temporary artifacts.

Each planned slice should name its independently reviewable outcome and gate.
At a gate, run proportionate tests, inspect the diff, run `git diff --check`,
update the log, write a slice result, and pause for approval before committing.
Sprint completion means the explicit exit criteria are satisfied, not merely
that every planned activity was attempted.

Plans may be revised during a sprint when an explicitly scheduled learning
checkpoint changes the evidence. Record both the observation and resulting
plan change in `LOG.md`; do not silently rewrite the history of why a decision
was made.

Large generated decks, API responses, and temporary run directories should
normally remain outside Git. Store small reports or artifact manifests in
`results/` and link to external artifacts from the log.

## Promotion to project authority

Sprint documents are evidence and implementation history. When a sprint
establishes a decision, product principle, shared contract, roadmap change, or
operational policy affecting multiple AstroWoof repositories, promote that
conclusion to
[`astrowoof-project`](https://github.com/kevin2357/astrowoof-project).
Keep the original sprint record intact and add an authority notice or link when
readers might otherwise mistake it for the living cross-system source.
