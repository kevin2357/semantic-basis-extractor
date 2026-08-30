# API Slice 0 review — review-required with pending retries

## Decision

**Approved: proceed to Slice 1's bounded, read-only retained-workspace
provenance inspection once the exact protected checkpoint-authority input and
temporary read-only R2 credential are supplied.** This approval does not extend
to provider access, workspace/API/R2 mutation, recovery, deployment, release, or
any retained-run action.

## What is aligned

- The investigation correctly treats `review_required` as an editorial outcome
  that may coexist with residual provider custody. It does not assume that three
  retry ledger rows form one pass lineage or that every retry must be consumed.
- The frozen Pippin and Duchess API/native IDs, active generations, byte counts,
  and declared-member counts are an appropriate subject boundary. The required
  protected authority file closes the remaining object-selection risk: no R2
  listing, naming heuristic, or nearest-generation fallback is acceptable.
- The `HEAD=2`, `GET=2`, zero-write / zero-provider boundary is appropriately
  narrow. Whole-archive validation before member interpretation, exact member
  membership, hash validation, logical-root validation, and refusal on mismatch
  are all the right posture.
- The planned join is ownership-correct. Native evidence establishes native
  pass/retry/fan-in and durable provider lineage; API records establish the API
  action/provider/reservation projection. A missing join remains `unresolved`.
- The sanitization contract is appropriately conservative. Structural names,
  closed codes, IDs, hashes, and bounded diagnostics may be recorded; prose,
  prompts, protected subject data, secret storage references, and provider
  payloads must remain out of committed evidence.
- The causal alternatives stay genuinely open. In particular, the fact that the
  retained checkpoint contains no sealed `review_required` result must limit
  confidence; it must not be converted into a retroactive native transition.

## Required small corrections before / during Slice 1

1. Update the stale status wording in `EVIDENCE.md`: Slice 0 is complete and the
   current gate is **Voof-paws 1 / Slice 1**, not "awaiting owner review before
   Slice 0." The same distinction is already correctly stated elsewhere.
2. The local inspection-authority input needs the **checkpoint contract and
   compatibility identity values that are actually expected**, not only field
   names. It may obtain them through the protected API metadata lookup, but the
   inspection receipt should record their nonsecret digests/identities and state
   whether the archive matched them.
3. For each timeline claim, retain a compact provenance pointer: native declared
   relative path + member SHA-256, API row/action ID where applicable, and whether
   the conclusion is direct, inferred, unknown, or contradictory. This is
   especially important for the last known state before the missing terminal
   publication.
4. Keep the Slice 1 tool independently constrained from ordinary SBE execution:
   no import/path may invoke a runner, restore a workspace in-place, construct a
   provider transport, or use environment discovery to substitute a different
   storage object. Its only remote primitives should be the specified exact
   object `HEAD` and `GET` operations.

## Causal questions to preserve for Slice 1/2

- Whether final QA/review selection occurred with a **required** retry still
  unresolved, rather than merely alongside an independent retry from another
  pass.
- Whether the provider-created retry's durable provider identity exists in the
  exact retained native evidence and, if so, why the native projection reported
  zero provider-local dependencies.
- Whether the later providerless authorized retry was prepared before terminal
  editorial selection as a valid independent successor, or afterward/stale.
- Whether the decisive review/QA evidence is simply beyond the retained
  checkpoint. If it is, record that as an evidentiary limit rather than turning
  source-code inference into historical fact.

## Gate for the next pause

Pause at Voof-paws 2 with the sanitized timeline, exact lineage/custody joins,
receipt, and confidence-marked causal classification. Do not draft a behavior
change until that review has separated a valid editorial stop, a retry/fan-in
defect, a custody-projection defect, contradictory evidence, and an unknowable
historical cause.
