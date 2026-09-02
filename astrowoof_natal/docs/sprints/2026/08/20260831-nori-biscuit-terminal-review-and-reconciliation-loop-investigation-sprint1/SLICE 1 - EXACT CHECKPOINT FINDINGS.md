# Slice 1 — exact checkpoint findings

## Access and validation result

The exact approved access budget was consumed successfully:

- Biscuit generation 13: one `HEAD`, one ETag-conditional `GET`.
- Nori generation 15: one `HEAD`, one ETag-conditional `GET`.
- Total: two `HEAD`, two `GET`, zero list/write/delete.

Both objects matched their frozen key, ETag, byte length, archive SHA-256, and
inventory SHA-256. Both ZIP archives passed path/traversal/link/duplicate/member
validation, every declared member matched its byte length and SHA-256, and the
workspace snapshot member sets validated offline. All native results joined
their receipts, bounded journal ranges, and retained publication snapshots.

The restored physical directory intentionally differs from each recorded stable
logical root; therefore validation compared immutable snapshot member evidence
without rewriting the workspace contract or pretending the disposable restore
occupied the production path.

## Biscuit generation 13

Checkpoint identity:

- archive SHA-256: `925dfed7…89d47`;
- inventory SHA-256: `3aa7b1db…c7b3`;
- native revision: 88;
- native status: `WAITING_FOR_RESPONSE`.

### Exact native facts

1. `paid_53ff…` (creative retry, pass 6 attempt 2) is `REPORTED`; its
   completed response was adopted, QA-rejected, and terminally reported.
2. `paid_b189…` (creative retry, pass 2 attempt 2) is `WAITING` with durable
   response `resp_0de681…`, `last_outcome=completed`, four retrieval attempts,
   consumption present, and an exact completed response artifact. It is not
   reported.
3. The matching pass attempt remains `AMBIGUOUS_PROVIDER_SUBMISSION`, has no
   provider metadata, no QA, and no finish timestamp.
4. `paid_937…` is a separate providerless `PREPARED` pass-6 attempt-3 action.
5. The live v2 intent still names `paid_53ff…` and `paid_b189…`, says
   `PROVIDER_PENDING`, and has both durable provider operation IDs.
6. There is no `local_work_progress` record. The completed `paid_b189…`
   evidence derives one blocking local dependency.
7. Its stable semantic operation key is
   `work_c2a017c3443ee1fbb5518972`; no consumed-key history exists.
8. Latest sealed result `nres_bbb1350a6758739d3e89f142` is a valid v0.1
   `provider_pending` reconciliation result at revision 88.

### Loop classification

This is not a legitimate due-time wait: retrieval is complete. The checkpoint's
static action/binding/provider/artifact facts satisfy the completed-adoption
eligibility predicates, yet the attempt remains ambiguous. The later API cycles
restore the same immutable checkpoint ID/generation, so every cycle begins from
byte-identical native truth and the same semantic operation key.

The supplied log ends before those later cycles. It cannot prove whether an
ephemeral successor was declined by API or whether SBE produced no publishable
successor. The absence of any successor in the exact retained generation means
that distinction requires provider-free production-boundary reproduction.

## Nori generation 15

Checkpoint identity:

- archive SHA-256: `721926c6…e6e8d`;
- inventory SHA-256: `56514a2f…a756`;
- native revision: 85;
- native status: `WAITING_FOR_RESPONSE`.

### Exact native facts

1. All six initial actions and creative retry `paid_080…` are `REPORTED`.
2. Polish `paid_d359…` is `WAITING` with durable `resp_055d13…`, completed
   reconciliation, consumption present, and an exact completed response
   artifact. It is not reported.
3. The subject is `FINAL_QA_WARN`; polish attempt 1 remains `SUBMITTED`, has no
   paid-action pointer/provider metadata, and is unfinished.
4. The live singleton v2 intent is `PROVIDER_PENDING` for the polish action.
5. Existing consumed history contains `work_b1d339…`, not the current polish
   operation `work_485dd3307818ab352c77ab9d`.
6. Result `nres_cca6d3bd230517d294e57cef` and receipt
   `nreceipt_7bcbf15b34b652a2b87f4ff1` validate exactly. The result is v0.2:
   - outcome `review_required`;
   - cause `local_work_progress_contradiction`;
   - custody finality `provider_reconciliation_required`;
   - reconciliation inventory exactly `[paid_d359…]`;
   - `new_provider_create_permitted=false`.

### Terminal distinction resolved

The native result proves SBE did **not** claim complete terminal custody. It
sealed an editorial/native review decision while explicitly preserving
retrieval-only polish custody. API's later `native.terminal.review_required`
failure and resource cleanup therefore cannot be justified by treating
`review_required` alone as full terminal closure.

This preserves the requested vocabulary boundary: SBE `terminal_closed` was the
command outcome for a sealed result; API terminalization was a separate consumer
decision, and the exact result shows that decision discarded retained custody.

## Safety boundary

No provider adapter, resume, reconciliation, repair, denial, retirement, or
workspace mutation was invoked. The downloaded copies remain local diagnostic
evidence only.
