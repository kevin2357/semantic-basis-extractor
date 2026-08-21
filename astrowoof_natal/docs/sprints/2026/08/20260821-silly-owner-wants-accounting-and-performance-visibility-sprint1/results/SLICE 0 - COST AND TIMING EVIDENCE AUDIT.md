# Slice 0 — Cost and Timing Evidence Audit

Date: 2026-08-21
Status: complete; awaiting API review before contract design

## Conclusion

SBE and AstroWoof already preserve enough authoritative evidence to avoid building
a second billing ledger. The missing surface is a closed, privacy-minimized,
action-scoped projection that makes those facts consistently ingestible and
queryable.

SBE should publish that projection only after its source ledger, provider evidence,
journal range, result, snapshot, and publication receipt are durable. The API should
ingest it transactionally and idempotently, retain the exact native observation,
and own PostgreSQL normalization and later account-billing reconciliation.

SBE must not connect to or mutate AstroWoof PostgreSQL. Doing so would couple the
standalone native runtime to API credentials and migrations and would introduce an
unavoidable filesystem/database atomicity gap.

## Evidence matrix

| Fact | Current native source | Current public/API form | Gap or incompatibility |
|---|---|---|---|
| Native action identity | paid-action ledger `action_id` | paid action and journal action binding | Sufficient join key |
| Route and stage | action binding plus native route | journal route/action binding; API category | API category is coarser than native stage and does not preserve pass/attempt |
| Profile/request identity | action binding and run profile | authorization/request JSON and receipts | Subject-specific request digest is not an analytics cohort identity |
| Model/reasoning/service | provider request metadata and binding | mostly exact JSON or provider-operation context | Not deliberately normalized for historical queries |
| Maximum output/commitment | immutable action binding | API paid-action authorization | Already authoritative; observation should reference, not redefine, authority |
| Token usage | `reported.usage`, attempt metadata, Batch members | usage evidence reference plus exact observation JSON | Full token components are not normalized columns |
| Cached/cache-write tokens | normalized provider usage | nested native evidence | Cache-write support is provider-dependent; absence must not imply zero unless provider usage explicitly reports zero |
| SBE cost estimate | versioned price book applied to reported usage | `estimated_micro_usd` and reported API cost | SBE estimate is not provider invoice or account-authoritative billing |
| Reconciled cost | append-only reconciliation reference only | API `reconciled_cost_usd` | Correctly API-owned; must join later rather than appear as native truth |
| Cost disposition | ledger/Batch round and journal vocabulary | provider operation/observation columns | Existing closed vocabulary should be reused exactly |
| Create HTTP duration | interactive attempt `elapsed_seconds`; initial wave aggregate | logs/native JSON, not normalized | Per-member initial-wave create duration is not consistently durable/public |
| Retrieval HTTP duration | response diagnostic `duration_ms` per GET | retained native diagnostic; not normalized in API | Good source fact; one action may have many retrieval attempts |
| Observed pending interval | provider identity time to terminal observation | derivable from durable observations | Includes polling/backoff delay and is not provider compute duration |
| Native action/stage span | attempt/stage `started_at` and `finished_at` | native JSON, API job spans | Open/missing boundaries and route-specific meanings need normalization rules |
| API worker/lease span | not SBE-owned | API attempts, leases, checkpoints | Must remain a separate orchestration metric |
| Provider-native duration | only when provider explicitly supplies it | no stable common field | Must remain null unless contractually supplied; never infer it from polling |
| Outcome/acceptance | attempt QA, action state, Batch member state | journal/cycle outcomes plus exact JSON | Needs a closed analytics outcome distinct from lifecycle authority outcome |
| Provenance | ledger, evidence files, journal/result/snapshot/receipt | native execution receipts and provider observations | Sufficient substrate for immutable observation binding |

## Route and stage findings

The intended unit is one native paid action:

- exact or bounded interactive initial authoring: one action per logical pass and
  attempt;
