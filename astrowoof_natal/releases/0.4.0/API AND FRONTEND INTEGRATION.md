# API and Frontend Integration - 0.4.0 Candidate

Do not pin this candidate until a release is explicitly approved, tagged, and
published. The current review wheel SHA-256 is
`4fb7a114ae4866475778d36b677d170499a5558e0f1a854aeb88616b9c6c8c84`.

## Worker sequence

1. Verify exact AGF 0.8.1, SPC 0.11.0, and SBE 0.4.0 wheel hashes and installed
   runtime/resource identities.
2. Preserve the four untouched SPC bounded artifacts and AGF runtime receipt.
3. Invoke `astrowoof-run-bounded-natal --prepare-only` or start execution directly.
4. Persist SBE public/lifecycle state into API-owned PostgreSQL authority. HTTP
   status endpoints never read worker scratch or execute SBE.
5. For OpenAI, pass a frozen generation profile containing the complete spend
   policy. Treat exit code 3 as a native waiting/budget/ambiguity boundary and
   inspect the machine-readable state.
6. Reserve funds transactionally in the API, issue authorization bound to the exact
   prepared action, restore the complete workspace at its logical path, and resume.
7. Poll existing provider identity without another reservation or submission.
8. Inspect and close out through `astrowoof-authoring-lifecycle`; use closeout plus
   API-owned lease/storage/product policy to decide cleanup.
9. Validate `bounded/final/delivery.json` and every referenced artifact/hash before
   frontend ingestion.

The OpenAI adapter reads `OPENAI_API_KEY` from the worker environment. Never place a
key in the profile, run state, authorization, events, or snapshot evidence.

## Commands

```text
astrowoof-run-bounded-natal \
  --input-package /work/projected-bounded \
  --run-dir /work/sbe-run \
  --subject /work/private/minimized-subject.json \
  --generation-profile /work/private/generation-profile.json \
  --provider fake

astrowoof-run-bounded-natal \
  --resume --run-dir /work/sbe-run --provider openai \
  --spend-authorization /work/private/authorization.json

astrowoof-authoring-lifecycle --run-dir /work/sbe-run inspect
astrowoof-authoring-lifecycle --run-dir /work/sbe-run closeout
```

The API must pass the same provider configuration on every resume. Batch mode is
not currently supported for bounded authoring and is rejected before execution.

## Frontend boundary

The frontend consumes the separate bounded cards/delivery contracts on its new
bounded-reading page. It must not route them through exact-Natal card assumptions.
Editorial tiers are layout/navigation hints, not confidence. Capability limitations
and uncertainty messaging derive from API-owned validated private state; protected
birth/location evidence must not be copied into public cards.

The v1 product always has fifty invariant cards on success. An insufficient basis
is a failed/review outcome, not a shorter successful reading. The UI may later
choose to hide low-priority claims, but SBE does not suppress them in this release.

## Detailed authority documents

- `Spend Authorization Consumer Handoff.md`
- `Provider Spend Enforcement.md`
- `Provider Disclosure and Durable Workspace Contract.md`
- `Authoring Lifecycle Consumer Handoff.md`
- `Bounded Natal Provider Disclosure Inventory.md`
- the packaged contract and execution-event catalogs

AstroWoof API consumer review accepted this handoff and all nine requested contract
points. No additional event or consumer-contract change is required before release.
