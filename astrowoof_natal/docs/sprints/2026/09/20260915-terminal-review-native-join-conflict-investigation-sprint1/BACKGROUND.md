# Terminal-review native-join conflict investigation

## Purpose

Two ordinary QA terminal-review runs on the same deployed SBE `0.4.63` route completed their normal native terminal handoff but produced a typed editorial capture-status rather than a canonical editorial-review packet and its projections. The API-owned capture-status records agree on:

- `outcome=not_captured`;
- `reason=contradictory_native_evidence`; and
- `detail_code=native_join_conflict`.

This is not an intentional policy exclusion: ordinary, clean editorial terminal-review routes are expected to be eligible for packet collection. In the same cohort, a successful ordinary delivery run emitted the full canonical packet, projections, and longitudinal artifacts.

The missing longitudinal artifacts are part of the same failure surface, not a
separate pre-assembly condition. Both review witnesses reached fan-in and had
an assembled deck; witness B also completed two polish actions. Their capture
stopped at `native_join_conflict` before canonical packet construction could
reach the downstream longitudinal-artifact publisher. By contrast, the one
successful delivery witness in this cohort emitted the expected 11 artifact
rows: three `assembled_deck` rows and eight `provider_response` rows. The
investigation must therefore verify whether resolving the native join restores
both packet/projection and artifact publication, rather than opening a
separate artifact-only seam.

The investigation objective is to locate the exact contradictory native join from the two retained checkpoint witnesses, then determine the smallest evidence-faithful correction. This sprint does not authorize a runtime change until the precise conflict is established.

## Frozen witnesses

| Witness | API run | Authoring run | Native run | Native result | Native receipt |
| --- | --- | --- | --- | --- | --- |
| A | `d849dcda-5410-4ccd-af60-26beaba8c0d3` | `d31aeae9-8949-4153-ac3b-43d4d02ee02d` | `a1a465e5f765f7cfbb2d1defa66225cf806a7a01877ad3e4d2dc4139c8afcfde` | `nres_e67a46f89e4e1aa320651c67` | `nreceipt_6774eec6a3360a049e21765c` |
| B | `7904b817-715d-4491-92fd-8760c8c57eb1` | `a556bec2-5dbb-42ad-9d97-6a4dba001606` | `673d4d45e6d269b3b69d47f0eafceb1dcd0bbf9fa2c43a41725014d51ba7fbcb` | `nres_cae11bcfb2948ee4764f2895` | `nreceipt_340135496ed7e6ced643abc0` |

Both runs are terminal and released: they hold no active execution capacity, provider custody, or other QA resource allocation. The packet issue is observability evidence collection, not authority for any retained run action.

## Exact read-only R2 coordinate packet

| Witness | Generation | Checkpoint ID | Exact R2 object key | Archive bytes | Archive SHA-256 | Inventory SHA-256 | Logical restore root |
| --- | ---: | --- | --- | ---: | --- | --- | --- |
| A | 7 | `8cc62c67-32d7-4467-a051-b5ed96797f76` | `v1/checkpoint/c535c649769d434a8ce5412122755aa6` | 4,719,373 | `e09545cb1aba45e2864ad0939d9294017be4990a6cb0fa585fae47178b3ef454` | `7864a9bf08a1f8f1dbc2f4ef0b4361617a6a290c86fb35ea3eaf01b6dd2a295d` | `/work/runs/workspace-63ecee29-f5bb-47cc-b4eb-12bd856290f3/sbe` |
| B | 9 | `49cf66bd-fea2-4944-8eed-87126d5d4227` | `v1/checkpoint/c27e3b62f6cb49d384a9441e30c1f3e6` | 5,098,057 | `1d20a6e2edd219788d21553580e77771840f5863f0dee54e4ea931a40d7b10e7` | `d034d78f5558ab2ddadd2b57037105e24a9b1a31870b6b4c50df66abbee639d3` | `/work/runs/workspace-6a694feb-3bb5-40a9-8003-a135608dfcb7/sbe` |

## Additional immutable joins

| Witness | Result SHA-256 | Receipt SHA-256 | Receipt checkpoint-basis SHA-256 |
| --- | --- | --- | --- |
| A | `e67a46f89e4e1aa320651c67dd96ed2fc0724563bc0e718aa772e384f509f51a` | `6774eec6a3360a049e21765c8727761f959d391af3e7738118b8873ef245d4be` | `930330420562722e942112c52ea6b5dee3135ccd88716f7dd1aa7c68cbf897c5` |
| B | `cae11bcfb2948ee4764f28952444a2a5e42b973c79d65e79c993b684a9f1d4e3` | `340135496ed7e6ced643abc06773c64676d6f379e9a1284f3758ed88279e5031` | `397b06c3ac3bc8b3e1c6bc43bae15938bcb14e881c3b6005972597b126e74e35` |

## Authorization and boundary

The owner explicitly authorizes SBE to perform **exactly one conditional HEAD and one bounded GET for each of the two named checkpoint objects above**. The GET is only for hash-verified, read-only extraction and comparison of the terminal result, receipt, and evidence needed to identify the contradictory join.

Not authorized: listing, alternate-object discovery, writes, provider calls, reconciliation, recovery, resume, repair, API/DB mutation, or retained-workspace mutation. Do not use the read to infer authority to alter either run.
