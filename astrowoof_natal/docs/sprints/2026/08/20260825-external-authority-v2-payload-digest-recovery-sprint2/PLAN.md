# External-Authority v2 Payload-Digest Recovery — Patch Sprint 2

Date: 2026-08-25
Status: Slices 0–3 complete; final release review pending
Starting release: SBE 0.4.23
Expected release: fresh immutable patch version

## Objective

Correct the canonical payload-resolution mismatch that caused two valid ordinary
v2 continuations to seal as `pre_provider_refusal / request_payload_digest_mismatch`
before provider I/O. Preserve the fence: only the exact payload committed by the
action binding may reach provider create.

## Current diagnosis

The ordinary exact authoring adapter computes `binding.request_sha256` from the
complete Responses payload. For editorial/privacy reasons it persists:

- `openai-request.json`, with the large workspace user prompt replaced by a fixed
  placeholder; and
- `openai-workspace-prompt.txt`, containing that exact prompt separately.

Unlike initial-wave preparation, this path does not also persist
`openai-request-payload.private.json`. The v2 resolver searches for JSON payloads
and compares their canonical digest directly with the binding. It therefore hashes
the redacted display artifact, not the complete request payload that established
the spend binding. A valid later creative-retry action consequently refuses before
provider create.

This diagnosis must be confirmed by a production-shaped provider-free fixture
before source behavior changes.

## Invariants

1. No provider create occurs until request, inspection, grant, authorization
   documents, complete binding, and exact payload digest all join.
2. `binding.request_sha256` continues to mean the canonical SHA-256 of the exact
   provider request body—not a digest of a redacted display artifact or a newly
   invented derivative.
3. Historical reconstruction is allowed only through the closed snapshot-bound
   exact request builder pinned to retained route, attempt, feedback, profile,
   resource, and builder compatibility identities. It must reproduce the persisted
   flattened prompt and the binding digest. No fuzzy search, semantic equivalence,
   literal one-field reattachment, or API/private inference.
4. Future actions retain an exact native payload artifact so ordinary dispatch
   need not reconstruct when direct evidence is available.
5. Existing `pre_provider_refusal` receipts, invocation history, and action history
   remain truthful and immutable. The refused grant is never revived and the old
   action must not be rewritten to imply that refusal never occurred. Continued
   work requires a freshly derived native posture, fresh inspection, fresh request,
   and fresh API authority decision.
6. Provider-bound, ambiguous, stale, malformed, duplicated, or non-unique payload
   evidence remains fail-closed.
7. No retained QA workspace is mutated and no provider credentials, network, or
   spend are used during development or qualification.

## Slice 0 — Reproduce and freeze the digest distinction

- Build an ordinary exact interactive action through the production request
  preparation path.
- Prove the action binding matches the in-memory complete payload.
- Prove the persisted redacted request alone does not match.
- Prove the adjacent flattened prompt is insufficient for literal payload
  reattachment because it does not preserve the original ordered content-block
  boundaries and cache-control metadata.
- Assess bounded interactive preparation explicitly. Include it in the runtime
  correction only if it uses the same redacted-artifact representation and can use
  the identical closed resolver without weakening existing evidence rules.
- Record the canonical JSON rule: UTF-8, Unicode preserved, recursively sorted
  object keys, compact separators, arrays ordered, no whitespace dependence.
- Add a sanitized exchanged fixture containing the public inspection/request/grant/
  authorization identities plus non-sensitive native payload-artifact metadata.

Gate: owner/API review confirms the exact digest basis and recovery evidence before
the resolver changes.

## Slice 1 — Implement exact payload persistence and closed recovery

- Add one shared payload persistence/resolution helper used by ordinary exact and
  bounded interactive preparation where applicable.
- For newly prepared requests, persist the exact private provider payload alongside
  the existing redacted/operator artifacts before external-authority inspection.
- For historical exact work lacking that file, invoke only the versioned,
  snapshot-bound deterministic request builder from the exact retained route,
  attempt, prior feedback, profile/provider configuration, source workspace, and
  compatible resource/builder identity.
