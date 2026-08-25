# Sprint Log

## 2026-08-25 — Full saunter plan prepared

Created as the SBE companion to API Sprint 45 after fresh QA external-authority
v2 invocations returned `ambiguous_submission`. No implementation, provider
activity, retained-run mutation, or release occurred.

Expanded the initial skeleton into a complete five-waypoint saunter plan after
tracing the current production CLI and dispatcher boundary. The current
hypothesis is now explicit: `CALL_ENTERED` is persisted before the callback
performs local payload resolution and provider setup, so deterministic local
failures can be conservatively but incorrectly collapsed into provider ambiguity.

The plan requires evidence-based execution phases rather than exception-type
classification, strict public outcomes and joins, provider-free failure
injection, installed-wheel qualification, and four joint review checkpoints.
Implementation remains paused before Scenic Waypoint 0 pending owner/API review.

## 2026-08-25 — Plan approved; Scenic Waypoint 0 opened

Owner and API approved the saunter direction. API decisions incorporated:

- use a fresh closed command-result schema version;
- make `pre_provider_refusal` an explicit outcome;
- use a closed provider-I/O/custody assertion rather than a boolean;
- preserve API ownership of reservation/admission identity and policy;
- retain all review checkpoints; and
- publish the complete requested sanitized consumer-fixture matrix.

Scenic Waypoint 0 is authorized to begin provider-free boundary tracing and
failure injection. No retained QA or real provider work is authorized.

## 2026-08-25 — Scenic Waypoint 0 initial reproduction

Added a production-shaped provider-free regression that separates entry into the
dispatch callback from entry into the scripted provider transport. Removing the
exact prepared payload causes local request materialization to fail after the
current durable `CALL_ENTERED` checkpoint. The transport call count remains zero,
but 0.4.22 returns `ambiguous_submission`, persists
`AMBIGUOUS_PROVIDER_SUBMISSION`, and reports provider I/O as performed.

The companion before-entry test proves the immediately preceding failure point
remains replayable and makes zero callback/provider calls. The full boundary
inventory remains in progress before Waffle Checkpoint 0.

## 2026-08-25 — Scenic Waypoint 0 complete

Completed the boundary inventory and froze the public CLI reproduction. The
recommended correction is a prepared-create value built before the fence plus a
transport-only operation after it. Classification is thereby determined by the
durable execution phase, never by exception class.

Recommended versioning is provider dispatch result v3 embedded by command result
v2. Historical v2 ambiguity remains review-only.

Focused provider-free gate: 25 tests passed. No source/runtime behavior changed.
Paused at Waffle Checkpoint 0 for API review before schemas or implementation.

## 2026-08-25 — Scenic Waypoint 1 complete

Recorded API's Waffle Checkpoint 0 approval and implemented the proposed public
contract without changing dispatch runtime behavior:

- provider dispatch result v3;
- external-authority v2 command result v2;
- explicit `pre_provider_refusal`;
- closed provider-I/O and grant-invocation dispositions;
- closed refusal and ambiguity reasons;
- ordered prepared-create digest evidence;
- strict Python validators independent of `jsonschema`;
- packaged JSON Schemas;
- public builders/readers/validators; and
- packaged sanitized positive/negative fixture matrix.

Focused gate using the existing qualified 0.4.22 environment: 30 tests passed,
including Draft 2020-12 schema validation. Dispatch still emits the historical
v2/v1 result pair; no production classification changed in this waypoint.

Paused at Waffle Checkpoint 1 for joint schema/authority review before runtime
execution-path correction.

## 2026-08-25 — Scenic Waypoint 2 corrected after API review

Implemented phase-aware provider dispatch: deterministic payload/provider
preparation occurs before the durable call fence, the prepared-create digest is
revalidated against the unchanged snapshot under the writer, provider I/O runs
outside the writer, and returned identity or ambiguity is checkpointed before
the next member.

The first review run found two real gaps. A refusal reset only its causal member,
leaving the untouched suffix under the sealed aggregate grant, and the CLI
converted a missing returned provider ID into a generic transport exception.
The correction now seals the complete invocation, archives and restores every
provably unentered suffix member, preserves any provider-bound prefix, enables a
fresh inspection/request/grant path, and lets the dispatcher classify malformed
returned identity explicitly.

Checkpoint drift between preparation and call-fence persistence is now the
closed pre-provider refusal `checkpoint_changed_before_create`. The old grant is
sealed, no provider call occurs, and replay is exact.

Focused provider-free gate after the requested non-vacuous three-member
prefix/refusal/suffix addition: 35 tests passed. Paused at Waffle Checkpoint 2 for
re-review before consumer surfaces.

Repeated focused execution also exposed a pre-existing Windows fixture/runtime
integrity race: authoritative snapshot publication could reuse a process hash
cache entry after a temporary absolute path was removed and recycled with the
same size and coarse modification timestamp. Snapshot validation correctly
bypassed the cache and therefore intermittently refused the newly written
manifest. Snapshot publication now also hashes current bytes without the process
cache; the cache remains available only for non-authoritative inventory callers.

## 2026-08-25 — Scenic Waypoint 3 consumer surfaces complete

Added the provider-free `astrowoof-provider-dispatch-result` command for strict
validation/export of dispatch v3, command result v2, and the packaged sanitized
fixture bundle. The command accepts no workspace, provider, credential, grant,
response ID, or submission option. Added the contract identities to the packaged
catalog, a consumer handoff and hash manifest, and command-level tests.

The phase boundary now emits the existing closed, redacted
`external_authority.refused` event for pre-provider refusal and concise text
classification logging. Diagnostic sink failure is isolated from snapshot,
action, authority, provider-call, and result behavior.

Focused Waypoint 3 gate: 17 tests passed. Paused for Waffle Checkpoint 3 API
fixture/adoption review before installed-wheel and release qualification.

## 2026-08-25 — Waffle Checkpoint 3 correction complete

Factored one strict fixture-bundle value validator shared by packaged reading and
the CLI `--input` path. Empty bundles, extra root keys, malformed case envelopes,
duplicate names, and expectation mismatches now fail before output is written.
Added the validator to the supported root-level Python surface and added CLI
regressions for empty and extra-key bundles.

Focused correction gate: 16 tests passed. Waffle Checkpoint 3's conditional
approval is satisfied; Scenic Waypoint 4 release qualification may begin.

## 2026-08-25 — Scenic Waypoint 4 release candidate qualified

Committed candidate source at
`9f3e3874aee74099b7c1a43b5094fe55c8426fb3`, bumped to fresh version 0.4.23,
and built twice with `SOURCE_DATE_EPOCH=1787666725`. Both 980,621-byte wheels
are byte-identical at SHA-256
`adf16ecc785c2eeb98bcc1b4ed77d49bba0f208a1943c58e74320b2eed5135de`.

The installed wheel passed exact SPC 0.11.1 dependency validation, `pip check`,
provider-free packaged fixture validation/export, and the generic installed
release smoke through `DELIVERY_COMPLETE`. The one broad source suite completed
with 719 passed and 3 expected skips.

No provider/network call, credential, spend, or frozen-QA access occurred.
Paused at final Waffle Checkpoint 4; tag and publication are not authorized yet.

## 2026-08-25 — Final Waffle Checkpoint 4 approved

API independently reviewed the candidate and reran the focused consumer/runtime
gate: 18 passed with one expected optional-schema skip. Final approval required
only correcting stale candidate/pending wording in the normative handoff and
labelling the old Waypoint 1 questions as resolved decision history. Those prose
corrections are complete. Owner and API authorized immutable 0.4.23 tagging and
publication; no runtime or artifact rebuild is required.
