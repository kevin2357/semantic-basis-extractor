# Slice 2 — Exact retained-workspace reproduction

## Authority and acquisition

The owner explicitly authorized one conditional HEAD and one bounded GET for
each coordinate-pinned checkpoint. No list, retry, provider operation, API-state
mutation, or additional R2 read occurred.

| Witness | HEAD bytes | ETag | GET bytes | Verified archive SHA-256 |
| --- | ---: | --- | ---: | --- |
| Bodoni | 5,252,898 | `78291d128e9b25be14b58b3f0a11f002` | 5,252,898 | `e4274217c5821d553f4f1fe321b87f2b4b7ac3a2e07ce2aa8d17f0a9fbaefae5` |
| Turing | 5,141,410 | `7eae685a3b415b7e729822b328d883a6` | 5,141,410 | `0eb6a327433ba5fcd56973aa8d152086a4ea839358bac7c55a95feab7f6835ea` |

Each GET used the HEAD ETag as `If-Match` and an exact byte range. The downloaded
objects are ZIP archives despite their inherited `.tar.gz` filenames. Archive
inspection found 937/943 total regular entries, no links, no absolute paths, and
no `..` traversal members. Full manifest verification found zero byte-size or
SHA-256 mismatches across 936 Bodoni and 942 Turing workspace members. The
manifest inventory digests match the coordinate packets.

The R2 authorization is consumed.

## Reproduction controls

Reproduction used disposable extracted roots mounted read-only into a disposable
Docker container with:

- `--network none`;
- a read-only container filesystem;
- the repository or installed package mounted read-only;
- a bounded temporary filesystem outside the restored roots; and
- exact result IDs only.

An initial deliberately relocated mount failed in
`validate_workspace_snapshot()` at the original stable-root check. This is a
control result, not the live diagnosis. Mounting each workspace at its exact
coordinate-pinned logical root removed that relocation artifact.

## Exact-root results

| Witness | Exact logical root | Public capture result |
| --- | --- | --- |
| Bodoni | `/work/runs/workspace-59cceb2b-340b-4d0f-8e19-8f2832ea9000/sbe` | `unsupported / contradictory_native_evidence` |
| Turing | `/work/runs/workspace-8f5c86db-27a9-4543-90e2-1592c6d7ef88/sbe` | `unsupported / contradictory_native_evidence` |

Both exact-root calls returned normally. Neither raised, and neither attempted
network I/O. Therefore the retained checkpoint contents do **not** reproduce the
live `unavailable` branch under the frozen 0.4.61 source.

The typed contradiction is not the incident under investigation: if that same
result had occurred live, API would have entered capture completion and status
envelope/preflight/POST phases. The live trace instead proves a caught local
exception before capture completion.

## Release/runtime parity

- `astrowoof-natal-authoring-v0.4.61` resolves to release-lock commit
  `477cfa2491f33377f1a873772c5e465c588f0741`.
- There are no source changes under `astrowoof_natal/src` between that tag and
  current `main`.
- Current source and API's installed 0.4.61 copies of `__init__.py`,
  `editorial_review_runtime.py`, `native_transitions.py`, and `closure.py` are
  equal after newline normalization.

This rules out a source-level difference among the relevant retained local
copies. It does not by itself attest the already-destroyed live container's
individual site-packages bytes, although its native logs reported release
0.4.61.

## Root evidence and remaining ambiguity

Immediately before terminal publication, each native workspace fingerprint was
`validation=valid`. Its `logical_root_sha256` exactly matches the SHA-256 of the
coordinate-pinned canonical root:

| Witness | Live logical-root SHA-256 |
| --- | --- |
| Bodoni | `6de6911ca8e7bfff781b8597a0c6bd5abc3a8640eaa08799107a6bee3d99ef03` |
| Turing | `04ef679a3ce4dfae652162d7bb8f3afc4136e0afb3ec6feb03d170e943391bca` |

Current API source passes the same `workspace` variable used by the native
engine into `_observe_editorial_terminal()`. Accordingly, a persistent wrong
allocation root is not established. The short live failure remains compatible
with an early exact-reader problem such as a wrong call-time path, missing or
changed result/snapshot evidence, or another pre-inventory validation failure.
The discarded failure-phase event prevents those cases from being distinguished
retrospectively.

## Review Gate B recommendation

Do not change SBE packet construction from this evidence. The exact retained
workspaces make the public function return a typed status, and source parity is
clean.

API should first correct its proven failure-event token/schema mismatch and add
a production-emitter regression. A subsequent witness should safely retain the
exception class and capture phase. If API can also record a content-free digest
of the actual call-time root, it can distinguish root substitution without
logging the path. Only then should another SBE change be considered.

No SBE release is justified by Slice 2 as presently classified.
