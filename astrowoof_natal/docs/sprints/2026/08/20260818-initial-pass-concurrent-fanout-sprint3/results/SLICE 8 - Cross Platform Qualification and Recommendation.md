# Slice 8 — Cross-Platform Qualification and Recommendation

Status: complete; awaiting final Kevin/API review and separate release authorization

## Recommendation

Recommend the concurrent initial-wave work for a fresh immutable `0.4.7` release.
The qualification wheel still identifies itself as `0.4.6`, which is already an
immutable published release; it is evidence for the post-0.4.6 source boundary and
must not replace or alter 0.4.6.

## Reproducible artifact

Two independent builds used fixed epoch `1787084172` and were byte-identical:

| Property | Value |
|---|---|
| Qualified source commit | `05903cf` |
| Wheel | `astrowoof_natal_authoring-0.4.6-py3-none-any.whl` |
| Bytes | 821,731 |
| SHA-256 | `0609928cbeef837ac8b718b00217b46203a0ce1c119060d41011190ff2e2479b` |
| Entries / packaged resources | 114 / 67 |
| `py.typed` | present |
| Tests / bytecode in wheel | 0 / 0 |

The exact published SPC 0.11.0 dependency was downloaded and reverified at
`82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d`.

## Timing evidence

Each measurement gives six provider callbacks an identical scripted 75 ms delay.

| Runtime | Serial six-call sum | Concurrent wave | Ratio |
|---|---:|---:|---:|
| Windows CPython 3.12.13 | 451.7 ms | 78.1 ms | 0.173 |
| Linux CPython 3.11.15 | 451.1 ms | 78.9 ms | 0.175 |

The concurrent path tracks the slowest member plus small coordinator overhead, not
the sum of six members. The test retains six independent requests and serialized
native outcome persistence; it does not collapse editorial passes.

## Installed qualification

Windows and network-isolated Linux environments both passed:

- installation from the exact qualification SBE wheel and pinned SPC wheel;
- `pip check`;
- installed lifecycle smoke;
- installed exact release smoke;
- exact interactive initial wave;
- exact Batch six-member round;
- bounded interactive initial wave;
- bounded Batch six-member round; and
- installed-package timing driver with explicit `site-packages` origin proof.

The full source suite completed 456 tests in 428.516 seconds: 438 passed and 18
environment-dependent tests skipped. The strict schema/contract/lifecycle subset passed 41
tests without skips under the installed `jsonschema` environment.

Focused source coverage includes fresh-worker detach/not-due/reclaim, partial
completion, identity durability, pass-local retry, deterministic fan-in, optional
continuation, final QA/review, delivery, Batch usage settlement, stale observation,
single-writer contention, snapshot interruption, journal/result/receipt, and event
redaction.

## Residual limits

- Provider acceptance and local Response-ID persistence cannot be made one atomic
  transaction. Identity-less interruption remains ambiguous and fail-closed.
- Deterministic request keys are not asserted as OpenAI idempotency.
- Six creates can increase instantaneous API rate pressure. API-owned global
  reservations, quotas, and circuit breakers remain the governing controls.
- Retrieval remains independently bounded at four due actions per short cycle.
- Batch remains one paid round/API reservation; this sprint did not convert Batch
  members into interactive-style reservations.
- No paid live call was needed or made in Slice 8.

Machine-readable evidence is in
[`slice8-qualification.json`](slice8-qualification.json).

## Release gate

The implementation meets the sprint exit criteria. Version bump, final exact-source
rebuilds, tag, GitHub publication, and immutable asset verification require explicit
authorization after Kevin/API final review.
