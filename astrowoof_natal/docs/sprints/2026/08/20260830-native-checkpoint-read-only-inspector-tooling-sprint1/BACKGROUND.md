# Background — native checkpoint read-only inspector tooling

## Why this sprint exists

Recent retained-QA investigations repeatedly needed the same cross-repository
forensic sequence:

1. API/operator authority identifies one exact immutable checkpoint object and
   authorizes a bounded download.
2. The downloaded archive is validated for content identity, archive safety,
   compatibility, declared inventory, member sizes, and member hashes.
3. The restored native workspace is inspected without executing resume,
   reconciliation, repair, publication, or provider work.
4. Investigators manually join native state, spend ledger, lifecycle evidence,
   retry lineage, result history, receipts, snapshots, and journal ranges.
5. A sanitized evidence packet is assembled for cross-repository review.

This worked, but each incident required new glue. During the Moxie terminal-
review investigation, an attempted use of API's production checkpoint restore
helper was excessively slow in the local instrumented runtime, so the same
closed validation had to be assembled from native archive tooling and explicit
member-hash verification. Publication validation then required a second SBE-
specific tool. The result was correct, but the workflow should be a supported,
repeatable capability rather than an incident-specific kayak.

## Desired capability

Provide an installed, provider-free, read-only SBE inspection surface for a
checkpoint archive already present on local disk. It should:

- validate archive identity and safety;
- validate and optionally restore the exact declared workspace inventory;
- validate native snapshots, journal ranges, results, receipts, and checkpoint
  bases without changing native truth;
- produce closed, sanitized projections of run state, paid actions/custody,
  retry lineage, lifecycle/result history, and publication provenance;
- identify contradictions without prescribing API scheduling or resource
  disposition; and
- emit a concise, immutable inspection receipt suitable for incident evidence.

## Ownership boundary

The inspector does **not** own remote-object discovery or authorization.

- API/operator tooling owns R2 coordinates, credentials, download authority,
  retention, API action/binding documents, leases, capacity, reservations,
  settlement, and recovery decisions.
- SBE owns validation and interpretation of supplied native checkpoint bytes.
- The inspector accepts a local archive and expected identities. It never lists,
  downloads, writes, copies, or deletes remote objects.
- Any comparison with API actions accepts a separate public join document; it
  never reads PostgreSQL or reconstructs API-private state.

## Safety posture

- Provider-free and credential-free.
- No OpenAI/provider transport import or invocation.
- No native writer lock, resume, reconciliation, repair, denial, closeout, or
  result publication.
- Extraction only into a caller-approved empty directory or an automatically
  managed temporary directory.
- Archive path/type/size/count bounds enforced before extraction.
- Private prompts, payloads, generated content, authorization documents, and
  subject details excluded from public output.
- Unknown versions and contradictory evidence fail closed.
- Inspection findings are evidence, not recovery authority.

## Relationship to current investigations

The Moxie investigation remains independent and should finish its causal and
ownership classification first. Its one-off scripts are characterization input,
not the final API. This tooling sprint should incorporate lessons from Moxie and
earlier retained-workspace investigations, then publish a stable general surface.

No source change, version bump, release, remote access, or retained-workspace
operation is authorized by this background document.

## Additional input from the Delerium polish-v2 investigation

The inspector must eventually support identity analysis where several lifecycle
or external-authority observations surround one native action. Its sanitized
projection should make the following independently queryable without exposing
payloads or authorization documents:

- stored and recomputed lifecycle/temporal inspection identities;
- checkpoint basis, observation time, and ordered authority inventory;
- external-authority request kind/digest and its exact inspection join;
- native action state, binding digest, provider-presence, consumption-presence,
  and v2 intent membership;
- grant and authorization-document references/digests when supplied in a
  separate public join document; and
- closed distinctions among immutable-object mismatch, different-observation
  identity, native dispatchability contradiction, and unavailable evidence.

The tool must not describe several observed digests as mutation of one request
unless the retained bytes prove that statement.
