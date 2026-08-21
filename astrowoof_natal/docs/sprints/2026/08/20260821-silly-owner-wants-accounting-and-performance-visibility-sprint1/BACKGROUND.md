# Silly Owner Wants Accounting Visibility — Background

Date: 2026-08-21
Status: Slice 0 discovery complete and API-reviewed; no schema frozen

## Why this sprint exists

SBE already records substantial provider usage and cost evidence inside each native
run. The AstroWoof API also persists paid actions, provider operations, append-only
operation observations, and reported/reconciled cost. That evidence primarily
exists to preserve authority and recovery correctness, however—not to make
historical operational questions easy to answer.

Useful questions now exist independently of whether AstroWoof later tightens its
pre-submission cost estimates:

- What did initial authoring, retries, polish, critic, and candidate work actually
  cost?
- How do exact versus bounded, interactive versus Batch, model/reasoning settings,
  profiles, and prompt/resource versions differ?
- How much input was cached, written to cache, uncached, output, or reasoning?
- Which costs are SBE estimates from provider tokens, provider-reported amounts, or
  API-reconciled account billing?
- How long do provider create calls, provider-pending intervals, individual GETs,
  complete actions, stages, and decks take?
- Which observations were accepted, retried, truncated, failed, skipped, or left
  with unavailable usage?

Collecting durable, queryable observations is therefore useful accounting and
operational visibility in its own right. Future estimate calibration may consume
the observations, but it is no longer the reason this evidence deserves to exist.

## Current cost evidence

### Native SBE

The native paid-action ledger and provider metadata retain much of the source
evidence per action:

- native action, run, route, stage, pass, and attempt identity;
- profile/state/request binding and versioned price book;
- model, reasoning configuration, service level, maximum output, and commitment;
- input, cached-input, cache-write, output, reasoning, and total tokens when
  reported;
- SBE's price-book estimate from reported usage;
- provider status, Response/Batch identity, and cost disposition; and
- append-only reconciliation references.

Run accounting also aggregates usage and estimated cost by stage, model, and
service level. This evidence is authoritative for native execution but retained
workspaces are not a convenient analytics database.

### AstroWoof API

Current API persistence includes:

- `sbe_paid_actions`: category, maximum authorization, reported and reconciled
  cost, state, and provider operation identity;
- `sbe_provider_operations`: status, cost disposition, estimated micro-dollars,
  usage evidence reference, native observation, and immutable result linkage;
- `sbe_provider_operation_observations`: append-only native observations and exact
  JSON;
- `sbe_authoring_runs`: profile, execution mode, and frozen ceilings; and
- native receipts/artifacts connecting the observation to immutable SBE evidence.

This is a strong authority foundation. It does not yet provide a deliberately
normalized historical economics/latency fact suitable for ordinary percentile and
cohort queries. Some dimensions remain nested JSON or require several joins; stable
prompt-geometry identity is also not an explicit cohort key.

## Current timing evidence and its limits

Timing is presently retained in several different forms:

- interactive provider metadata can include action `elapsed_seconds`;
- the initial interactive wave result records aggregate
  `provider_io_elapsed_seconds`;
- pass and optional-stage records have `started_at` and `finished_at` boundaries;
- each reconciliation GET writes a durable diagnostic containing start, finish,
  duration, provider status, and sanitized error evidence;
- logs contain individual HTTP request durations; and
- the API records job/attempt/lease/checkpoint timestamps and derives bounded
  operational spans where both durable endpoints exist.

These do not currently form one normalized, long-term provider-latency dataset.
Several measurements also mean different things and must not be flattened:

| Measurement | Meaning |
|---|---|
| Create HTTP duration | Time to receive the provider's create response/identity |
| Retrieval HTTP duration | Time for one GET of a known operation |
| Identity-to-terminal observation | Upper-bound observed pending interval, including polling schedule delay |
| Provider-reported processing duration | Provider-native duration, only if explicitly supplied and documented |
| Native action duration | Durable SBE action boundary, potentially including detach/wait/reconciliation |
| API job/attempt duration | Product worker/orchestration interval, not provider compute time |

Open actions must keep null completion/duration. Missing timestamps must never be
converted to zero. A terminal observation time after a polling delay is not an
exact provider completion time.

