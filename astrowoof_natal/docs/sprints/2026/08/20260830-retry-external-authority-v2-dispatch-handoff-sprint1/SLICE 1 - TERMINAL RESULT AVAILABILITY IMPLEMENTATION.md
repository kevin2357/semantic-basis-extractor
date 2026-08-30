# Slice 1 — terminal-result availability implementation

## Outcome

Implemented the approved additive discovery-only contract:

```text
astrowoof.native_transition_result_availability.v1
```

No lifecycle selection, provider behavior, native transition, result publication,
or authority behavior changed.

## Public surface

- Python reader: `read_native_transition_result_availability(run_dir)`
- Python validator: `validate_native_transition_result_availability(value)`
- Typed error: `NativeTransitionAvailabilityError` with closed `reason_code`
- Schema reader: `read_native_transition_result_availability_schema()`
- CLI: `astrowoof-native-transition-availability --run-dir ...`
- Packaged schema and contract-catalog identity

## Closed outcomes

- `none_available`: a valid restored workspace has no sealed native result.
- `available`: returns exactly one latest result ID for subsequent explicit read.
- malformed, conflicting, orphaned, unsealed, or snapshot-invalid evidence raises
  typed `availability_evidence_invalid`; it never becomes absence.

## Binding

Every successful availability document binds:

- native run ID;
- stable logical workspace root;
- SHA-256 of the restored `workspace-snapshot.json`;
- bounded result count;
- exact latest result ID or null;
- exact result-index file SHA-256 or null; and
- canonical availability-document SHA-256.

For `available`, the reader validates the complete indexed result inventory and
passes every result through the existing strict explicit-result reader before it
exposes the latest ID. API must still pass that ID into the explicit reader and
terminal ingress; availability grants no transition meaning.

## Evidence

- Focused availability tests: 5 passed, 1 optional `jsonschema` check skipped.
- Availability plus native-transition regression set: 49 passed, 1 optional
  schema check skipped.
- Source `git diff --check`: clean (line-ending notices only).
- Non-release installed-wheel build:
  `astrowoof_natal_authoring-0.4.30-py3-none-any.whl`
- Wheel SHA-256:
  `edb3303678492beec76272c70656dd7ee6b965af959913c3b59cf30b72aa944a`
- Installed package exposed the console entry point and packaged schema.
- Installed CLI produced both `none_available` and `available` documents against
  provider-free fixture workspaces.
- External provider calls/retrievals/spend: zero.
- Retained Diffie/Hellman access or mutation during Slice 1: zero.

The wheel retains the already-published `0.4.30` label and is qualification
evidence only. Any publication requires a fresh version after consumer review.
