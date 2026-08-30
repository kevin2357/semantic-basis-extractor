# Background — legacy v0.5 local-work contract upgrade

## Purpose

API Sprint 59 and this companion sprint address an independently reproducible
legacy lifecycle representation gap discovered during the bounded Diffie
investigation. The exact historical rejected lifecycle document is unavailable,
so this work must not be described as a proven Diffie repair.

## Seam

A coherent native mixed-custody checkpoint can have completed provider evidence
requiring deterministic local fan-in while another provider-bound action remains
pending. The native-produced lifecycle v0.5 document can be structurally valid
while selecting `ordinary_resume` without identifying the exact executable local
operation required by API's stricter scheduling semantics. The compatibility
adapter must therefore classify one exact semantic-validation failure at the
validation boundary; it must not describe the document as fully API-valid or
broadly catch `SbeProviderContractError`.

Newer v0.7/v0.8 documents express the missing evidence explicitly. They are not
a blind fallback ladder: v0.7 is sufficient when its exact executable local-work
evidence resolves the decision; v0.8 is required only when retry lineage or mixed
custody must also be joined.

API must keep v0.5 strict. It may request newer public observations only for a
precise, contractually frozen compatibility predicate, and only for the same
restored checkpoint. Newer evidence remains the sole scheduling authority.

## SBE scope

SBE must first inventory the already released 0.4.31 public readers, schemas,
fixtures, and qualification surfaces. It should add only the provider-free public
evidence genuinely missing for API's narrow adapter. A new SBE runtime change,
wheel, or release is not presumed. SBE must not add private-state recovery,
provider I/O, retained-QA mutation, or an ad-hoc API-only lifecycle state.
