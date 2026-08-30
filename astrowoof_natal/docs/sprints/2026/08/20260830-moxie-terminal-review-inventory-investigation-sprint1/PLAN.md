# Plan — Moxie terminal-review inventory investigation

## Goal

Determine why Moxie's sealed terminal-review action inventory failed API's
strict seven-action join. Establish from immutable native evidence whether the
result omitted a durable native action, was produced from a different checkpoint
basis, or exposed a scope that the public contract does not identify. Recommend
the smallest correctly owned correction, if any, without weakening exact action,
binding, route, stage, and provider-identity joins.

## Status

Slices 0–5A are complete. The retained worker remains suspended. The narrow
exact-interactive fan-in/adoption correction and provider-free interruption
matrix are implemented. Slice 5A closes the already-identified SBE half of the
cross-repository diagnostic gap before the shared release cost is incurred.
Paused at Voof-paws 5A before Slice 6; no version bump or release work has begun.

## Frozen source fact and resolved hypotheses

Current SBE source defines `build_terminal_action_dispositions()` to project
**every paid action in the native spend ledger, in ledger order**. Native result
v0.2 does not declare a smaller snapshot-subset scope, and its API join validator
requires exact action-set and identity equality.

The investigation began with these possibilities; Slices 1–4 resolved them:

1. Generation 11 contains all seven API actions plus one native-only retry-3
   action; the terminal result used the same complete eight-row ledger.
2. The API-owned retry-2 action and provider identity join exactly.
3. The rejected join was eight native rows versus seven API rows.
4. The native-only row was prepared after retry-2 retrieval completed and before
   the terminal review, without an intervening public authority request.
5. Existing public scope/provenance is sufficient; the defect is native
   fan-in/adoption ordering, not a missing result-scope contract.

The background and closed access manifest now supply the exact R2 object key,
object UUID, digests, size, ETag, and logical path. No listing or guessed key
is permitted.

## Guardrails

- One retained Moxie checkpoint only.
- Exact R2 `HEAD` and `GET` only after coordinate verification; no bucket list.
- Restore under a fresh local temporary root; verify containment and hashes.
- No provider access, reconciliation, resume, repair, publication, or writer
  command.
- No API database, job, lease, capacity, reservation, settlement, or delivery
  mutation.
- Sprint evidence contains only safe IDs, digests, states, ordinals, counts, and
  contract metadata—never prompts, generated content, credentials, or subject
  data.
- Treat the rejected historical result as unavailable unless immutable evidence
  actually recovers it.
- No implementation, release, or retained-run recovery before joint review.

## Slice 0 — evidence freeze, coordinates, and source contract map

Freeze supplied API/native identities. Hash the background and coordinate
packet. Trace production builders/readers/validators for terminal review v0.2,
command results, immutable publication, lifecycle v0.7/v0.8 inventories, retry
lineage, provider-identity durability, and terminal-review selection.

Deliver:

- field-level authority/scope table;
- safe expected seven-action API join inventory;
- R2 access manifest with exact key, ETag, archive/inventory digests, and size;
- evidence-availability table: retained, reconstructable, or irretrievably
  historical.

Gate — Voof-paws 1: API confirms the exact coordinate packet and safe join
inventory before R2 access. If the exact key is unavailable, stop; never list.

## Slice 1 — exact read-only checkpoint restoration

Perform one approved `HEAD` and one `GET`. Verify object identity, ETag, byte
count, archive SHA-256, snapshot inventory, logical root, and archive safety
before interpretation. Read only checkpoint/snapshot manifests, native state and
ledger join fields, journal/result/receipt indexes, lifecycle evidence, retry
lineage, and provider identity metadata.

Deliver:

- `SLICE 1 - READ-ONLY R2 ACCESS RECEIPT.json`;
- sanitized native checkpoint inventory;
- seven-action native/API join matrix classifying each mismatch by field.

Gate — Voof-paws 2: review immutable findings. If validation fails, stop with
snapshot-invalid evidence; do not repair.

## Slice 2 — causal reconstruction and result provenance

Reconstruct when each action and attempt first appears; the creative retry's
native state/provider evidence; the revision/basis bound by lifecycle; and any
terminal result/receipt with its snapshot, journal range, invocation, and action
inventory. Compare exactly:

1. generation-11 native spend ledger;
2. any immutable terminal-review result recovered there; and
3. API's seven-action immutable join inventory.

Every causal claim cites a retained artifact path and digest or a named
source/test boundary. Unknown historical payload facts remain unknown.

Deliver: `SLICE 2 - MOXIE SANITIZED CAUSAL AND INVENTORY MATRIX.md`.

Gate — Voof-paws 3: API agrees whether the next step is reproduction, an
API-only correction, or an SBE contract question.

## Slice 3 — provider-free production-boundary reproduction

Build the smallest sanitized fixture faithful to retained evidence and enter
through the actual terminal-review production boundary. Cover:

