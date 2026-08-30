# API pre-Slice 1 contract decisions

## Decision

API accepts the companion-plan correction. The upgradeable v0.5 input is not
described as “strictly validated” if its semantic scheduling predicate has
already thrown. It is instead:

1. native-produced and structurally valid under the released v0.5 schema;
2. valid for every ordinary v0.5 invariant; and
3. rejected only at one explicitly frozen semantic scheduling predicate because
   v0.5 cannot prove the executable local operation needed by API.

API will isolate that predicate at the validation boundary. It will not broadly
catch `SbeProviderContractError`, weaken another v0.5 check, or infer work from
private native state.

## Minimum newer-evidence rule

- Use v0.7 when its exact executable-local-work inventory resolves the next
  operation and no retry-lineage/mixed-custody ambiguity remains.
- Require v0.8 only when its retry-lineage and custody join is necessary.
- In either case, the newer validated document alone selects the operation;
  availability of a newer reader is not authority to resume generically.

## Required Slice 1 inventory output

Please identify the literal public v0.5 fields and relation which make the
predicate upgradeable, the shared run/checkpoint/snapshot identities that bind
the successor, and the precise v0.7/v0.8 outcomes for:

- provider custody still pending/not due;
- provider reconciliation due;
- exact local work with no higher-precedence custody;
- lineage conflict or review; and
- missing, stale, malformed, or contradictory successor evidence.

That inventory is the implementation gate for API Slice 3. No implementation,
provider activity, retained-QA access, or release is authorized by this review.