## Proposed evidence product

Define a versioned, closed, append-only **provider economics observation** for one
exact native paid action or one exact Batch round. The public surface should look
like a transaction tape, not a grouped report: SBE exports individual facts and the
API derives summaries by stage, deck, route, model, profile, cohort, or time window.
Observations must be derived from immutable native evidence and expose no prompts,
subject data, credentials, or provider response content.

Provider settlement may precede editorial acceptance, retry disposition, final QA,
or delivery. One stable transaction may therefore acquire append-only revisions as
those later facts become durable. Each revision must identify its predecessor and
preserve all previously accepted provider identity, usage, cost-basis, timing, and
provenance facts. A revision adds knowledge; it never rewrites history.

Candidate dimensions:

| Concern | Candidate fields |
|---|---|
| Identity | native run/action ID, stage, route, pass/attempt or Batch round |
| Cohort | profile ID/manifest hash, SBE release, resource/prompt-geometry identity |
| Provider | mechanism, model, reasoning, service level, price book |
| Authority | commitment, maximum output, authorization and external-decision refs |
| Usage | input, cached input, cache write, output, reasoning, total tokens |
| Cost | SBE estimate, explicit provider monetary amount if available, API billing join reference—not reconciled value |
| Basis | reported, estimated, unavailable pending reconciliation, or no work consumed |
| Outcome | accepted, rejected/retried, failed, truncated, skipped, ambiguity/review |
| Timing | create HTTP, retrieval attempts, observed pending span, native action span |
| Provenance | immutable result/journal/snapshot/provider-evidence references |

The native observation should state only facts SBE can prove. API-reconciled cost is
API-owned and should be joined or projected by the API rather than written back as
native truth.

## Storage direction

The likely ownership split is:

1. SBE publishes a compact versioned observation or sufficient typed facts from
   native evidence.
2. The API validates and ingests it transactionally with the native result.
3. The API retains immutable revisions and may merge them into a query-friendly
   current transaction row or view using stable transaction/revision keys.
4. The API owns the durable normalized analytics projection and joins later billing
   reconciliation.
5. Immutable native/provider references remain the audit source; the analytics row
   does not replace them.
6. Percentiles, dashboards, exports, and future estimate recommendations derive
   from append-only observations rather than mutable running averages.

Whether the API needs a new table, an extension of provider-operation observations,
or a materialized/query view remains a field-by-field API design decision. This SBE
sprint should expose the native facts cleanly without claiming ownership of the API
migration.

## Cohort identity

Historical comparisons require a stable cohort identity more general than the
subject-specific request digest. A candidate cohort combines:

- route and paid stage;
- provider mechanism, model, reasoning, and service level;
- generation profile ID and exact manifest hash;
- SBE release and resource-bundle hash;
- explicit prompt/request-geometry contract version;
- price book and maximum-output policy; and
- outcome stratum where analytically relevant.

Changing prompt order, schema, cache breakpoints, resource text, pass topology, or
provider mechanism must not silently contaminate an existing cohort.

## Non-goals

This sprint does not:

- tighten commitment formulas or production ceilings;
- choose percentiles, margins, or minimum sample sizes for forecasts;
- make SBE the account-wide billing authority;
- treat estimates as reconciled charges;
- infer missing usage or timing as zero;
- expose prompts, provider payloads, or protected subject data;
- change the fifty-claim semantic budget; or
- build dashboards inside SBE.

## Questions for API review

- Which candidate fields are already queryable without parsing JSON?
- Should one API row represent a paid action, a provider operation, or an immutable
  observation revision?
- How should Batch round cost and member-level usage be represented without
  multiplying reservation authority?
- Which timestamps can be retained as authoritative facts versus derived spans?
- Does API billing reconciliation update the projection or append a separate joined
  reconciliation fact?
- What retention/privacy policy applies to provider IDs and timing diagnostics?
- Which cohort identity should SBE declare and which aggregation dimensions should
  remain API-owned?
- Should API retain one immutable revision table plus a current-state projection,
  or can its existing append-only observation table provide the revision history?
- Which native editorial milestones warrant a new revision, and what predecessor
  rule should API enforce transactionally?

