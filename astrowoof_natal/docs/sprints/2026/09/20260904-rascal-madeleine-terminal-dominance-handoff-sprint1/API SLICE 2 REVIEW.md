# API Slice 2 review — production-shaped terminal-dominance matrix

**Verdict: approved to begin Slice 3 packaged-boundary qualification.**

The new matrix exercises the three coordinator boundaries implicated by the
Rascal/Madeleine traces rather than merely unit-testing the terminal predicate:

1. the direct public CLI;
2. exact interactive response reconciliation; and
3. exact Batch reconciliation.

Each deliberately enables the qualitative critic, forces an exact delivery
conclusion at the coordinator-owned finalization point, and turns any critic
selection into a test failure.  The interactive and Batch paths additionally
prove the crucial public observations: terminal outcome, no synthetic
`local_continuation`, no external-authority request, no added spend action, and
no new provider create/upload.  This is the production-shaped coverage missing
from Slice 1.

The retained-custody and independently-created-local-successor controls remain
important.  They preserve the distinction API needs: a truthful
`review_required` result with durable provider custody is still retrieval-only,
whereas a fully concluded delivery may hand off as terminal.  Neither permits
new optional work.

For Slice 3, please retain the complete production command boundary and make
the qualification receipt disclose the exact terminal result/receipt identity
and digest, checkpoint/snapshot identity, terminal outcome/reason, and the
resolved-versus-retained custody assertion.  The package test should continue
to establish that terminal delivery emits no successor authority, provider
action, grant, or synthetic local continuation.  API will consume that public
sealed evidence; it must not reconstruct private native finalization state.

No API, QA, R2, provider, deployment, or release operation occurred during
this review.
