# Background

## Purpose

Investigate one isolated post-deploy observability gap: Tschichold reached an
ordinary native terminal-review outcome, but did not appear in either Better
Stack repository source as a full editorial packet or longitudinal-artifact
bundle. This is an evidence-collection investigation only. It does not
authorize provider work, lifecycle mutation, reconciliation, recovery,
workspace mutation, package changes, deployment, or a retry of the run.

## Scope witness

| Field | Value |
| --- | --- |
| Dog label | Tschichold |
| API run ID | `0b4dd176-d4dd-451c-8719-02f74505b102` |
| SBE authoring run ID | `4372af6e-403c-49dc-bb20-25bf0e8b4f54` |
| Native run ID | `c1462e77f29c81a26e47430068bb34ae54eaafcce9b4cb2331bdff61f36fbe45` |
| SBE job ID | `7ba20d4c-967c-4091-bec6-9ac3e5131937` |
| Authoritative terminal classification | `native_terminal_review_required` / `native.terminal.review_required` |
| Latest exact native result | `nres_baa5f597cf71ed0be89dd2a8` |
| Native publication receipt | `nreceipt_a2767504131583a0ef8d419d` |

The API authoritative lifecycle shows `failed` only because terminal editorial
review is represented as a failed reading/run; it is not, by itself, evidence
of a pipeline crash.

## Immutable checkpoint coordinate packet

The following was obtained from the API's fixed read-only QA diagnostics
catalog. PostgreSQL provides no R2 object version or ETag.

| Field | Value |
| --- | --- |
| Checkpoint ID | `0f2832c9-64eb-4c6a-9a69-074ade15adbf` |
| Generation / state | `15` / `active` |
| Storage object ID | `27e5815c-b2af-4200-a1bb-45aed25ae17b` |
| R2 key | `v1/checkpoint/27e5815cb2af4200a1bb45aed25ae17b` |
| Archive SHA-256 | `aabaebd72ff1cf52a02b77419845367e880c05369242d514b34b18954217747f` |
| Inventory SHA-256 | `e52faf73c4e89ee03e711446f119eda161a2696003d9699b9ab1d260f85ede3a` |
| Archive byte size | `5470437` |
| Logical restore root | `/work/runs/workspace-183c0651-091a-4ec5-aef5-bf360743dc94/sbe` |
| Result SHA-256 | `baa5f597cf71ed0be89dd2a8e7775ee70321150b0760b91d29e03d2a8a05dfea` |
| Receipt SHA-256 | `a2767504131583a0ef8d419d7bc13614ed35e2d93f7439f31375ea3ebc56d124` |
| Receipt checkpoint-basis SHA-256 | `efb52fe55863986508d828d35452964a4f699e1ee84ea54ffe3318a1730a5cf7` |

No R2 HEAD or GET is authorized by this background alone. If workspace evidence
is necessary after Better Stack/trace inspection, request a separately bounded
conditional HEAD and GET with the exact intended use.

## Better Stack audit finding

API queried both hot and archived Better Stack storage after the 0.4.64 QA
deployment. A full packet is specifically an entry with:

```text
source_kind=editorial
event_kind=packet
```

Tschichold has no such packet row and no longitudinal artifact rows. This is
not a confusion with the lightweight capture-status document: all observed
rows in the editorial source for comparable terminal runs are full packet rows
with associated projections.

SBE may use the native run ID above to perform read-only Better Stack searches
against:

- `AstroWoof QA Editorial Packet Repo` (source ID `2750012`)
- `AstroWoof QA Longitudinal Artifact Repo` (source ID `2750023`)

## Initial hypotheses

1. one-off transport/HTTP delivery failure after an otherwise constructed
   packet;
2. capture eligibility/authority selection skipped at this exact terminal
   handoff;
3. packet construction/refusal before either repository write; or
4. a status/capture path distinction not covered by the current audit.

The completed investigation chose hypothesis 3. Exact authority selection and
native-source proof succeeded, but SBE evidence collection failed before packet
assembly because one legitimate pre-QA failed pass attempt has no acceptance
report. See `SLICE 0-2 - EXACT FAILED ATTEMPT EVIDENCE FINDING.md`.
