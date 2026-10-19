# Gate A research — proving which attempt produced a native publication

> **Historical research, not an alpha release requirement.** The narrowed
> scope and containment expectations are in [Slice 0C](SLICE%200C%20-%20ALPHA%20SAME-CALL%20HANDOFF%20AND%20CONTAINMENT.md).
> Candidate A/B and attempt-keyed automatic reconstruction are deferred;
> retain their cautions against guessing and reattribution.

**2026-10-18. Design research only; not a frozen contract or implementation.**
This responds to [API's v2 review](API%20AGENT%20-%20GATE%20A%20CONTRACT%20REVIEW%20V2.md).
API approves the direction for research, but matching field/argv/time handoffs
and joint Gate A approval are still required before implementation.

## The exact ambiguity

API is right: if attempt A leaves an anchor in the workspace and attempt B
later publishes, B's retained snapshot can contain **both** anchors. Given
only “A's anchor occurs in B's snapshot,” an attempt-keyed sidecar could
incorrectly associate A with B's result and receipt. A valid receipt, snapshot
digest and self-hashed sidecar do not independently prove the claimed causal
association. A reader needs a **publication-specific reference** to one
attempt, not merely the set of anchors present at publication.

## What the current code gives us—and does not

- `native_transitions.py::publish_native_execution_result` mints a native
  invocation ID during publication, appends hash-chained journal records,
  computes a checkpoint basis, writes the result and workspace snapshot,
  then writes the receipt and retained copies. The receipt binds the native
  result, invocation, journal range, checkpoint basis and snapshot. It does
  **not** bind API's `supervision_invocation_id`.
- `checkpoint_basis` excludes native results/index and the ordinary snapshot
  inventory excludes publication receipts, but regular workspace files can be
  members of both basis and snapshot. `read_native_transition_result` checks
  the exact result, receipt, retained snapshot digest and retained basis digest;
  it does not currently verify an API attempt link.
- The ordinary result v0.1, terminal-review result v0.2 and journal v0.1
  validators use closed top-level fields. In particular, terminal-review
  `projection_refs` must be empty in both SBE and API; it is **not** an
  available place to smuggle a supervision ID. API checks journal record shape
  and hash chain, but it does not currently interpret an attempt binding.
- `reconciliation.py::_single_writer` and
  `lifecycle.py::_exclusive_lifecycle_lock` both use the
  `spend-consumption.lock` single-writer boundary. However, the current
  coordinator does not hold one continuous writer lock across retrieval,
  local continuation and the later `publish_native_execution_result` call.
  A new pre-seal association cannot assume that continuous exclusion already
  exists; nested acquisition and lock ordering require explicit design.
- Publication already has repair for an incomplete receipt and an unsealed
  journal tail, and a terminal-review exact-replay branch can return an
  **existing** sealed result. Those paths do not currently establish which
  API supervision attempt owned the publication. They cannot silently assign
  an older result to a different attempt just because it is returned again.

## Candidate A: a publication-specific singleton slot

One candidate worth testing—not yet proven or selected—is a versioned,
closed **active-publication slot** at one fixed, non-excluded workspace path.
Under an exclusive publication writer boundary:

1. Validate the API prelaunch envelope and the selected decision/route/profile.
   Allocate or recover **one** SBE native publication invocation ID for this
   attempt, and durably record a closed immutable attempt anchor. The API
   `supervision_invocation_id` identifies the child command; the native
   publication ID remains a separate SBE identity. The anchor binds both,
   the exact command digest and decision/route/profile references.
2. Write one canonical active-slot document referring to that exact attempt
   anchor **and** native invocation. The slot must be included at its fixed
   path in both the result's retained checkpoint basis and receipt-retained
   snapshot. Its bytes or an exact reconstructible canonical representation
   must be retained with the publication so the reader can verify its SHA even
   after a later attempt replaces the live slot. The receipt-excluded evidence
   area is a possible location for those retained bytes, not an automatic
   guarantee of remote durability.
3. Seal the native result using the same native invocation ID as the slot;
   validate the closed result and receipt, their journal range and basis, and
   the exact singleton slot in *that result's retained evidence*. Then publish
   a closed attempt-keyed mapping and typed stdout companion. The validator
   must compare the slot/anchor, SBE result/receipt, API prelaunch identity and
   exact decision/predecessor; a mapping or path name alone is not authority.
4. Verify A→native invocation→result/receipt and the reverse association are
   unique. Attempt A's old anchor can remain a snapshot member while B's
   **single slot** names B; an A→B mapping must be refused even though A's
   anchor is present. Use an exact attempt/result selector, never latest.

This is stronger than simple anchor membership because the *specific slot at
the fixed path in that publication's retained evidence* identifies the claimed
attempt and native invocation. It is a contract candidate, not a formal proof
that current code provides the association. It also does not make SBE's local
disk remotely durable or convert hashes into cryptographic authentication
against an untrusted writer; API must validate the writer/authority boundary.

### Challenges that could rule out Candidate A

- Native invocation must be allocated and durably bound before sealing, then
  explicitly supplied to or safely recovered by the publisher; the current
  function mints/repairs it internally. Any change to the published caller or
  journal replay must preserve closed schemas and exact-route behavior.
- The anchor, singleton slot and corresponding publisher must share a real
  writer exclusion boundary. Do not hold the same non-reentrant byte lock
  twice, call `_writer_held=True` without proof, or assume local continuation
  is already covered by the publication lock.
- If a prior terminal review result is reused or an incomplete result/journal
  is repaired, validate the **original** attempt and invocation. A new
  attempt cannot claim an old result merely by installing its own slot. Agree
  whether such cases return an explicit prior-publication reference under
  separately validated authority, or fail closed; do not mint duplicate
  terminal results solely to make the new mapping convenient.
- A crash after result or snapshot but before receipt, or after receipt but
  before sidecar, must recover only when the persisted slot/anchor, native
  journal, result and receipt uniquely agree. If any material link was not
  captured in recoverable state, remain unresolved. Checkpoint archive/restore
  must carry both the retained slot evidence and sidecar and verify them at the
  correct logical root. A lost local workspace before remote checkpoint is
  still a loss; a local file is not a remote recovery promise.
- `not_due` must stay mutation-free: no new active slot, anchor, native result
  or successor checkpoint just to represent no publication. Loss of its
  stdout does not prove the command was not due.

## Candidate B: explicit versioned native publication binding

If the singleton-slot design cannot establish the association and recovery
rules with existing closed results, use a deliberately versioned native
journal/result or other native publication contract that explicitly includes
the API attempt/anchor digest and native invocation in the hash-bound
publication. This is semantically clearer but may require changes in SBE's
public exact readers, terminal-review result/command contracts, API validators
and downstream consumers. Preserve the old contracts and route old work to
its compatible release context; never alter the interpretation of v0.1/v0.2
or pretend a new result has the old identity. No particular successor schema
number or cross-repo compatibility is asserted here.

## Decision and required tests

Recommend investigating Candidate A first because the existing retained basis
already has a hash-bound member inventory, but use Candidate B if the required
one-to-one association, old-terminal replay or actual restore cannot be proved
without weakening validation. This is a **research preference**, not approval
to implement A or evidence that it works.

The joint contract must freeze the active-slot/anchor/binding fields and
canonical bytes/digest, identifier uniqueness, exact-reader semantics, allowed
argv and output cardinality, and actual child/parent time semantics. API must
specify how its persisted prelaunch capability is joined without exposing the
capability, and how lease/fence authority gates recovery. The fake-provider
joined matrix must at minimum prove:

1. Two attempts on the same run, with A's anchor retained in B's snapshot:
   B binds only B; A→B and a slot/invocation/result mismatch are refused.
2. Terminal delivery, terminal review and nonterminal transition; older and
   newer valid publications; exact no-publication output and no mutation.
3. Wrong attempt/run/route/profile/argv/decision, altered slot bytes or digest,
   changed retained basis/snapshot, duplicate conflicting mappings, copied
   sidecars and wrong receipt: all fail closed.
4. Failure and authorized restart between anchor, slot, journal append, result,
   snapshot, receipt, sidecar, stdout, archive and remote checkpoint; exact
   replay versus old-terminal reuse; no invented identity or duplicate create.
5. Real API checkpoint archive/restore and exact reader, including loss of
   local workspace before/after durable remote checkpoint. No provider I/O.
6. Exact-route and shared-reader/terminal review regression, including old
   releases and worker-context compatibility.

Gate A remains open. No code, tests, provider calls or live state were changed
as part of this research.
