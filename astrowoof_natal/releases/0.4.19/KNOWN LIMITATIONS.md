# Known Limitations — SBE 0.4.19

Operator retirement v1 is intentionally not a generic force-state or cleanup
operation. It supports only exact-Natal, provider-free, fully quiescent workspaces.
It does not cancel or reconcile provider work, combine providerless denial with
retirement, repair arbitrary historical bytes, delete artifacts, or release any
API-owned resource.

Bounded Natal, Batch-specific retirement, delivery-complete work, provider-pending
or ambiguous work, and unknown historical contract shapes remain unsupported and
fail closed.
