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
      YYYYMMDD-sprintN-short-name/
        PLAN.md
        LOG.md
        results/
          README.md
```

- `sprintN` resets to `sprint1` at the beginning of each date.
- `short-name` states the sprint's subject without trying to encode its entire scope.
- `PLAN.md` is the current approved scope, phases, controls, and exit criteria.
- `LOG.md` is the chronological execution and decision record.
- `results/` holds durable comparative findings, compact reports, and links to large or temporary artifacts.

Plans may be revised during a sprint when an explicitly scheduled learning
checkpoint changes the evidence. Record both the observation and resulting
plan change in `LOG.md`; do not silently rewrite the history of why a decision
was made.

Large generated decks, API responses, and temporary run directories should
normally remain outside Git. Store small reports or artifact manifests in
`results/` and link to external artifacts from the log.
