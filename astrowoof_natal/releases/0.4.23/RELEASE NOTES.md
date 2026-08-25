# AstroWoof Natal Authoring 0.4.23

Status: release candidate qualified; tag/publication pending owner and API review

SBE 0.4.23 makes the external-authority v2 provider-create boundary
machine-distinguishable. Deterministic payload/configuration preparation now
occurs before the durable call fence. Proven pre-provider refusal is distinct
from post-fence submission ambiguity, durable provider-pending custody, and
exact replay.

The release adds provider dispatch result v3, external-authority command result
v2, strict Python and JSON Schema validation, sanitized fixtures, and the
provider-free `astrowoof-provider-dispatch-result` validation/export command.

Historical ambiguity is not reclassified. The provider API's irreducible
submission/identity-persistence gap remains explicit. No result authorizes the
API to infer global reservation, capacity, billing, or product state.

## Qualification

- Artifact source commit: `9f3e3874aee74099b7c1a43b5094fe55c8426fb3`.
- Fixed build epoch: `1787666725`.
- Full source suite: 719 passed; 3 expected environment/opt-in skips.
- Two byte-identical candidate wheels; SHA-256
  `adf16ecc785c2eeb98bcc1b4ed77d49bba0f208a1943c58e74320b2eed5135de`.
- Generic installed release smoke: pass with 50 cards and four summaries.
- Installed provider-free fixture validation/export: pass.
- Exact installed dependency: `semantic-projection-core==0.11.1`; `pip check` pass.
- External provider/network calls and spend: 0.
- Frozen QA cohort access/mutation: 0.

Tagging and publication remain pending final Waypoint 4 authorization.
