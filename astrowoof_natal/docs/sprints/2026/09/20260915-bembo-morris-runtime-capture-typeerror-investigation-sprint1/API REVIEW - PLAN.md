# API review — investigation plan

## Decision

Approved to begin Slices 0 and 1 under the stated read-only/provider-free
fences.  The plan frames the evidence correctly and does not presume SBE
ownership merely from the installed callable being the catch boundary.

## Confirmed API findings

The live witnesses establish all of the following for both delivery and review:

- API selected exact public terminal-result authority;
- the observer wrapper and capture phase were entered;
- capture returned the normalized `type_error` failure class;
- API's hashed call-time `workspace` string exactly equals the independently
  emitted SBE `logical_root_sha256` for the same native run;
- the wrapper returned `unavailable`, with zero artifacts; and
- no envelope, request-preflight, or Better Stack HTTP phase was reached.

Accordingly, Slice 0 may exclude an incorrect caller root string and transport
as the present cause.  It should phrase that carefully: matching this digest
proves the exact string passed to capture matched the live SBE logical root; it
does not itself prove every member under that root satisfies packet-builder
assumptions.

## Requested additions to Slice 0/1 evidence

1. Pin **installed** package provenance as well as checked-out source
   provenance.  The diagnostic concerns the exact 0.4.61 wheel/import surface
   present in the worker, so a local source match must be demonstrated rather
   than assumed.
2. Preserve the branch boundary of the first exception: distinguish a
   `TypeError` before `build_editorial_review_runtime_capture`'s assembly
   `try`, within assembly, and while that function tries to turn an assembly
   failure into typed unsupported status.  The plan already identifies this;
   make it an explicit matrix column.
3. For each candidate, record whether it is shared by both delivery and review
   or route-specific.  Common normalized class is useful narrowing, not proof
   of a single line.
4. Retain only safe frame names/line numbers as proposed if an exact retained
   reproduction is later authorized.  Do not add exception prose or paths to
   production events.

## Gate posture

No R2 coordinate packet or read authorization is granted by this review.
If Slices 0–1 cannot identify a tested provider-free defect, return with the
smallest exact coordinate request for each witness and the precise read needed.
No runtime change, release, or retry should begin before that gate.