- creative retry, polish, critic, and qualitative candidate: one action per
  attempt;
- exact or bounded Batch: one paid action per Batch round, with ordered member
  usage/outcome evidence nested beneath it; and
- providerless denial or skipped optional work: an action classification with no
  provider usage, not a fabricated zero-cost provider operation.

Batch members must not become separate API reservations or independent paid-action
facts. Member rows may be useful as subordinate audit/analytics detail, but their
usage must aggregate beneath exactly one round authority. Partial member usage must
retain `provider_usage_unavailable_billing_reconciliation_pending` for the round.

All five paid-stage categories exist in the current API contract: initial,
creative retry, polish, qualitative critic, and qualitative candidate. Native
stage/pass/attempt identity is more precise and should be retained without changing
those API authority categories.

## Cost semantics to freeze in Slice 1

The observation must distinguish:

1. `provider_usage_reported`: complete usage evidence exists and SBE may publish a
   price-book estimate;
2. `provider_usage_unavailable_billing_reconciliation_pending`: provider work may
   be billable but complete usage is absent;
3. `no_provider_work_consumed`: native evidence proves no provider work occurred;
4. `not_applicable_provider_pending`: work exists but is not terminally costed.

An estimated amount is only an SBE calculation from a named price book and reported
usage. The API's reported-cost projection and later reconciled account cost are
separate facts. Missing usage, partial Batch usage, and unknown pricing must never
become `$0`.

## Timing semantics to freeze in Slice 1

One generic `duration` would be misleading. Preserve independently:

- provider-create HTTP duration;
- each provider-retrieval HTTP duration;
- first durable provider identity to terminal observation span;
- native action and stage spans;
- provider-native processing duration, only if explicitly reported; and
- API worker/job/lease spans, which are outside the native observation.

Every duration needs a named basis and its endpoint timestamps or source reference.
Open actions retain null completion/duration. Terminal observation after a polling
delay is an upper-bound observed pending span, not exact provider processing time.

## Cohort gap

Existing request digests bind subject-specific bytes and are unsuitable as the only
historical cohort key. Slice 1 should define a prompt/request-geometry identity
that changes when editorial resources, request schema, cache breakpoints, pass
topology, or transport-relevant request construction changes. It should combine
with route, stage, model, reasoning, service level, generation profile/manifest,
SBE release/resource bundle, price book, and maximum-output policy.

The cohort identity is descriptive evidence, not permission to submit work and not
a replacement for the exact paid-action binding.

## Proposed publication and ingestion boundary

The lowest-risk option is an append-only observation referenced by a validated
native invocation result and its journal range. A consumer must validate the full
result/journal/snapshot/publication-receipt chain before accepting it.

Recommended replay identity:

`(native_run_id, native_action_id, observation_id, observation_sha256)`

The API should preserve the complete canonical observation JSON before or alongside
any normalized projection. Analytics projection failure must not reinterpret SBE
state, authorize provider work, or invalidate already-ingested native authority.

## Privacy boundary

The projection needs identities, configuration, usage, costs, outcomes, timings,
and immutable references. It does not need prompts, provider response content,
cards, claims, protected subject fields, credentials, authorization documents, or
complete action bindings. Fixtures use synthetic IDs and values only.

## Slice 1 questions for API review

1. Should the normalized API fact be a new action-observation table, an extension
   to provider-operation observations, or an API-owned projection/view over exact
   retained JSON?
2. Should member-level Batch facts be normalized or retained only inside the
   immutable round observation?
3. Does billing reconciliation append a separate joined fact (recommended), or
   update a convenience projection while preserving immutable history?
4. Which cohort dimensions need indexed columns on day one?
5. Should observations publish at every durable provider update or only when the
   action becomes terminally classified? The audit recommends append-only updates
   with a terminal action summary, avoiding delayed loss of retrieval timings.

## Slice 0 gate

PASS for native discovery. No contract or implementation should be frozen until the
API reviews this matrix and the representative fixtures.

