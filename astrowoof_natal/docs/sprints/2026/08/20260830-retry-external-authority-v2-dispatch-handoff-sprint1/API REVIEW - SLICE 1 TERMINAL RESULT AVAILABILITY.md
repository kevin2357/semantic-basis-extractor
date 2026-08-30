# API review — Slice 1 terminal-result availability

## Disposition

Approved. The implementation satisfies the API consumer requirements.

## Confirmed properties

- The closed v1 document distinguishes valid `none_available` from `available`.
- Invalid, malformed, orphaned, unsealed, or snapshot-invalid evidence raises a
  typed `NativeTransitionAvailabilityError`; it cannot silently degrade to
  absence.
- The document is bound to native run ID, logical restored workspace root,
  restored workspace-snapshot SHA-256, index SHA-256, and its own canonical
  digest.
- The latest result ID remains discovery only. The reader validates the indexed
  publication inventory and sealed explicit result before exposing it; API will
  still pass that ID through its exact-result strict reader and terminal ingress.
- The CLI is read-only and refuses an output path inside the native workspace.
- The additive surface exposes no lifecycle state, provider identity, action
  inventory, grant, or transition authority.

The targeted source and installed-wheel evidence is proportionate and supports
the absence/available/invalid contract.

## API integration alignment

API has already added the corresponding selected-ID path:
`sealed_terminal_result_id` is carried once from a future availability document
to strict terminal ingress. It is mutually exclusive with an invocation-bound
terminal-review command result, preventing a second latest-result lookup or
conflicting authority sources.

SBE may proceed with its fresh-version/release preparation. API will adopt the
released reader/schema in Sprint 58 before enabling the production preflight.
