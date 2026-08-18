# Cost Tracking and Estimation Background

Date: 2026-08-18
Status: discovery input; not an approved implementation contract

## Why this work is being considered

SBE deliberately authorizes paid provider work using conservative commitments.
That protects the per-run ceiling and gives the AstroWoof API a safe amount to
reserve before provider submission, but current commitments can be materially
higher than eventual provider-reported cost. At low global spend limits, the
difference makes useful parallelism harder: safe reservations occupy more of the
API-owned budget than the completed work normally consumes.

The immediate question is whether historical evidence can support tighter, still
fail-closed commitments. Prompt-prefix caching is one likely source of predictable
savings, but it is not the only variable. Actual spend also varies by route, paid
stage, model configuration, provider mechanism, output behavior, and authoring
contract identity.

This is distinct from SBE's semantic claim budget. The fifty-claim basis limit is
an editorial/extraction constraint; the subject here is provider token usage and
dollar spend.

## Bounded live-run qualification finding

A retained SBE 0.4.6 interactive bounded-Natal run on 2026-08-18 provides the
first full-deck live calibration evidence for the new six-pass topology. All six
initial passes were accepted on their first attempt. Native accounting recorded
596,523 input tokens, 30,841 output tokens, 962 reasoning tokens, and an estimated
cost of USD 1.9539225. No creative retry, polish, critic, or candidate provider
work was submitted.

The assembled 50-card deck then correctly failed deterministic final QA because
two independently selected foundational claims represented the same North Node
editorial semantics through separate Mean Node and True Node source objects. The
two isolated passes consequently authored nine byte-equivalent body variants.
This is useful quality evidence, but it also exposed a state-projection defect:
the bounded lifecycle assigned `FINAL_QA_REQUIRES_REVIEW`, after which shared
`persist_state()` status recomputation inferred `AUTHORING_COMPLETE` solely from
the six accepted pass states and overwrote the more authoritative final-QA state.

The provider-safety consequence was limited in this run: the final-QA gate still
returned before polish, so no additional paid work was submitted. The public and
native status was nevertheless misleading. This must be repaired before bounded
observations are admitted into automated calibration cohorts, because cohort
outcome classification must distinguish accepted authoring passes from a deck
that failed cross-pass final QA.

The retained evidence workspace is intentionally preserved outside the release
tree at:

```text
C:\dev\github\semantic-basis-extractor\.runs\kevin-bounded-live-20260818\run
```

Its run ID is
`9e0ed9d979b6aaf8cd86e65672704648e1ea8dc59c7dcb6159ad700e811470ba`.
The workspace is diagnostic evidence, not a release fixture and not a completed
delivery. It must not be manually edited, blessed, or resumed past the failed QA
gate.

### Ownership and defensive policy

SPC owns the upstream bounded-projection decision about whether Mean Node, True
Node, or both are emitted. SBE should not silently choose one source record or
collapse their provenance. SBE does, however, own editorial admission and can
fail closed before paid authoring when two selected claims have equivalent
provider-visible/editorial semantics and would predictably yield duplicate cards.
The future check should report both claim IDs, source refs, correspondence/evidence
identities, and the equivalence basis so an upstream policy issue remains
diagnosable.

## Current commitment and settlement behavior

SBE's current pre-submission commitment is intentionally simple and conservative:

```text
estimated input tokens * uncached input rate
+ maximum output tokens * output rate
```

The input estimate uses UTF-8 byte length divided by four. Batch applies its
versioned price-book multiplier. The commitment does not assume that a particular
prompt prefix will receive a cache hit.

After provider work settles, native accounting is finer grained. SBE can retain
reported input, cached-input, cache-write, output, and reasoning usage; reported
or estimated cost components; model and service-level identity; stage and route;
price-book identity; the exact paid-action/request binding; and append-only
reconciliation references. Until settlement is available, committed spend remains
the counted amount. Polling an existing provider operation creates no new
commitment.

## Existing durable storage

### Native SBE evidence

Each run's native spend ledger and associated immutable/provider evidence already
contain much of the required per-action detail. Paid actions are distinguished as
initial authoring, creative retry, polish, qualitative critic, and qualitative
candidate work. Their bindings include route, stage, model, service level, maximum
output, commitment, price-book version, profile/state identity, and request digest.

This is authoritative per-run evidence, but retained workspaces and archived JSON
artifacts are not a convenient historical analytics database.

### AstroWoof API persistence

The API already persists several relevant layers:

- `sbe_paid_actions` records the logical paid action, category, maximum authorized
  spend, reported and reconciled cost, state, and provider-operation identity.
- `sbe_provider_operations` records provider status, cost disposition, SBE's
  estimated micro-dollars, usage-evidence reference, complete native observation,
  and immutable result linkage.
- `sbe_provider_operation_observations` retains append-only historical native
  observations and their complete JSON.
- `sbe_authoring_runs` records profile ID and contract, exact profile-manifest
  SHA-256, execution mode, and the frozen per-run/stage ceilings.
- Native execution receipts preserve route family, provider mechanism, immutable
  journal range, snapshot, and result evidence.

