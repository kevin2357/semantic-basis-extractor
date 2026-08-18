# Slice 2 — Bounded Six-Pass Packet Evidence

Date: 2026-08-18  
Status: complete; awaiting gate review

## Outcome

Bounded Natal now has a deterministic editorial topology independent of provider
transport: five isolated ten-card passes and one isolated summary/theme pass. The
compiler emits a strict split assignment plus six minimized pass packets under the
new v2 run identity.

This slice does not submit or reconcile provider work. The v2 artifacts become the
input to interactive execution in Slice 4 and Batch transport in Slice 5.

## Frozen behavior

- Every one of the 50 selected claim IDs appears in exactly one card pass.
- Assignment is deterministic for the frozen policy, subject, and canonical claim
  deck while balancing claim families and avoiding homogeneous adjacency.
- The summary pass contains no authorable card claims; it receives the frozen four
  summary fields and the same minimized whole-dog context.
- Every provider view contains only allow-listed subject data, bounded authority,
  relevant selected terms, editorial resources, and the context required for its
  isolated task.
- Provider transport is not encoded in a pass packet. Interactive and Batch must
  consume the same frozen logical packet later.
- Reassembly accepts pass results in any arrival order but restores canonical claim
  and summary ordering deterministically.

## Packaged contracts

- `bounded-natal-split-assignment-v1.schema.json` validates the assignment identity,
  deterministic seed/policy, five-by-ten membership, summary pass, and digest.
- `bounded-natal-authoring-pass-packet-v1.schema.json` validates each self-contained
  pass view and rejects undeclared transport or provider fields.
- Both contracts are discoverable from the packaged contract catalog.

Native validation additionally proves cross-artifact facts that JSON Schema alone
cannot express: exact deck closure, ordered pass membership, registry equality,
resource identity, canonical digest, and provider-visible minimization.

## Test evidence

Desktop focused command covered bounded authoring, provider construction/product QA,
and lifecycle regression surfaces:

```text
Ran 39 tests in 45.660s
OK
```

The Python 3.11 Linux worker image independently ran the bounded-authoring suite:

```text
Ran 12 tests in 0.560s
OK
```

Generated evidence comprised one split assignment plus six pass packets; all seven
instances validated against their packaged schemas. Mutation tests cover added
transport guesses, membership changes, duplicates, missing members, order changes,
and incomplete result sets.

Provider operations: 0. Spend: USD 0.

## Deliberate boundary

The existing lifecycle still creates historical bounded v1 one-operation state.
Slice 2 changes compilation only. Slice 4 must explicitly admit the v2 six-pass
execution model, and legacy v1 workspaces must fail closed rather than acquire
fabricated pass history.
