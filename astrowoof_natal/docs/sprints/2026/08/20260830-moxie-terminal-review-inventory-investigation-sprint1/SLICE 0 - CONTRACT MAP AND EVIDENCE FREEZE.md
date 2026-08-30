# Slice 0 — contract map and evidence freeze

## Decision summary

The current public contract is full-native-ledger, not an undocumented
snapshot-scoped subset:

- `build_terminal_action_dispositions()` reads every row from
  `state.spend_ledger.actions` and preserves ledger order.
- terminal-review result v0.2 binds those rows through
  `action_inventory_sha256`, plus exact reconciliation and providerless-denial
  subsets.
- the immutable result binds a native revision/checkpoint basis and journal
  range; the receipt then binds that result to the complete workspace snapshot.
- SBE's public API-action validator requires exact action-set equality and exact
  native-run, binding, route-family, stage, and provider-operation joins.

Consequently, Moxie's mismatch is not presently explainable as a legitimate
implicit subset. It remains an evidence question: what exact ledger/result was
present in generation 11, and how did it compare with API's seven actions?

## Public authority and scope map

| Evidence | Native meaning | Scope | Positive permission | Does not prove |
| --- | --- | --- | --- | --- |
| `state.spend_ledger.actions` | durable native paid-action ledger | all actions stored in that checkpoint | none by itself | API reservation/admission state |
| lifecycle action inventory | public projection of checkpoint actions | exact inspected native checkpoint | selector inputs allowed by its closed branch | later API-created action exists natively |
| terminal-review v0.2 `action_dispositions` | custody disposition for every native ledger action | complete ledger loaded under publication writer | reconciliation/denial only where explicitly listed; never new create | API job terminalization or resource release |
| `action_inventory_sha256` | ordered terminal-row content identity | exact v0.2 result | integrity comparison | an alternate action scope |
| `post_checkpoint` | revision, checkpoint-basis digest, logical root | native state used for the result | exact checkpoint join | R2 checkpoint generation by itself |
| `journal_range` | invocation/native-transition provenance | exact unclaimed journal range | exact result provenance | API ingestion success |
| publication receipt | result + full snapshot + checkpoint basis seal | exact immutable publication pair | reader acceptance after validation | API custody/settlement disposition |
| terminal command-result envelope | exact invocation/result/receipt transport | one command invocation | ingest named result | availability-based latest-result authority |
| API `SbePaidAction` rows | API-owned paid-action bindings/custody | current API run inventory | API-side join/admission decisions | native ledger presence |

## Production boundary trace

### Native result construction

- `terminal_review_contracts.py:91` projects all ledger actions.
- `terminal_review_contracts.py:155` upgrades the base native result to v0.2,
  computes the full ordered inventory digest, and derives custody subsets.
- `terminal_review_contracts.py:323` performs the supported exact join against
  API-supplied immutable action documents.

### Publication ordering

- `closure.py:2739` saves state/snapshot before terminal-review publication.
- `closure.py:2744–2780` inspects review posture, publishes v0.2, emits the exact
  command-result envelope, then exits 2.
- `native_transitions.py:712` publishes under the native writer.
- `native_transitions.py:787–816` permits exact replay only when revision,
  route, cause, outcome, and recomputed full-ledger inventory digest agree.

### API strict ingress

- `sbe_native_transition_ingestion.py:281–310` locks every API paid action for
  the run and rejects unless its exact ID set equals the terminal rows.
- subsequent validation joins immutable binding digest, route/stage, native run,
  and provider identity.
- the companion API sprint separately owns the lease-expiry containment defect;
  it must not relax this inventory join as a workaround.

## Frozen coordinate provenance

| Artifact | SHA-256 |
| --- | --- |
| `BACKGROUND.md` | `6b83afca7f396483ab9ab0463e8d8654bf6ca5aed89794fac10551e3d8b4ee4e` |
| `API REVIEW - PLAN AND VOOF-PAWS 1.md` | `bf6ecc4a46cefc05a3c70e4c15e8180e2b2ed45191cd577f981a0ddb3ee7e11a` |

The exact object key is
`v1/checkpoint/429d43b26dc04ad9ac31ee68c9d32878`. It is a deterministic
rendering of the API storage reference and is authorized for one future `HEAD`
and one future `GET`. Slice 0 performed neither.

## Expected API join inventory

API asserts seven paid actions:

- six initial actions with API status `reported`; and
- creative-retry action `paid_5769a5e279df0fc506f65a91`, status
  `provider_created`, provider response
  `resp_057af41fd08baade006a947ae12fd087d0b3f03d5d45c128a1`.

`provider_created` is API custody evidence only. It is not proof that the action,
provider identity, consumption, or report exists in generation 11's native
ledger. The six initial action IDs and the seven complete immutable API binding
join documents are not present in the supplied sprint evidence. They are not
required to inspect the native checkpoint, but they are required before claiming
an exact successful or failed seven-row field-level join.

## Evidence availability

| Fact | Availability | Treatment |
| --- | --- | --- |
| generation-11 checkpoint coordinates/hashes | retained and frozen | verify before access |
| generation-11 native ledger/result indexes | expected inside checkpoint | inspect read-only in Slice 1 |
| API seven-action count/status chronology | retained API authority | accepted as supplied |
| seventh API action/provider identity | retained API authority | frozen above |
| six initial API action IDs/full bindings | not supplied here | request only if field-level join is needed |
| rejected terminal-review payload | not retained by API | never reconstruct or claim exact delta |
| native result/receipt in generation 11 | unknown until inspection | absence is evidence limitation, not defect |
| lease-expiry conversion | established API companion concern | keep separate from native inventory cause |

## Slice 0 conclusion

The source and coordinate contract are sufficiently frozen for the bounded R2
inspection. Voof-paws 1's coordinate requirement is satisfied. Per API's review,
the sprint pauses before `HEAD`/`GET` so the source map and remaining join-input
limitation can be reviewed explicitly.
