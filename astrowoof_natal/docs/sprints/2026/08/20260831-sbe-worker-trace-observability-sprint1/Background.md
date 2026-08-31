# Background — SBE worker trace observability

Recent QA investigations repeatedly required downloading an exact retained R2
checkpoint and writing or adapting an offline parser to recover nearly the same
facts:

- which native checkpoint and snapshot the worker restored;
- which lifecycle branch SBE selected and why;
- the ordered action inventory and action-state distribution;
- retained provider custody and the SBE-selected due subset;
- completed provider evidence awaiting local adoption;
- retry lineage and local-work progress;
- live, retired, completed, or ambiguous external-authority v2 intent;
- terminal/review result and receipt continuity; and
- the exact public artifact SBE returned to API before process exit.

The existing `✨🐶` Python logging was indispensable when it happened to cover
the failing boundary. Coverage remains uneven, however. Some decisions are
visible only as a terse status, some public handoffs do not log their complete
safe identity, and historical reconstruction often begins with a workspace
download because logs do not establish the exact restored basis.

This sprint implements the SBE-focused trace work tracked by AstroWoof control
room issue #11. It does not replace authoritative lifecycle/result contracts,
redesign structured events, or eliminate the read-only checkpoint inspector.
Its aim is to make workspace forensics the exceptional fallback rather than the
normal first step.

## Owner decision

Log a sanitized workspace fingerprint immediately after SBE has opened and
validated the restored workspace, and again when SBE publishes or returns a
new authoritative checkpoint/result. The fingerprint is an identity summary,
not a dump of the workspace.

Safe candidates include:

- native run ID;
- route and public contract/version identity;
- logical workspace-root digest or other non-path identity;
- checkpoint generation/object identity when supplied in native metadata;
- state revision;
- snapshot, archive, inventory, and checkpoint-basis digests where available;
- installed SBE/SPC compatibility identity; and
- restore/snapshot-validation outcome.

Never log signed URLs, credentials, absolute restored paths, prompts, generated
content, provider payloads, complete bindings or authorization documents,
source archives, or subject data.

## Relationship to other observability tracks

- API trace logging owns queue, lease, custody, mapper, subprocess, ingestion,
  and API resource-release decisions.
- The deterministic trace parser owns deterministic-worker log interpretation.
- The structured-event checkup owns event taxonomy, forwarding, retention, and
  schema coverage across repositories.
- The R2/native checkpoint inspector remains the exact historical/crash and
  persistence-integrity fallback.

Logs remain descriptive, lossy, and non-authoritative. API must consume and
validate the referenced public artifact rather than act on a trace line.
