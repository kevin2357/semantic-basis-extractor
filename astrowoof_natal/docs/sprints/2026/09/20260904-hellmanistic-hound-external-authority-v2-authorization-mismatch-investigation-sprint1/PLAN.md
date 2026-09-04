# Plan — external-authority v2 authorization mismatch investigation

## Slice 0 — Trace and public-contract inventory — Complete

Map the supplied Hound trace to released `0.4.44` public v2 request, grant,
fence, action, and dispatch readers. Catalogue each digest field by its actual
domain and establish the first rejection predicate from source or state an
evidence ceiling.

In particular, prove whether the fresh request/grant passed fence validation
before the refusal, and trace why a completed/reported predecessor could retain
a live v2 dispatch intent while successor authority is selected. Distinguish a
fresh-grant defect from the dispatch-time identity comparison against a stale
native intent; do not infer either from the generic `authorization_mismatch`
reason label.

## Slice 1 — Provider-free reproduction — Complete

Construct the smallest real-native/provider-free test that reaches the same v2
dispatch/revalidation boundary. Preserve API-owned authority as an external
public artifact; do not manufacture an API private-state replica.

The reproduction must prove both facts independently: the fresh successor
request/grant pass their public fence, and the existing predecessor intent is
the actual identity mismatch. It must prove that the current CLI nonetheless
calls dispatch, while payload resolution and provider create remain unreachable.

## Voof-paws — Joint repair decision required

Before runtime mutation, agree the public disposition for a fresh, valid grant
blocked by an obsolete completed intent, and confirm the safe writer boundary
for intent retirement during response reconciliation. The candidate repair must
not turn a stale intent into permission to create or make API infer a
replacement grant.

## Slice 2 — Joint resolution packet

If a defect is proven, define the smallest general SBE/API correction, the
cross-boundary regression tests, and release/compatibility implications. Active
QA recovery is explicitly out of scope.

**Implemented repair candidate:** response-reconciliation's coordinator-owned
post-adoption checkpoint requests ordinary-v2 intent retirement. It retires
only an intent whose complete ordered inventory is durably `REPORTED` with
complete provider evidence; pending, ambiguous, and incomplete inventory stays
live. The v2 CLI now returns an explicit, zero-I/O v4 command result with
`completed_intent_retirement_required` only after independently proving a
different live intent is fully reported, custody-free, unambiguous, and
retireable; it does not dispatch against different request/grant identities.
All other `action_state_or_custody_mismatch` causes retain their existing
fail-closed refusal/exception paths.

**Compatibility:** this adds closed public provider-dispatch v5 and command
result v4 readers/schemas. API must treat the result as a refused invocation,
run no provider create, and obtain any subsequent authority only from a fresh
post-retirement inspection. No retained-QA mutation or API private-state
reconstruction is part of the patch.

## Voof-paws — Review repair candidate

Before qualification/release preparation, review the narrowed public refusal
shape and the response-adoption checkpoint tests. In particular, confirm that
the new reason remains distinct from a grant validation failure and that API
maps it to an ordinary fresh-inspection path, never an implicit regrant or
retry.

## Slice 3 — Installed-wheel qualification — Complete

Build the frozen `0.4.45` candidate twice under a controlled build timestamp;
require byte-identical wheel bytes. Install the candidate outside the checkout
with the exact local SPC `0.11.1` compatibility dependency, then run the
public v2 retirement qualification and the source fixture against the installed
CLI/module boundary. Verify packaged v4/v5 schema readers and no provider or
retained-QA activity.

## Slice 4 — Release preparation — Pending final approval

Record the candidate hash, focused and installed qualifications, exact package
resource checks, known optional-schema environment limitation, and scope. Do
not tag, publish, or mutate retained QA until explicit final approval.
