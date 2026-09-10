# Background

Baskerville and Hopper are the two current operator-quarantine subjects. API is
attempting the existing nice path: restore exact retained native evidence, ask
SBE for its public read-only disposition assessment, and execute quarantine only
when that assessment proves the posture permitted.

AstroWoof previously attempted this path once, but the operator runner did not
receive a valid SBE assessment. The subsequent QA reset removed the database and
R2 workspace evidence, so the historical cause cannot be reconstructed exactly.

This sprint reconstructs the current production boundary provider-free before
interpreting the Baskerville/Hopper outcome. In parallel, it investigates why
Baskerville stopped making ordinary lifecycle progress in the first place.
Those are separate questions: assessment failure does not establish the cause
of the stuck run, and successful quarantine would not explain it. It does not weaken
`astrowoof.operator_disposition_assessment.v1`, authorize quarantine, access
their retained workspaces, perform provider work, or design the universal
emergency-stop path.

Design provenance is retained on branch
`codex/operator-quarantiner-native-design` at commit `baee8bd`. This mainline
sprint takes only its investigation-first Slice 0 direction.
