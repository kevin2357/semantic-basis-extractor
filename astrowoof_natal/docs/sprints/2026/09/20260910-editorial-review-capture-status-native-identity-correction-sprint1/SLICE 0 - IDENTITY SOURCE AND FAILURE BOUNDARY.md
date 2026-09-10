# Slice 0 — identity source and failure boundary

Status: discovery complete; proposed contract decision awaiting Kevin and
API/Vafflemutt review before implementation.

## Outcome first

`editorial_review_capture_status.v1` can remain unchanged. Its three required
correlations can be emitted honestly only after one exact native result view and
one exact single-subject workspace state agree. The runtime must otherwise emit
no capture status.

`subject_id` is mandatory correlated content but deliberately does not
participate in `capture_id`. The frozen semantic-manifest formula remains:

```text
capture_id = H(native_run_id, native_result_id, reason, detail_code)
```

The runtime needs an exact-source validator in addition to closed-schema
validation. A status whose subject is changed and reserialized can remain
self-consistent under the frozen ID formula, but it is not legitimate unless its
subject matches the exact native workspace evidence.

## Exact identity sources

| Status field | Required source | Required agreement |
| --- | --- | --- |
| `native_result_id` | caller-selected `result_id` | must equal result document `result_id` and publication receipt `result_id` |
| `native_run_id` | validated result document | must equal receipt `run_id` and restored `run.json` `run_id` |
| `subject_id` | the sole key of validated `run.json.subjects` | exactly one subject must exist; no path, fixture, result projection, or API value may substitute |
| `reason` | closed runtime classification | must be one capture-status v1 reason |
| `detail_code` | closed reason mapping | must be the unique detail code assigned to that reason |
| `capture_id` | semantic-contract v5 formula | run ID, result ID, reason, and detail code only; subject ID is excluded |

The production `read_native_transition_result` validates the result's
content-derived ID, its receipt binding, journal range, retained snapshot and
checkpoint basis, and current workspace snapshot. It does not currently compare
the caller's filename/result selector directly with the embedded result ID.
The editorial runtime must therefore perform the explicit three-way selected
ID comparison before any capture status is returned. This sprint does not need
to widen into a shared native-reader change unless implementation proves the
local check cannot be kept exact and bounded.

## Branch-by-branch emission matrix

| Branch | Identity available at present code point | Correct v1 behavior |
| --- | --- | --- |
| exact reader rejects malformed/missing/unsealed evidence | no validated exact view | raise/fail closed; emit no status |
| receipt schema check fails after an injected/custom exact reader | values may be present but the receipt is not a supported validated publication | emit no status |
| native result v0.3 is valid but unsupported by editorial capture | exact run/result/receipt exist; subject still requires validated single-subject state | emit `unsupported_result_version` only after state join succeeds |
| supported result has an ineligible route/outcome | exact run/result/receipt exist; subject still requires validated single-subject state | emit `ineligible_route` only after state join succeeds |
| restored state `run_id` disagrees with result/receipt | subject belongs to an untrusted/mismatched state | emit no status |
| service level is unsupported and exactly one subject is proven | all required correlations are exact | emit `ineligible_route` |
| restored state has zero or multiple subjects | no unique exact `subject_id` | emit no status, regardless of service level |
| checkpoint, snapshot, release, profile, or resource join contradicts after exact subject proof | required identities remain exact; non-identity evidence is contradictory | emit `contradictory_native_evidence` |
| action/disposition or optional-stage evidence is missing/contradictory after exact subject proof | required identities remain exact | emit the applicable incomplete/contradictory status |
| fewer than six accepted pass winners after exact subject proof | required identities remain exact | emit `incomplete_native_evidence` |
| packet assembly raises after exact evidence collection | exact correlation context has already been established | emit `incomplete_native_evidence` |
| final semantic packet validation fails | exact correlation context has already been established | emit `contradictory_native_evidence` |

The current combined condition for unsupported service level or a subject count
other than one must be split because only the former can produce an honest v1
status when one subject is known.

## Proposed construction boundary

1. Keep fixture status construction explicitly fixture-only.
2. Add one runtime constructor that requires an immutable correlation context
   containing exact run, subject, and result IDs.
3. Derive reason/detail code centrally and compute the ID from the manifest's
   four declared values.
4. Add a validating exact-source join that checks a candidate status against
   the selected result, receipt, and sole workspace subject. Closed-root schema
   validation alone cannot establish subject authenticity.
5. Establish the correlation context once, after the exact selected-result and
   restored-state joins, and thread it through all later refusal paths.
6. Reorder early editorial eligibility classification so it may retain a reason
   internally while deferring public status construction until the subject join
   succeeds.

No partial status object is returned. Internal exceptions remain exceptions or
an equivalent local fail-closed outcome; they are not serialized as fictional
native observations.

## Contract and compatibility decision

- Preserve `editorial_review_capture_status.v1`.
- Preserve semantic contract v5's capture-ID formula.
- Correct the fixture helper's currently extra subject-ID input when deriving
  its capture ID; regenerate any deterministic qualification identity affected.
- Preserve every closed reason and detail code.
- Preserve successful packet/projection/artifact bytes and the exact-delivery
  handoff.
- Add no new route eligibility or API authority.

This is an additive/corrective public-helper change plus a correction to emitted
runtime values. It requires focused source, semantic mutation, installed-wheel,
and API consumer qualification, but no contract-version bump on current
evidence.

## Alloy impact assessment

`No Alloy impact.` The frozen relationship model does not represent concrete
capture-ID inputs or runtime correlation extraction. Observation remains
non-authoritative, so no modeled authority relation changes.

## Operations performed

Read-only source, schema, manifest, and test inspection only. No provider,
network, subprocess qualification, API sender, Better Stack, database,
retained-run, workspace mutation, package, version, tag, push, or release action
occurred.

