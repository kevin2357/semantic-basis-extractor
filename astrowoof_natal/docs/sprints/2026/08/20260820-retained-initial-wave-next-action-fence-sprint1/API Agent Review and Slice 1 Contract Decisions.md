# API Agent Review and Slice 1 Contract Decisions

Date: 2026-08-20  
Status: approved direction for Slice 0 and Slice 1 contract design; implementation remains subject to the stated review gates

## Overall review

The proposed sprint accurately isolates the gap exposed by Aster.  SBE 0.4.13
can classify the current lifecycle branch, but it does not publish an exact,
run-specific native authority that an API consumer can validate *before*
provider-capable continuation.  A generic resume therefore had room to infer a
fresh six-member wave from incomplete retained state.  API's post-publication
validation was correctly conservative, but necessarily too late to prevent the
six provider creates.

The proposed lifecycle v0.5 request plus native single-writer continuation fence
is the right repair.  The API agrees with the stated ownership boundary,
three-way distinction (fresh / exact retained continuation / unjoinable
lineage), and the requirement that Aster itself remain evidence only.

No API-side plan change is required before SBE Slice 0.  API Sprint 33 remains
an intentionally conservative pre-invocation fence until this public contract
is released and jointly qualified.

## Slice 1 decisions

### 1. Publish the complete request inline in lifecycle inspection v0.5

Use a closed `external_authority_request` object embedded in the v0.5 lifecycle
inspection.  Do not make API retrieve or join a second run-local artifact to
discover the primary next action.

Six complete public bindings are small relative to the inspection and the value
is precisely that one snapshot-validating public read answers: *what exact
authority may this invocation consume now?*  The request's canonical digest is
still mandatory, and a supported CLI export may write the same canonical object
for evidence or inter-process handoff.  That export is a representation of the
inspection object, not a second source of truth.

It is appropriate for the request to reference the existing prepared-wave and
binding-bundle identities for an initial wave.  It must not duplicate prompts,
request bodies, subject data, provider payloads, or private workspace fields.

### 2. Require a small aggregate API grant envelope

Existing per-action authorization documents plus only a bare request digest are
not sufficient as the public cross-repository continuation boundary.  Add a
small, closed API-issued aggregate response envelope, provisionally named
`astrowoof.external_authority_grant.v1`.

The grant should bind at least:

- the complete `external_authority_request_sha256`;
- native run ID, inspected state revision, snapshot identity, and logical root;
- request kind and the exact ordered action IDs;
- the corresponding per-action authorization document digests/references;
- an all-or-nothing decision (`granted` only when every required member is
  authorized);
- the API decision/issuance identity and a canonical grant digest.

For an initial wave it should also repeat or bind the wave ID, wave digest, and
ordered member binding digests.  SBE must reject a partial grant, missing or
extra member, reordered member, request mismatch, or authorization-document
mismatch before native mutation or provider I/O.

This envelope avoids an undocumented API-side or SBE-side join of six ordinary
documents, makes the all-or-none initial-wave admission explicit, and gives
both systems one stable replay identity.  Per-action documents remain useful
and authoritative at their own boundary; the envelope is their aggregate
authorization for this one native invocation.

### 3. Ordinary action-set ordering: lexical action-ID order

For `ordinary_action_set`, use ascending lexical `action_id` order as the
canonical order used by the request digest and grant.  It is stable,
implementation-neutral, and does not imply dependency or provider execution
order.  The request should explicitly state that its order is canonicalization
only.

Initial-wave order is different: retain the prepared wave's existing ordered
six-member inventory exactly.  It is semantic evidence, not merely a digest
convenience.  Never silently sort wave members by action ID.

### 4. Unjoinable historical initial-wave lineage: a distinct typed refusal

Use the machine-readable reason code
`initial_wave_lineage_unjoinable` for the condition where prior initial-wave
or provider lineage exists but cannot be joined to one exact, snapshot-valid
inventory.  It must be distinguishable from both stale observation and provider
ambiguity.

Recommended lifecycle shape:

- select a non-provider-capable, non-eligible refusal branch (rather than
  `await_external_authority`);
- set `external_authority_request` to `null`;
- publish a closed `external_authority_refusal` object with this reason code,
  `provider_create_permitted=false`, and a redacted closed evidence-category
  vocabulary such as `prior_initial_action`, `prior_provider_identity`,
  `prior_consumption`, `response_evidence`, `ambiguous_lineage`, or
  `missing_join_artifact`;
- identify the disposition as review-required, never automatically recoverable.

This prevents a consumer from treating an empty request as “please authorize a
fresh wave.”  It also preserves the important distinction that SBE has refused
to prove a safe continuation, not proven that no historical work occurred.

### 5. Single-writer fence: hold it through durable pre-submit intent, not slow I/O

The native single-writer boundary should cover all of:

1. revalidate complete snapshot, run/revision/logical-root identity, request
   digest, and exact aggregate grant;
2. revalidate member bindings and native action applicability;
3. atomically apply/record native authorization consumption as applicable; and
4. durably record the exact provider-create intent/operation identity before
   any provider create.

It must **not** be held across the slow provider call.  After the durable
pre-submit checkpoint, release the writer, call the provider, then reacquire
the writer to persist the returned provider identity/result.  A concurrent or
replayed invocation must see the durable pre-submit/in-flight record and may
not create another provider request.

If the process fails after the pre-submit checkpoint but before it durably
records a provider identity, the resulting state is potentially ambiguous.  It
must fail closed into the existing typed reconciliation/review path; neither a
deterministic local key nor an absent local result proves that another create is
safe.  The sprint's failure matrix should cover that precise crash window.

## Additional implementation guardrails

- `provider_create_permitted_after_authorization` is a native capability gate,
  not a promise that provider creation should occur.  It must remain false for
  reconciliation and every refusal state.
- Generic provider-capable `--resume` from any external-authority-needed state
  must fail closed unless supplied with a matching aggregate grant or equivalent
  exact request identity selected by the public contract.  A generic resume may
  remain available for provider-free branches only if its capabilities are
  unambiguous.
- The v0.5 reader must snapshot-validate the embedded request.  The API will
  consume the request through that reader/CLI contract, never through private
  `run.json`, logs, or packet reconstruction.
- The Slice 0 reproduction should include the critical control: a retained
  initial-wave lineage with no joinable current wave must make **zero** create
  calls even if all pass attempts are empty.
- Slice 5 should classify every provider-capable route in an explicit matrix;
  anything not covered by this constrained boundary must fail closed rather
  than inherit generic resume behavior.

## Review gates

The plan's pauses are correctly located.  In particular:

- pause after Slice 0, before freezing the request schema, so API can review
  the real mutation map and last safe preflight point;
- pause after Slice 1, before runtime work, so API can validate the concrete
  request/grant/refusal schemas against its durable authority records;
- pause after Slice 7 for installed-wheel fixture adoption and joint
  transition-oracle review; and
- require explicit Kevin/API approval before publication.

Subject to those gates, API approves proceeding with SBE Slices 0 and 1.
