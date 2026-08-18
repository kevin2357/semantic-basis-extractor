# Slice 5 Result — Bounded Batch Transport

Status: complete; awaiting API fixture/lifecycle review

## Outcome

Bounded-Natal v2 now supports Batch for initial six-pass authoring and pass-local
creative retry. Batch changes provider transport only. It does not change pass
membership, prompt/schema bytes, retry feedback, authority reattachment, acceptance,
or deterministic assembly.

One Batch round is one paid SBE action and one API reservation unit. Its members are
ordered pass/attempt evidence below that authority. The initial round contains six
members; a single rejected member creates a later one-member creative-retry round.

## Durability and safety

The native round persists its JSONL hash, ordered member bindings, File ID, Batch
ID/status, request counts, output/error identities, aggregate maximum output,
aggregate commitment, and cost disposition. Once Batch identity is durable, restart
retrieves it and cannot upload or create replacement provider work.

Terminal provider files are validated as one exact member inventory before any
member mutation. Duplicate, unknown, missing, overlapping, or malformed evidence
fails closed. Provider-terminal failed rounds become pass-local retry evidence.

Provider usage absent from any potentially billable member of a terminal Batch is
not zero. SBE requires complete member usage before aggregate settlement; a mixed
reported/unreported round remains billing reconciliation pending. Provider polling
custody ends, but the API retains consumer authority under its own policy.

## Public lifecycle

Inspection v0.3 validates bounded-Natal route family plus Batch mechanism and exact
round operation reference. Neutral reconciliation accepts configured bounded Batch
adapters, performs retrieval only, and uses existing waiting/review/terminal and
cost-disposition vocabularies. Legacy bounded v1 Batch remains unsupported.

## Qualification

- Exact semantic closure: 85 tests passed in 207.894 seconds.
- Desktop bounded/lifecycle gate: 120 tests passed in 124.146 seconds.
- Python 3.11 Linux read-only-container gate: 120 tests passed in 27.162 seconds.
- Provider operations: 0. Spend: USD 0.

## Gate conclusion

The bounded Batch transport, round-level authority, pass-local retry, provider
custody, billing-authority separation, and restart behavior satisfy Slice 5. API
fixture/lifecycle review is required before Slice 6 begins.