- exact seven-row full-ledger result and successful strict join;
- native ledger omitting the API-owned creative retry;
- same action with binding/provider/stage mismatch;
- stale result/checkpoint basis versus a later action;
- provider-created retry in reconciliation-only custody; and
- lease expiry after a typed join refusal as a consumer-seam witness only.

Assert zero provider I/O and no new native authority. A mismatch remains typed
review/refusal and is never accepted as an unchecked subset.

Deliver: characterization tests and `SLICE 3 - PROVIDER-FREE REPRODUCTION.md`.

Gate — Voof-paws 4: freeze cause and ownership before runtime/schema work.

## Slice 4 — contract sufficiency and ownership decision

Choose one primary correction class:

- **no SBE defect** — coherent full-ledger result; API ingestion/lease fencing
  owns correction;
- **SBE runtime defect** — stale/incomplete native state or incomplete ledger
  projection;
- **cross-repository publication seam** — API authority advanced without an
  adoptable native checkpoint/result; or
- **public contract gap** — a legitimate bounded scope exists but current public
  evidence cannot prove it.

For a contract gap, propose but do not implement the smallest closed versioned
scope/provenance addition, bound to checkpoint basis, native ledger inventory,
and predecessor/successor relation. API must not reconstruct `run.json`.

For an API issue, specify a typed non-looping disposition and preserve the
separation between local capacity and provider/reservation custody. For an SBE
issue, add implementation slices only after approval.

Deliver: `SLICE 4 - FINDING CLASSIFICATION AND HANDOFF.md`.

Gate — Voof-paws 5: joint approval. The sprint may close here without release.

## Slice 5 — minimal SBE correction

Implement exact-interactive completed-provider fan-in so response identity,
binding, parsing/materialization, deterministic QA, pass truth, and ledger truth
are coherently adopted before successor selection. Preserve full-ledger
projection, exact joins, immutable provenance, custody/denial distinctions,
historical result immutability, and zero unauthorized provider creation. Add the
provider-free matrix frozen in the Slice 4 handoff and pause before packaging.

Status: complete. Existing public contracts were sufficient; source and focused
provider-free tests changed.

## Slice 5A — v2 public-command observability completion

Wire the supported `astrowoof-external-authority-v2` CLI into SBE's existing
application logger and failure-isolated execution-event surface. The underlying
intent/dispatch runtime already emits the required safe events; this slice must
make them reachable through the installed public command without changing
lifecycle, authority, custody, provider, or command-result semantics.

Deliver:

- standard `✨🐶` application logging arguments and run/invocation/state context;
- one closed event transport selection (`--events-jsonl` or
  `--events-stdout-jsonl`) with output kept outside the native workspace;
- emitter propagation through intent commit and provider dispatch;
- concise command-entry, branch/result, and sanitized exception logging;
- a focused Moxie adoption/refusal logging assertion at the newly corrected
  completed-provider fan-in boundary; and
- provider-free tests for successful fence/intent/dispatch sequencing, typed
  refusal, failing event sink isolation, and protected-data absence.

The authoritative command result remains the output file. Logs and events are
supplementary diagnostics only and may never authorize mutation, provider work,
retry, capacity release, or settlement. Durable retention/relay of child stderr
and events remains API-owned and may proceed concurrently.

Gate — Voof-paws 5A: focused tests and privacy/failure-isolation evidence must
pass before Slice 6 packaging. No schema/version expansion is expected.

Status: complete. Focused matrix, compilation, and diff hygiene pass; paused for
API review before packaging.

## Conditional Slice 6 — installed qualification and release decision

Only if SBE code or packaged contracts change: publish closed fixtures and a
provider-free installed-wheel receipt; qualify exact equality, mismatch refusal,
retry/provider custody, replay, and provenance; agree a risk-proportionate gate;
freeze version/hash before testing; and seek separate owner approval before
commit/tag/publication. Retained QA recovery/deployment remain out of scope.

Status: complete and published as `astrowoof-natal-authoring-v0.4.33`. Final
byte-identical wheels and installed qualifications passed. The once-run full
suite and focused fixture correction are recorded without claiming a repeated
wholly green full suite.

## Acceptance criteria

- The exact checkpoint is validated and inspected without mutation.
- Terminal-review inventory scope is stated unambiguously.
- Native ledger, recovered result (if any), and API inventory are joined by exact
  action, binding, stage, route, and provider identity.
- No conclusion relies on the lost rejected payload or API private-state
  reconstruction.
- Inventory-contract and lease/capacity-loop concerns remain distinct.
- Invalid/insufficient evidence yields a typed non-looping review/refusal.
- Provider-created custody remains intact; no new provider work is authorized.
- The investigation can close after Slice 4 without build or release.

## Test strategy

- Source/contract characterization before implementation.
- Hash-verified read-only retained evidence.
- Provider-free production-entrypoint fixtures.
- Rehashed mutations for action set, binding, provider ID, checkpoint basis, and
  any proposed scope/provenance.
- Focused tests by default; broader/installed qualification only if code or
  packaged public artifacts change.
