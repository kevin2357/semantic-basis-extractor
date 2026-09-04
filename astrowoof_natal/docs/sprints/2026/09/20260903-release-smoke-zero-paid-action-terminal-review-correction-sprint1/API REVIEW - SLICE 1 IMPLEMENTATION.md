# API review — Slice 1 implementation

**Disposition:** approved in substance; two small closure corrections requested
before Slice 2 packaging/installed qualification.

## What is aligned

- The provider-free release-smoke fixture materializes
  `spend_ledger: {"actions": []}` before native resume.  Publication therefore
  does not infer that an omitted ledger is empty.
- The new v0.3 result is an exact-key, separately versioned zero-action result.
  It carries an explicit zero inventory, forbids new provider creation, and has
  no action disposition, provider-operation, authorization, consumption, or
  custody projection surface.
- v0.2 remains the strict paid-action path.  The v0.3 builder refuses missing,
  malformed, and nonempty ledgers; the normal v0.2 builder remains in use unless
  the private fake-provider smoke switch selects v0.3.
- The new command envelope and receipt joins are independently versioned and
  validated.  API's existing v0.2 consumer will therefore fail closed on v0.3,
  as intended; no API lifecycle interpretation changes are needed.

## Requested small corrections

1. `SLICE 1 - EXPLICIT ZERO-ACTION TERMINAL CONTRACT.md` still says
   "proposed; API contract review required before source mutation."  Update the
   status and qualification language to reflect the implemented, reviewed
   contract.
2. Add an explicit regression proving that a real v0.2 one-action result cannot
   be accepted as v0.3 (and, conversely, that the strict v0.2 validator rejects
   a v0.3 zero-action result).  The present malformed/attached-evidence cases
   are useful, but this direct cross-version assertion protects the central
   non-downgrade boundary more clearly.

Those are contained test/documentation refinements, not a request to broaden
the feature.  Once incorporated and green, API approves progression to Slice 2
packaging and installed-wheel qualification.
