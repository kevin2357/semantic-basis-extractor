# API review — Slice 3 packaged qualification

## Assessment

The overall design is correct and appropriately scoped for a lean package-only
patch:

- qualification-only package surface; no production lifecycle/runtime change;
- no API import of SBE test helpers or construction of native workspaces;
- public v0.5/v0.7/v0.8 validators remain canonical composition authority;
- complete dynamic public bundle is separated from a reproducible, path-free
  receipt; and
- the not-due fan-in, due custody, and lineage-conflict outcomes are exposed
  without provider I/O.

## Required correction before approval

`validate_legacy_local_work_upgrade_bundle` currently validates each embedded
document and checks the *declared* `legacy_predicate_failures`, but does not yet
derive the frozen asymmetric predicate from the embedded v0.5 document itself.
Consequently, a rehashed bundle could describe a different valid v0.5 ordinary
resume shape while retaining the `local_dependency_count` label.

Please recompute and require, for `consistent_not_due`:

1. v0.5 `ordinary_resume` with the frozen ordinary branch/capacity relations;
2. an empty `local_dependencies` array; and
3. at least one `provider_custody.actions[]` item classified
   `completed_provider_evidence`.

Then derive the sole API semantic predicate failure from those actual fields,
rather than trusting the scenario summary. Add a rehashed mutation regression
that changes this relation while retaining otherwise valid v0.5 document shape.

Please also add (or point to) focused rehashed mutation coverage for the claims
made in the contract: selected operation/source actions, retained custody/due
subset, and conflict outcome. Existing SBE validators may establish much of
that, but the qualification-bundle validator should demonstrate its own stated
projection checks.

With those narrow corrections, API expects to approve Slice 3 and SBE may enter
the lean installed-wheel release gate. No production provider, retained-QA,
deployment, or release work is authorized by this review.
