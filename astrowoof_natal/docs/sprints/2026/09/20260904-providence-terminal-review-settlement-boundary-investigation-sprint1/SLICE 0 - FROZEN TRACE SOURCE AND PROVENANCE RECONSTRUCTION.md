# Slice 0 — frozen trace, source, and provenance reconstruction

## Outcome

Slice 0 confirms a general API settlement-disposition gap for the public SBE
v0.2 finality `providerless_denial_required`.

It does **not** certify Providence's complete retained sealed artifact. The
trace proves the invocation-bound public identity and a source-consistent native
shape; exact action rows, bindings, receipt/journal fields, projection references,
and cause code still require an exact result/receipt export or a separately
authorized checkpoint read.

No retained workspace, R2 object, live API state, or provider was accessed.

## Frozen identities

| Identity | Value |
| --- | --- |
| API run | `5dda2560-1d6c-4a8c-b393-363da3c81212` |
| Native run | `d7017c0ce261b1536ed005e45b2f94ccde056d83c62e789c7f484d361840612f` |
| API job | `d3168e58-19e0-416b-8fc1-44a8b6acc499` |
| Native invocation | `ninv_7440ab2c75754ac3a5fb35f0` |
| Native result | `nres_0f3d3b6a3cc256db4b7a9c1b` |
| Result SHA-256 | `0f3d3b6a3cc256db4b7a9c1b13a5159b202e2b030aa9c9c7f66a7a711ab70ebc` |
| Native receipt | `nreceipt_2b0e8df6e0278a32ff245d61` |
| Receipt SHA-256 | `2b0e8df6e0278a32ff245d61aa3aa241045cf7d6a27ff0bf2476636181abbafa` |
| Accepted API checkpoint | generation 12, `ec4a5b25-9e1a-4198-835f-6d2e07ebd0be` |
| SBE / SPC | `0.4.47` / `0.11.1` |

## Minimal causal timeline

Times are shown in America/Denver daylight time (MDT, UTC-06:00) and UTC.
Line references name the owner-supplied local diagnostic copy
`C:\tmp\providence-terminal-custody-20260904\sbe-worker-04.log`.

| Denver time | UTC | Evidence and meaning |
| --- | --- | --- |
| 14:23:56 | 20:23:56 | Line 11: six initial actions are `WAITING`, with six durable provider identities and custody count 6. |
| 14:24:04 | 20:24:04 | Line 87: two retained initial actions are not due; SBE selects `release_until_due`. |
| 14:24:42 | 20:24:42 | Line 106: those two actions become due and SBE selects reconciliation. |
| 14:24:44 | 20:24:44 | Lines 128 and 130: retrieval-only GETs report both provider operations completed. |
| 14:25:33 | 20:25:33 | Line 223: creative retry dispatch finishes as `detached_provider_pending`; the later native summaries show six initial actions `REPORTED` and one retry in provider custody. |
| 14:31:16 | 20:31:16 | Line 445: API accepts checkpoint generation 11 after the retry reconciliation cycle. |
| 14:31:42 | 20:31:42 | Lines 484–486: all seven existing actions are `REPORTED`; SBE consumes one local operation and selects `ordinary_resume`. |
| 14:31:44 | 20:31:44 | Lines 501–504: the successor has eight actions—seven `REPORTED`, one `PREPARED` polish—with zero provider custody; lifecycle retains it for review and exposes no authority request. |
| 14:31:46 | 20:31:46 | Lines 507–513: the same eight-action shape remains at revision 79; local work is consumed with successor `none`. |
| 14:31:47 | 20:31:47 | Lines 518–522: SBE seals the v0.2 result and receipt, then emits an exact command envelope with `providerless_denial_required`, `review_required`, no create permission, and exit 2. |
| 14:32:19 | 20:32:19 | Lines 523–525: the worker reports `terminal_closed`, accepts checkpoint generation 12, and records no remaining local/provider dependency. |
| 14:32:19 | 20:32:19 | Lines 526–538: API reads terminal ingress, rejects the unsupported settlement disposition non-retryably, fails the job, and releases the lease. |

The initial fan-out, retrievals, and retry are context, not the fault. The fault
occurs after SBE has published the exact terminal-review command envelope and
API has accepted its successor checkpoint.

## Source and contract map

### SBE result construction

`astrowoof_natal/src/astrowoof_natal_authoring/terminal_review_contracts.py`
defines the controlling public semantics:

- lines 22–29: closed custody-disposition and finality vocabularies;
- lines 99–145: every ledger action is projected in ledger order;
- lines 120–127: `PREPARED`/`AUTHORIZED` become
  `providerless_denial_only`, while provider-bound and ambiguous states remain
  separate;
- lines 148–160: aggregate finality is derived by precedence from the complete
  custody set;
