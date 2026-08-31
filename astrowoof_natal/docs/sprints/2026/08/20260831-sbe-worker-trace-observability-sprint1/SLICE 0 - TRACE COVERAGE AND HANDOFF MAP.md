# Slice 0 — Trace coverage and handoff map

## Finding

SBE already returned closed authoritative artifacts, but operational traces did
not consistently expose the safe identities needed to explain which artifact,
branch, custody posture, and checkpoint were selected. Operators therefore had
to restore retained workspaces to answer questions that were already decidable
at runtime.

| Boundary | Before this sprint | First-release trace |
|---|---|---|
| semantic closure / reconciliation | branch prose and provider events varied by path | validated workspace/native summary plus typed exit |
| lifecycle inspection | authoritative JSON only | validated branch/command/disposition summary |
| bounded entrypoint | sparse state prose | fingerprint, state inventory, decision, exit |
| external-authority v2 | fence events but incomplete command correlation | validated basis/state, dispatch outcome, exact exit |
| native transition sealing | result and receipt existed | post-publication result identity/outcome summary |
| result availability | authoritative discovery document only | discovered result identity and typed exit |

Provider adapters already carry detailed call/retrieval diagnostics. This sprint
does not duplicate payload-level transport logging; it joins the surrounding
native state and public command decision to those existing lines.

## Scope decision

The first release covers the above production-facing boundaries and the real
exact/bounded lifecycle CLI used by qualification. Initial-wave v1, operator
retirement, and specialized repair commands keep their existing traces unless
they pass through the shared closure/native-publication helpers. They can be
added later without changing the safe projection contract.

## Authority boundary

Trace lines explain authoritative bytes; they never replace them. Consumers
must continue validating lifecycle, authority, result, receipt, and snapshot
contracts. Missing or malformed traces cannot authorize a transition.
