# Slice 1 — Sprint 58 Semantic Diff

## Result

API Sprint 58 is not a credible direct cause of the lost provider-lifetime
overlap.

Its production changes added exact sealed-terminal identity transport and a
terminal-result preflight. They did not change:

- provider-pending `release_until_due` ingestion;
- `continue_local_cycle` handling;
- allocation acquisition or release;
- full-pool eligible-run restriction;
- queue ordering;
- ordinary defer timing; or
- the four-member native reconciliation bound.

More decisively, a retained pair began its two initial waves 97 seconds apart
after Sprint 58, and overlapping provider-bound lifetimes remain visible on
September 2 and September 3.

## Compared revisions

| Role | Revision | Meaning |
|---|---|---|
| Pre-Sprint-58 control | parent of `31237f6` | before Sprint 58 documents and code |
| Exact-result ingress | `d34d3b8` | transports command-returned or selected exact result ID |
| Terminal preflight | `56511f6` | discovers explicit absent/available result before ordinary selection |
| Sprint closeout | `bc5873f` | final Sprint 58 tree and dependency alignment |
| SBE availability provider | `3709f18` / SBE `0.4.31` | adds public availability reader used by preflight |

## Semantic diff

| Area | Before | After | Scheduling/fairness effect |
|---|---|---|---|
| Terminal invocation result | Command result or generic latest-result fallback entered ingress | Exact command result or exact selected result ID can enter ingress | Tightens identity; no nonterminal allocation effect |
| Cycle-entry terminal detection | Ordinary selector could run before newly visible sealed terminal evidence was consumed | Availability reader can return an exact ID before legacy bridge/lifecycle selection | Terminal work stops earlier; absence follows prior path |
| Availability absence | Latest reader raised an untyped error for no result | Closed `none_available` result | Enables safe preflight; does not alter nonterminal disposition |
| Terminal result precedence | Newly sealed terminal result could be masked by stale nonterminal projection | Exact sealed terminal result wins | Correct terminality; should reduce, not extend, slot ownership |
| Provider-pending release | Exact `release_until_due` release service | Unchanged | None |
| Actionable continuation | Retained allocation for local continuation | Unchanged | None |
| Full-pool eligibility | Existing allocation owners remain eligible so they can progress/release occupied slots | Unchanged; introduced earlier in `dc4cae0` | Existing monopolization mechanism, not Sprint 58 change |
| Native due subset | At most four due actions | Unchanged | None |

## SBE companion assessment

SBE `0.4.31` added `native_transition_result_availability.v1`, its reader/CLI,
schema, fixtures, and tests. It validates snapshot/result-index identity and
returns closed absence or an exact latest result ID.

It did not modify the provider-pending capacity reducer, reconciliation cap, or
the meaning of `release_until_due` and `continue_local_cycle`. The SBE companion
is therefore a negative control for the fairness investigation.

## Chronology test

| Event | Date |
|---|---|
| Sprint 58 implementation complete | August 30 |
| SBE 0.4.31 availability contract integrated | August 30 |
| Retained pair with 97-second initial-wave gap | August 30, post-Sprint-58 |
| Verified overlap witness | September 2 |
| Two verified overlap witnesses | September 3 |
| Verified serial Podium/Laurel witness | September 6 |

There was no absolute disappearance of overlap to attribute to Sprint 58. The
correct causal question is whether Sprint 58 or a later change began a gradual
increase in peer latency. Its source diff exposes no direct nonterminal capacity
mechanism, and the 97-second post-sprint witness makes it an appropriate negative
control. The API-side review should still verify deployed image identities and
test later history/configuration boundaries.

## Later history candidates

The API repository contains several scheduling/terminal changes after the last
verified overlap and before the serial witness. These are candidates for the API
side to classify, not proof of causality:

| Commit | America/Denver | Subject |
|---|---:|---|
| `8c389b3` | 2026-09-03 21:26 | release SBE capacity at retry ceiling |
| `f8590d9` | 2026-09-04 10:31 | admit sealed native delivery handoff |
| `fd669bc` | 2026-09-04 17:14 | settle sealed providerless terminal reviews |
| `99c1ff4` | 2026-09-04 23:56 | hand off terminal reconciliation directly |
| `38d72e4` | 2026-09-06 02:20 | preserve sealed delivery through terminal inspection |
| `e783078` | 2026-09-06 04:33 | settle sealed terminal delivery before failure |

Most titles concern terminal handling and may be irrelevant to nonterminal
fairness. The API semantic diff should inspect actual predicates rather than
select a commit by title.

## Replay assertions frozen for the joint huddle

### Sprint 58 negative control

Use a workspace with no sealed terminal result and the same final
`continue_local_cycle` inspection on both sides of Sprint 58.

Expected:

- availability preflight is absent/no-op after Sprint 58;
- final nonterminal cycle result is equal;
- allocation remains owned in both versions;
- job defer/eligibility behavior is equal;
- peer selection is equal.

Then add a sealed terminal result.

Expected:

- post-Sprint-58 code consumes the exact result before ordinary selection;
- this closes/releases or settles according to exact terminal ingress;
- it cannot create a new nonterminal retained-owner loop.

### Actual divergence replay

After API identifies the narrow post-September-3 candidate revision, replay:

1. one capacity slot;
2. A with six durable provider identities;
3. B eligible but never allocated;
4. A reconciliation with more due actions than the four-action bound;
5. A final `continue_local_cycle / provider_reconciliation_due`;
6. deterministic defer and claim;
7. subsequent fan-in and not-due transitions.

Compare:

- allocation owner after every command;
- exact eligible run set;
- next selected job;
- `available_at` and claim time;
- B time-to-first-submit;
- A due-time wakeup lateness;
- provider operation counts;
- workspace writer count.

## Classification

- **Sprint 58 direct regression:** rejected by source diff and chronology.
- **SBE 0.4.31 companion regression:** rejected by source scope.
- **Existing retained-owner policy as enabling mechanism:** confirmed.
- **Exact change that increased peer latency and eventually produced a
  terminal-boundary wait:** not yet established; requires API Slice 0–1 results
  and joint review.

## Voof-paws 1 questions

1. Does API history confirm that the September 2–3 witnesses ran a post-Sprint-58
   deployment?
2. Which later commit first changes the same two-run/one-slot replay result?
3. Did deployed slot count, ordinary defer, or worker polling configuration
   change independently of source?
4. Is an API-only bounded-turn rule expressible using the existing final SBE
   disposition and durable command boundary?
5. If not, what exact native fact is missing—without overloading
   `release_until_due`?
