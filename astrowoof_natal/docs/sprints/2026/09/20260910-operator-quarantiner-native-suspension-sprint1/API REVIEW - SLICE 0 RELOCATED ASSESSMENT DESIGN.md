# API review — Slice 0 relocated assessment design

## Decision

**Approved in principle.** The additive, read-only relocation wrapper is the
right boundary for the operator-runner quarantine path. It resolves the
historical `disposition_assessment_unavailable` seam without weakening the
absolute-path invariant on any executable native workspace and without
mistaking a copied checkpoint for writer authority.

The API will own the durable request/replay record, archive/checkpoint proof,
request-owned restore directory, wrapper persistence, and any later mutation.
SBE remains the exclusive owner of native evidence interpretation and the
nested v1 custody/posture classification.

## Points confirmed

1. A wrapper around an unchanged
   `astrowoof.operator_disposition_assessment.v1` is preferable to a v2
   reissue. Relocation changes evidence-view provenance, not custody
   semantics.
2. `archive_sha256`, checkpoint identity/generation, and inventory truth are
   API-proven claims. SBE must validate the restored members and supplied
   authority joins, but must not imply it reconstructed the original archive
   bytes from an extracted directory.
3. The separate public relocated reader and separate relocated snapshot
   validator are required. The ordinary reader/validator and every executable
   public command must retain the existing physical-root equality rule.
4. Exact-request, exact-checkpoint freshness and the closed no-I/O/no-mutation
   capability fence are necessary. There must be no latest-object discovery,
   fallback path discovery, or writer-lock acquisition.
5. A returned wrapper is assessment evidence only. It does not authorize
   quarantine; API independently validates/persists it and applies any later
   custody mutation under its existing operator authorization and transactional
   rules.
6. The proposed real API/SBE integration gate is required. Fake restore or
   reader doubles remain unit coverage only and cannot prove the deployed
   boundary.

## Small freeze-time clarifications

- Define the logical-root digest input precisely as the existing canonical,
  normalized logical-root string representation—not an OS-dependent raw path
  spelling. The SBE implementation should compare canonicalized values before
  calculating the two root digests.
- API will create `request_id` once and make it immutable: the same request ID
  may replay only the same canonical authority digest. A different authority
  (including a later checkpoint generation) requires a new request ID.
- `issued_at`/`expires_at` should be unambiguously UTC RFC 3339 instants. API
  will choose the bounded window; SBE must check validity both before and after
  the fenced read.
- The wrapper's `assessed_at` must be supplied/frozen by API for deterministic
  qualification, while live operation may set it immediately before the read.
  Its digest calculation must be specified alongside the authority digest so a
  replay cannot silently rebind metadata.
- Preserve the optional `terminal_result_id` only as an exact selector when it
  is already part of the API request. It must never trigger terminal-result
  discovery. If no exact selector was provided, ordinary v1 semantics must
  either classify from the permitted immutable state or refuse.
- A valid v1 `prohibited`/`unsupported` posture remains a successful
  assessment result; malformed, contradictory, or unproven evidence is a
  refusal. Keep those two outcomes distinct for the API operator UX.

## API contract impact

No existing executable workspace, generation, paid-action, provider,
publication, or normal lifecycle contract changes. The companion API work will
add a narrow request/authority/wrapper persistence boundary and invoke this
reader only after an exact checkpoint restoration. The final quarantine command
will continue to fail closed if no valid relocated assessment is durably bound
to its exact request/checkpoint.

With the clarifications above captured in the schema/fixtures, SBE may freeze
the additive schemas and proceed to implementation.