- lines 163–186: v0.2 result construction binds the action inventory, denial
  and reconciliation IDs, finality, and no-create assertion;
- lines 278–360: the Python validator closes shape and semantics, recomputes
  inventories/finality, and verifies result identity; and
- lines 484–500 and 524–544: the command envelope carries the sealed
  result/receipt identities and finality and is itself validated.

For the trace-described shape, seven `REPORTED` rows are
`terminally_accounted`; the one providerless `PREPARED` polish row is
`providerless_denial_only`. With no provider or ambiguity custody, line 159
derives `providerless_denial_required`.

### API validation and unsupported mapper

`C:\dev\github\astrowoof-api\src\astrowoof_api\services\sbe_native_terminal_ingress.py`
shows this order:

1. lines 99–129 read the exact result ID supplied by the command and validate
   the command against the sealed publication;
2. lines 130–135 require a recognized native terminal outcome;
3. line 137 evaluates the full custody disposition before API persistence;
4. lines 75–81 implement only `final` and a narrow
   `provider_reconciliation_required` mapping; and
5. lines 82–84 reject every other valid nonfinal settlement boundary.

API's lower transition-ingestion validator already accepts all five SBE v0.2
finalities and rederives them from the sealed action rows in
`src/astrowoof_api/services/sbe_native_transition_ingestion.py`, lines 721–730
and 837–848. The gap is therefore after public semantic validation and before
API persistence/disposition—not a vocabulary parsing failure.

`C:\dev\github\astrowoof-api\src\astrowoof_api\worker\sbe.py`, lines 461–510,
routes `terminal_closed` into terminal ingress and has explicit handling only
for retained provider reconciliation versus ordinary terminal closeout. The
unsupported mapper exception escapes to the worker's typed non-retryable
provider-lifecycle failure path.

## Provenance and sufficiency table

| Claim/evidence | Provenance | Gap diagnosis | Exact Providence settlement | Provider-free fixture |
| --- | --- | --- | --- | --- |
| Seven reported actions plus one prepared polish action | Log lines 501, 503, 507, 511, 517 | Sufficient | Summary only; complete rows absent | Sufficient shape to construct fixture |
| Zero provider custody, ambiguity, and v2 intent | Same native summaries | Sufficient | Summary only | Sufficient |
| Exact result/receipt/invocation IDs and digests | Log lines 518–522 | Sufficient | Necessary but not full artifact validation | Sufficient fixture identity model |
| `providerless_denial_required`, no create, exit 2 | Command envelope, line 522 | Sufficient | Necessary but not action-row proof | Sufficient expected envelope |
| SBE finality derivation | Released SBE source/validators | Sufficient | Only if applied to exact sealed rows | Sufficient normative rule |
| API accepts the five-value vocabulary | API transition validator source | Sufficient | Only if the exact reader completed | Sufficient consumer rule |
| API mapper implements only two finalities | API terminal ingress source | Sufficient | Sufficient to explain observed exception | Sufficient failure/control case |
| Exact action dispositions and binding digests | Not present in logs | Not required | **Missing** | Construct deterministically |
| Exact cause code, journal range, projection refs, checkpoint basis | Not present in logs | Not required | **Missing** | Construct deterministically |
| Exact reader/receipt validation completed | Source order plus observed mapper exception | Strongly source-implied | Not an independently retained validation receipt | Exercise directly |

### Three distinct conclusions

1. **Public semantic sufficiency:** complete. The trace plus both released source
   validators prove a reachable, public `providerless_denial_required` shape
   and an API mapper that does not implement it.
2. **Exact-artifact sufficiency:** incomplete. Providence must not be settled
   from logs. A complete exact export or authorized checkpoint read is required.
3. **Fixture sufficiency:** complete. The trace supplies a production-shaped
   eight-action scenario and exact expected no-I/O disposition for a
   provider-free cross-repository gate.

## Frozen settlement constraints

The expected implementation boundary remains:

- accept only a fully validated, invocation-bound result/receipt/checkpoint and
  exact ordered denial inventory;
- persist API-owned settlement intent and idempotency before invoking SBE;
- retain the workspace and evidence; do not terminal-clean the precursor;
- perform zero provider create, retrieval, or transport I/O;
- invoke only the exact supported providerless-denial operation;
- require a cryptographically joined successor and reinspection;
- permit terminal closeout only from genuinely final successor custody; and
- make interruption replay inert.

Logs, the finality label, and exit code are evidence but not sufficient live
settlement authority.

## Slice 0 decision

The architectural diagnosis is complete without protected checkpoint access.
Slice 1 still needs an exact Providence result/receipt export or an explicitly
authorized checkpoint read before certifying or operating on the retained run.

The provider-free fixture can be designed now, but runtime implementation must
wait for the exact-artifact gate and API ownership review.