Consequently, this work does not require a second accounting authority. Existing
records can reconstruct a useful baseline. Some calibration dimensions, however,
currently live inside JSON or require joins across several tables. Historical
percentile queries would be awkward, and stable prompt-geometry identity is not
yet an explicit cohort key.

## Proposed storage direction

Keep native evidence and API billing reconciliation authoritative. Add, if the
discovery proves it useful, an API-owned append-only calibration projection with
one observation per settled paid action. This could be a narrowly scoped new table
or a compatible extension/projection of existing provider-operation observations;
that choice should follow a field-by-field audit rather than be assumed now.

The normalized observation should carry at least:

| Concern | Candidate fields |
|---|---|
| Pipeline | route family such as `exact_natal` or `bounded_natal` |
| Paid work | initial authoring, creative retry, polish, critic, or candidate |
| Provider path | Response or Batch mechanism; model; reasoning configuration; service level |
| Authoring identity | profile ID, profile contract, and exact profile-manifest SHA-256 |
| Implementation identity | SBE release and packaged resource-bundle identity |
| Prompt cohort | stable prompt-contract/layout or request-geometry version |
| Pricing | price-book version and applicable provider pricing mode |
| Authorized geometry | estimated input, cache-eligible input, maximum output, and commitment |
| Actual usage | reported input, cached input, cache-write, output, and reasoning usage |
| Cost evidence | native estimate, provider-reported cost, API-reconciled cost, and evidence basis |
| Outcome | accepted, rejected/retried, truncated, provider failure, or other closed result |

The row should reference the immutable native/provider evidence from which it was
derived. It must not replace that evidence or claim account-wide billing authority.
Mutable averages should not be the primary record. Percentiles and recommendations
should be computed from immutable observations by a view, report, or versioned
calibration job.

## Versioning and cohort identity

A simple human-maintained `authoring_version` would help, but it would be too easy
to leave unchanged when cost-relevant request geometry changes. A reliable cohort
should combine:

1. SBE release identity;
2. authoring profile ID and exact manifest SHA-256;
3. packaged prompt/resource-bundle SHA-256;
4. an explicit prompt-contract or request-geometry version;
5. route, paid stage, provider mechanism, model, reasoning configuration, and
   service level; and
6. price-book version and maximum-output policy.

The existing exact request digest remains valuable audit evidence but is normally
unique to a subject and assignment. It is therefore not a useful aggregation key.
The missing abstraction is a stable cohort identity meaning that requests used the
same templates, assembly order, schemas, routing policy, and cache geometry while
excluding subject-specific bytes.

This is especially important for cache-aware estimates. Moving dynamic material
earlier in a prompt, changing tool/schema text, or changing a prefix can alter cache
behavior even when the editorial goal and model stay the same. Such a change must
create a new cohort rather than silently contaminate historical calibration.

## Evidence-basis rules

Calibration must distinguish at least:

- provider usage reported;
- provider usage unavailable and billing reconciliation pending;
- no provider work consumed;
- SBE-computed estimate based on reported tokens; and
- account-authoritative billing reconciliation performed by the API.

Unavailable usage is not zero usage or zero cost. Likewise, native estimated cost
is useful operational evidence but is not the same as API-owned billing truth.
Output/reasoning fields must follow the provider's actual usage semantics and must
not be double-counted if a total already contains reasoning tokens.

## Possible adoption sequence

The working starting point is:

1. Export/query existing settled operations and measure how many observations have
   sufficient usage and identity evidence.
2. Audit the current native and API schemas field by field before choosing whether
   an API migration is necessary.
3. Define a stable, versioned calibration/cohort identity owned by the appropriate
   side of the SBE/API boundary.
4. If required, have SBE expose a compact versioned calibration block when paid
   actions settle and have the API ingest it as an append-only projection.
5. Derive p50/p90/p95 and upper-tail behavior by cohort, with minimum sample sizes,
   anomaly rules, and conservative fallback for unseen or changed cohorts.
6. Only then evaluate a tighter commitment formula and qualification strategy.

Before step 1 admits bounded observations, fix and qualify the bounded final-QA
state precedence described above. Otherwise historical queries could incorrectly
label a cross-pass QA failure as an authoring-complete outcome.

Historical evidence lacking a stable prompt identity should be labeled explicitly,
for example `legacy_unknown`. It may inform exploratory analysis but should not be
silently assigned to a modern cohort or automatically set production commitments.

## Open design questions

- Can current API rows plus their immutable JSON support the needed queries through
  a view, or is a normalized append-only table warranted?
- Which usage and prompt-geometry fields are already emitted consistently for every
  route and paid stage?
- Which repository owns the stable prompt/cohort declaration, and which repository
  owns derived calibration policy?
- How should cache-eligible prefix size be measured without making cache hits a
  safety assumption?
- What minimum sample size, percentile, safety margin, and aging window are safe?
- Should accepted and unaccepted generations be separate cohorts or outcome strata?
- How are model revisions or provider-side behavior changes detected when a public
  model name remains unchanged?
- What fallback applies to a new cohort, unavailable usage, Batch billing lag, or
  an observed tail above its calibrated commitment?
- Can a tighter estimate remain a reservation forecast while SBE's hard native
  ceiling continues to use an independently conservative maximum?

No answer in this document changes current spend enforcement or the SBE/API
authority split.