- Require the rebuilt segment flattening to equal the adjacent UTF-8 prompt, the
  redacted JSON to contain exactly one expected placeholder at the exact structural
  location, and the rebuilt complete payload to equal the binding digest.
- Prefer the one binding-owned direct payload reference. Historical fallback is
  the closed compatible builder, never literal two-file reattachment or discovery
  among candidate payload files.
- Store new direct private payloads through a binding-owned, snapshot-inventoried
  content reference. Resolve that exact reference; do not recursively discover
  candidate payload files.
- Keep typed `request_payload_unavailable`, `request_payload_ambiguous`, and
  `request_payload_digest_mismatch` outcomes unchanged.

Gate: focused source tests prove the valid path and every fail-closed mutation with
zero provider calls.

## Slice 2 — Prove post-refusal continuation semantics

- Reproduce the 0.4.23 pre-provider refusal and verify:
  - no provider identity, ambiguity, or consumption was created;
  - the old invocation replays only as the same refusal;
  - the immutable refusal receipt and action history remain unchanged;
  - the old invocation is never rewritten as untouched or successful, while the
    operational action may return to history-bearing `PREPARED` posture;
  - SBE derives and documents an exact supported post-refusal native posture from
    which a fresh inspection may emit a fresh compatible v2 request.
- Supply a fresh grant and authorization document set, resolve the exact payload,
  and use a scripted transport to prove exactly one create.
- Reopen in a fresh runtime and prove provider-pending/reconciliation-only custody
  with no duplicate create and no initial-wave replay.
- Cover exact creative retry positively and exact polish/critic/candidate plus
  bounded interactive according to their actual artifact shapes; unsupported or
  unavailable shapes fail closed explicitly.

Gate: API reviews the fixture/result matrix and confirms it can recover the two
retained runs using a new authority decision after release.

## Slice 3 — Installed-wheel qualification and handoff

- Package the canonical digest/recovery fixture and public validation surface
  needed by the API; do not expose protected prompt/payload content.
- Run a provider-free installed-wheel command/test through:
  refusal, fresh inspection, new grant, exact payload resolution, one scripted
  create, detach, and replay/reconciliation selection.
- Document the operator/API recovery sequence and the explicit prohibition on
  reusing either refused grant.
- Run the focused v2 dispatch, ordinary route, privacy-sentinel, snapshot, and
  installed-wheel suites plus `git diff --check`.
- Prepare a reproducible fresh patch wheel and pause for final release approval.

## Test matrix

Positive:

- newly persisted exact private payload matches binding;
- historical exact retained inputs deterministically rebuild a request whose
  flattened prompt, redacted operator artifact, and binding digest all match;
- fresh request/grant after pre-provider refusal dispatches exactly once;
- direct and reconstructed representations resolve to the same canonical payload;
- exact and bounded applicable ordinary interactive routes remain supported.

Negative:

- altered prompt, builder/profile/resource identity, route, attempt, feedback,
  placeholder, JSON field, array order, or binding digest;
- missing prompt, multiple placeholders, competing direct references, conflicting
  direct/rebuilt payloads, invalid UTF-8, or path escape;
- stale inspection, mismatched grant/document/binding, reused refused grant;
- provider identity, consumption, ambiguity, or unsupported Batch mechanism;
- event/log privacy sentinel leakage.

Every negative cell proves zero provider create and preserves a coherent native
checkpoint or the existing typed review/refusal posture.

## Review pauses

1. Now: Kevin/API review of this plan and diagnosis.
2. After Slice 0: freeze canonical digest and historical reconstruction rules.
3. After Slice 2: API reviews recovery and no-duplicate-create fixtures.
4. Before tag/publication: final owner/API release authorization.

## Exit criteria

- valid API-issued v2 authority reaches create only when the exact bound payload is
  proven;
- genuinely changed payloads still refuse before provider I/O;
- retained pre-provider refusals can progress only through fresh native/API
  authority, without replaying initial-wave or refused-grant work;
- installed-wheel provider-free evidence passes;
- consumer handoff and release records identify exact artifact/source hashes; and
- no paid or retained-QA activity occurs during the sprint.
