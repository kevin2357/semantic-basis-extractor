# Slice 2 — Exact Workspace Root Identity Finding

## Decision

Slice 2 identifies the first failing boundary. API invokes the post-terminal
observer with its outer checkpoint/API workspace root. Each retained SBE
workspace records a different native durable logical root. SBE's exact reader
correctly refuses that contradiction during snapshot validation.

No SBE runtime-capture defect is present. With identical retained bytes mounted
read-only at each workspace's own contract-bound root, the public SBE reader
and complete editorial capture succeed for both Garamond and Quill.

## Custody and access

API performed exactly one ETag-conditional HEAD and one bounded GET for each
owner-authorized checkpoint and retained the archives outside Git. SBE
independently verified both archive SHA-256 values before extraction. No
additional R2 operation was performed.

The local reproduction used a network-disabled, read-only container with all
capabilities dropped and `no-new-privileges`. SBE source and one workspace at a
time were mounted read-only. Diagnostic output was limited to phase, branch,
bounded exception class/fingerprint, safe counts, and root digests.

## Reproduction matrix

| Input/root | Garamond | Quill |
| --- | --- | --- |
| Archive SHA matches receipt | yes | yes |
| Snapshot member inventory | `902/902`, exact | `906/906`, exact |
| API/checkpoint root equals durable root | no | no |
| API/checkpoint root exact reader | snapshot-validation `ValueError` | snapshot-validation `ValueError` |
| Durable root exact reader | `delivery` | `delivery` |
| Durable root evidence collection | `delivery` | `delivery` |
| Durable root capture construction | packet `1`, projections `8`, artifacts `9` | packet `1`, projections `8`, artifacts `9` |

The API/checkpoint and durable root SHA-256 pairs are retained in `EVIDENCE.md`;
the native absolute durable paths are intentionally not published.

## Ownership and correction fence

Correction belongs at API's workspace identity source or observer call site. It
must carry the exact SBE durable root already established for that job and must
not discover a latest workspace, rewrite native state, weaken SBE stable-root
validation, or substitute the API run/checkpoint root.

SBE requires no package or runtime change from this finding. Existing
fail-closed stable-root behavior is correct. API should add a regression proving
that a terminal publication retry preserves both the exact result ID and the
exact native durable workspace root into observer invocation.

Stop for joint review before implementation or deployment.
