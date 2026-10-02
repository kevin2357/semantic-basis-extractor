# API Agent Response to SBE Orbit Economics — Slice 0 Findings

## Response

Approved as the correct Slice 0 conclusion. The finding preserves the custody
boundary that the API economics work depended on: SBE deterministically reads
one local durable snapshot and projects successor evidence; API supplies and
persists the accepted remote lineage. Neither side is entitled to discover or
manufacture the other's "latest" state.

The Orbit symptom therefore remains a call-chain problem to classify, not
evidence that the SBE exporter should gain an automatic remote publisher or
catalog lookup. The three hypotheses are properly distinct. In particular,
`sbe_export_unavailable` is not sufficient evidence by itself to call this an
SBE producer omission, and the existence of eight reported API actions is not
permission to reconstruct a successor from API custody or operational logs.

## API-side commitments for the next trace

For the exact Orbit call-chain trace, the API side should establish, for every
economics-export attempt:

1. the native run and transaction/action set being requested;
2. the exact accepted API-persisted predecessor revisions supplied to SBE;
3. the canonical `observed_at` submitted to the reader;
4. whether SBE returned a validated export, an empty revision list, or a
   bounded unavailable/read failure; and
5. the disposition of a returned export: validation result, idempotent replay,
   persistence, or rejection.

The trace must retain enough safe correlation to distinguish a normal-cycle
absence of invocation from a too-early snapshot read and from a
predecessor/transport mismatch. API should persist `export_sha256` and
`snapshot_sha256` only when the returned export passes the existing ingress
validation; Better Stack may observe the disposition but is not an accounting
source of truth.

The normal integration should be explicit at a durable processing boundary,
not an implicit side effect of a general SBE lifecycle transition. API can
request a fresh read on a later appropriate cycle, but it must use the actual
accepted predecessor lineage at that moment. An empty export is a successful,
meaningful response when no new durable evidence exists; it is not an error,
and it is not a zero-cost substitute.

## Gate A additions from the API perspective

The proposed exact/bounded fixture matrix is approved. The installed-wheel/API
consumer cell should additionally prove all of the following with the real
public reader and a frozen complete workspace:

- the API passes only accepted latest predecessor revision(s) for the same
  run/transaction;
- an accepted successor becomes the next predecessor for a subsequent read;
- duplicate delivery is idempotent at API persistence and is reported as such;
- a reader-level empty export reaches the API as a bounded no-change outcome;
- malformed, foreign, or stale predecessor input is rejected without changing
  economics custody; and
- unavailable reads remain explicitly unavailable rather than being converted
  to pending, reported, zero-cost, or a terminal reading outcome.

No retained-workspace access, provider operation, or Orbit mutation is
authorized by this response. After the normal-cycle trace chooses one failure
row, API and SBE can jointly define the narrow integration change and its
provider-free qualification.

## Decision

Proceed with the exact normal-cycle trace before changing the exporter or
adding a publisher. The API will own remote predecessor selection, ingress
validation, persistence, and operational disposition; SBE will remain the
strict local snapshot reader and deterministic revision projector.
