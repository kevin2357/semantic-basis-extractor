# Evidence

## Supplied corpus

- Source: `C:\Users\kevin\Downloads\sbe logs.txt`
- Total lines: 1,000
- `✨🐶` records: 827
- Parsed records: 827
- Malformed marked records: 0
- Command-result envelopes: 124
- Native runs: 2
- Registered unknown event names after inventory update: 0

The two runs contain 569 and 239 parsed events. The reporter produced 23 and 12
semantic lanes respectively. It identified five candidate semantic
republication cycles across the corpus. These are diagnostic candidates, not
asserted bugs.

## Source qualification

```text
python -m unittest astrowoof_natal.tests.test_run_report
```

Result: 9 tests passed.

Covered behavior includes deterministic parsing, interleaved partitioning,
privacy sentinel removal, exact no-progress detection, checkpoint-only semantic
republication detection, progress-witness suppression, report mutation refusal,
self-contained interactive rendering, four-format CLI output, malformed-line
accounting, and closed provider-free qualification replay.

## Generated artifact sizes

- `report.json`: approximately 484 KB
- `report.html`: approximately 283 KB
- `report.md`: approximately 24 KB
- `report.mmd`: approximately 8 KB

The generated report remains in the ignored local directory
`.tmp-run-report-latest/` for operator preview and is not source evidence.

## Safety

- External network calls: 0
- Provider calls: 0
- R2 reads/writes: 0
- Native workspace reads/writes: 0
- Runtime lifecycle/authority semantics changed: no
- Version/tag/publication: none

## Second real-corpus compatibility

The selected release sprint additionally exercised the reporter against the
2,149-line 2026-09-02 Render dashboard export. After adding the dashboard's
space-separated outer timestamp grammar, the parser recognized 1,829/1,829
marked trace lines, 317 JSON execution/command envelopes, two native runs, and
zero malformed or unknown registered events. Release qualification is recorded
in the adopting sprint rather than duplicated here.
