# AstroWoof Natal Authoring 0.4.23

Status: release candidate qualification in progress

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

Qualification evidence and immutable artifact identity remain pending final
Waypoint 4 review.
