# API Agent Scenic Waypoint 0 Review

Status: approved to proceed to Scenic Waypoint 1

## Assessment

The provider-free reproduction establishes the decisive fact: current
`CALL_ENTERED` means only that the dispatcher called a broad callback, not that
the callback reached provider transport. A missing prepared payload produces
zero scripted transport calls while persisting native ambiguity. That is both
safe against duplicate work and too coarse for API custody/scheduling.

The recommended split between deterministic prepared-create materialization and
a transport-only callable is approved. It makes classification depend on a
durable execution phase and direct call evidence rather than exception class.

## Frozen API decisions

1. **Versioning:** publish a fresh closed pair:
   - `astrowoof.external_authority_provider_dispatch_result.v3`; and
   - `astrowoof.external_authority_v2_command_result.v2` embedding dispatch v3.

   Existing exact-key validators make silent additive extension unsuitable.
   Historical dispatch v2 ambiguity stays review-only; API must never infer that
   it was a proven pre-provider failure.

2. **Provider-I/O assertion:** use a closed value, not a boolean. The consumer
   vocabulary should be semantically equivalent to:

   - `not_attempted`;
   - `create_entered_unknown`; and
   - `provider_identity_durable`.

   The result schema must reject contradictory pairings, including
   `pre_provider_refusal` with anything other than `not_attempted`, or detached
   provider-pending work without durable provider identity inventory.

3. **Pre-provider refusal and the exact grant:** a proven pre-provider refusal
   seals the *specific invocation/grant attempt* as refused. It must not leave
   that exact grant replayable, and it must not implicitly issue/reuse a grant.
   It does **not** itself terminalize the whole native action or run. A later
   attempt requires a fresh supported lifecycle inspection and a fresh explicit
   API authority decision. This preserves the audit record while avoiding a
   duplicate-call risk or an invisible automatic retry.

4. **Prepared-create evidence:** the durable call fence should bind a safe
   digest/identity for the prepared material and unchanged checkpoint basis, but
   must not expose request payloads, credentials, or protected provenance in
   public results. Provider construction/materialization must itself be proven
   non-I/O before it is treated as pre-fence work.

5. **API dispositions:**
   - pre-provider refusal: release execution capacity and any unspent action
     reservation only under the `not_attempted` proof; retain the failed grant
     and audit basis; no automatic retry;
   - ambiguous submission: release execution capacity, retain review custody,
     and permanently prohibit new provider creation for the ambiguous action;
   - detached provider-pending: ordinary retrieval-only custody;
   - exact replay: no API mutation; and
   - malformed/contradictory evidence: fail closed, distinct from recognized
     ambiguity.

   API's user/operator-facing disposition for recognized ambiguity should be
   specific (for example `provider_submission_ambiguous_requires_review`), not
   generic artifact integrity.

## Requested Scenic Waypoint 1 fixture matrix

Publish sanitized, packaged fixtures for:

1. missing/duplicate/digest-mismatched payload before the fence;
2. invalid local transport/provider configuration before the fence;
3. failure immediately after durable call entry;
4. transport-entered failure;
5. missing, malformed, or conflicting returned provider identity;
6. normal detached provider-pending work;
7. exact replay; and
8. malformed or contradictory public/sealed evidence.

API will join its own reservation/admission identity from its durable records;
SBE need not and must not assert API-global reservation facts.

## Checkpoint result

Approved. The planned joint review immediately after the schema/authority freeze
is the correct next pause.

