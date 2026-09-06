# AstroWoof Natal Authoring 0.4.53

SBE 0.4.53 corrects the diagnostic run-cohort timeline's wrapper identity
join. Production API wrapper start events may precede discovery of the native
run identity; the reporter now pairs those boundaries using their exact shared
API run/job/attempt/lease identities and enriches the native lane only from an
explicit, bijective API/native identity witness elsewhere in the export.

Conflicting or unresolved identity evidence remains fail-closed. No authoring,
lifecycle, provider, custody, scheduling, or command-result behavior changes.

This release uses the focused patch gate. The complete repository suite is not
required because the changed diagnostic reducer, its only CLI consumers, its
packaged qualification, and its production-shaped acceptance input are fully
enumerated and tested directly.

