# Initial-Wave Binding Bundle Patch Sprint 4 Evidence

## Exact 0.4.8 artifact

- Artifact source commit:
  `4e017dbe16846d57dea0649845c76f9be693b991`.
- Wheel: `astrowoof_natal_authoring-0.4.8-py3-none-any.whl`.
- Bytes / SHA-256: 828,375 /
  `572a46f310b9ea150a49d32705a45e3d0ced501462d2b2743d989ef5b44fb9e1`.
- Two fixed-epoch builds were byte-identical.
- Exact installed Windows/Linux gates: pass.
- Publication explicitly authorized; provider operations / spend: 0 / USD 0.

## Final consumer review

- [API Agent Final Release Review.md](API%20Agent%20Final%20Release%20Review.md)
- Disposition: approved for a fresh immutable 0.4.8, subject only to Kevin's
  explicit publication authorization and post-publication asset verification.
- No implementation, contract, lifecycle, transport, or ownership corrections
  requested.

## Slice 4

- [Slice 4 result](results/SLICE%204%20-%20Cross%20Platform%20Qualification%20and%20Recommendation.md)
- [Machine-readable qualification](results/slice4-qualification.json)
- Qualified source commit: `34de4798be76482dbb9f39a9fd59561bea9f81fe`.
- Two fixed-epoch builds were byte-identical: 828,375 bytes, SHA-256
  `f15d0afc9fd4eaac6c0a48c78af4c0787fef696ecc55a158be5778047e633b1e`.
- Wheel boundary: 118 entries / 71 resources; `py.typed` present; zero tests,
  bytecode, or cache entries.
- Full source suite: 449 passed, 20 expected skips, 469 total.
- Strict Linux contract/bundle/round-trip suite: 36 passed, zero skips.
- Installed Windows 3.12.13 and network-isolated Linux 3.11.15: `pip check`,
  lifecycle smoke, release smoke, exact/bounded joined reader and CLI all passed.
- Provider operations / spend: 0 / USD 0.

## Slice 3

- [Slice 3 result](results/SLICE%203%20-%20Authorization%20Round%20Trip%20and%20Failure%20Matrix.md)
- Exact and bounded integration authorizations now copy their complete bindings
  from the public bundle rather than private ledger state.
- API-shaped provider-free round trips validate the joined public input, create six
  ordinary authorization documents, build the wave envelope, preflight all six,
  and persist six simulated provider identities.
- The mismatch matrix covers membership/order and run/profile/revision/price-book/
  model/request/wave/wrapper conflicts; every refusal performs zero creates.
- Focused gate: 5 passed. Initial-wave public/contract gate: 36 passed with 10
  optional `jsonschema` skips in the base Windows runtime.
- Provider operations / spend: 0 / USD 0.

## Planning evidence

- Released prepared-wave contract: `astrowoof.initial_authoring_wave.v1`.
- Required member authorization contract:
  `astrowoof.provider_spend_authorization.v0.1`.
- Existing complete-binding projection: `spend-authorization-requests.json`, schema
  label `astrowoof.provider_spend_authorization_requests.v0.1`.
- Identified deficiency: no packaged closed schema/validator, no explicit
  wave-ID/digest binding, no frozen ordered inventory, and no supported run-specific
  public reader/CLI.
- Provider operations / spend: 0 / USD 0.
- API Slice 2 review: approved without contract changes.
- [API Agent Slice 2 Review and Response.md](API%20Agent%20Slice%202%20Review%20and%20Response.md)

## Slice 2

- [Slice 2 result](results/SLICE%202%20-%20Public%20Joined%20Authority%20Inputs.md)
- [Consumer review manifest](fixtures/slice2-consumer-review-manifest.json)
- [Installed qualification driver](qualification/slice2_installed_authority_inputs.py)
- Public root reader/CLI returns prepared wave plus binding bundle only after full
  snapshot, individual document, join, and wrapper digest validation.
- Packaged resource hashes are frozen in the consumer-review manifest.
- Public/contract suite: 61 passed in 3.864 seconds.
- Offline strict resolved-schema validation: pass.
- Installed Windows exact/bounded Python and CLI round trips: pass.
- Qualification wheel SHA-256:
  `15068ee064654226a7c05a37cddce18cc0e0ecb28c27b54e7824b1e8f46fd78a`.
- Provider operations / spend: 0 / USD 0.
- API review: approved after freezing one atomic snapshot-validating public pair
  reader for the prepared wave plus binding bundle.
- [API Agent Slice 0 Review and Response.md](API%20Agent%20Slice%200%20Review%20and%20Response.md)
- [Authority-inputs wrapper schema](contracts/initial-authoring-wave-authority-inputs.v1.schema.json)

## Slice 1

- [Slice 1 result](results/SLICE%201%20-%20Native%20Publication%20and%20Snapshot%20Integrity.md)
- Fresh exact and bounded interactive paths publish
  `initial-authoring-wave-binding-bundle.json` from authoritative complete binding
  objects, not reconstructed prepared-wave fields.
- Bundle builder/validator enforces exact fields, canonical digest, action identity,
  six-member order, aggregate commitment, and complete prepared-wave relationship.
- Complete snapshot includes the bundle; one-byte mutation fails validation and
  exact restoration passes.
- Combined wave/exact/bounded suite: 139 passed in 289.799 seconds.
- Final focused regression: 5 passed in 4.810 seconds.
- Provider operations / spend: 0 / USD 0.

Implementation and qualification evidence will be appended slice by slice.

## Slice 0

- [Binding Bundle Contract Proposal.md](BINDING%20BUNDLE%20CONTRACT%20PROPOSAL.md)
- [Proposal schema](contracts/initial-authoring-wave-binding-bundle.v1.schema.json)
- [Slice 0 result](results/SLICE%200%20-%20Contract%20Freeze%20and%20API%20Review.md)
- Exact and bounded complete bindings originate in `action_binding()` and are
  persisted by `prepare_action()` before `build_initial_wave()` projects them.
- Proposal is additive, interactive-only, provider-free, and state-vocabulary
  neutral.
- Proposal/current-wave suite: 18 passed without skips in offline Linux with
  `jsonschema`; base Windows environment passed 16 with two expected optional
  schema-library skips.
- Provider operations / spend: 0 / USD 0.
