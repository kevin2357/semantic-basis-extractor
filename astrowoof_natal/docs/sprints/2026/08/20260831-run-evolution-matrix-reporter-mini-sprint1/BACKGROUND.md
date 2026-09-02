# Background — deterministic run evolution matrix reporter

SBE now emits detailed `✨🐶` trace lines at workspace validation, native-state
projection, lifecycle selection, authority handoff, provider I/O,
reconciliation, local adoption, checkpoint publication, and command exit.
These logs made recent investigations substantially easier, but operators still
have to read hundreds of lines and mentally reconstruct a run's evolution.

The immediate design corpus is the owner-supplied full worker export:

`C:/Users/kevin/Downloads/sbe logs.txt`

This is diagnostic input, not native authority. The reporter must never convert
a log inference into an SBE lifecycle, custody, settlement, or transition fact.

## Initial corpus characterization

- Total lines: 1,000.
- `✨🐶` lines: 827.
- Prefix records parsed by the proposed grammar: 827/827.
- Native run IDs: two, plus global/unbound command records.
- Run `8a7c25e…`: 569 records over about 12m55s; initial reconciliation,
  accepted/rejected passes, two-action retry authority/dispatch, and later
  ambiguous/rejected retry evidence.
- Run `e0b406db…`: 239 records over about 4m03s; completed retry adoption,
  authoring completion, polish authority/dispatch, later reconciliation, and a
  local-work progress refusal.

The interleaving makes this a useful adverse fixture: a useful reporter must
partition by run/action identity before it builds any timeline.

## Product question

Can one deterministic, provider-free tool accept an arbitrary SBE worker log,
produce a closed normalized trace, and render each run as a compact evolution
matrix that answers:

- Where did the run spend time?
- Which native revision/checkpoint was current?
- What was happening to each pass/action?
- Who held custody?
- What command or authority boundary was selected?
- Which provider operations were created/retrieved?
- What local work was adopted or refused?
- Where did progress stop, repeat, contradict itself, or become unknowable?

The answer appears to be yes for current `0.4.36+` traces, with explicit
unknown/partial cells for older or incomplete logs.
