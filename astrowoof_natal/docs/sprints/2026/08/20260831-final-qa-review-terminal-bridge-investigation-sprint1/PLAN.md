# Plan — final-QA review terminal bridge investigation

## Status

Slices 0–6 complete and published as SBE `0.4.35`. The committed-source wheel,
GitHub release asset, and approved candidate are byte-identical.

## Objective

Establish the exact native/API seam that allowed Glimmer to carry both a
terminal-looking `FINAL_QA_REQUIRES_REVIEW` status and durable provider custody
for a newly submitted polish action. Define and reproduce the general invariant,
then make only the narrowly supported SBE/API correction.

## Non-goals

- Recovering, reconciling, retrying, denying, retiring, or deleting Glimmer.
- Retrieving `resp_0adb…` or creating any provider operation.
- Releasing or reallocating the active API reservation.
- Treating Predicate Paws as the same incident merely because both runs ended in
  review.
- Turning `FINAL_QA_WARN` into automatic acceptance or disabling final QA.
- Inferring API-global custody from native fields.
- Broad R2 listing or access beyond the exact approved objects.

## Preliminary invariants

1. `FINAL_QA_WARN` is a final-assembly finding, but when polish is enabled and a
   polish action is prepared or provider-bound it is not yet a fully closed run.
2. Durable provider identity/custody outranks terminal closeout and new provider
   authority. Existing provider work must remain reconciliation-only.
3. A public terminal result may be authoritative only after its exact action
   inventory proves no unresolved provider custody, submission ambiguity, or
   locally required terminal-publication transition remains.
4. The constrained v2 executor must not cross provider call-entry from a
   checkpoint that its own lifecycle contract classifies as terminal.
5. API consumes the exact invocation-returned terminal result when present; it
   must not infer terminal authority from a status label alone.
6. Providerless authorized work cannot be silently denied or released by SBE;
   any denial remains an explicit API-authorized/native-supported transition.

## Slice 0 — evidence freeze and source/log characterization

Deliverables:

- Hash and inventory `C:\Users\kevin\Downloads\sbe logs.txt`.
- Build separate Glimmer and Predicate Paws timelines.
- Correct the background statement about absent polish provider work.
- Map the Glimmer trace through final assembly, polish preparation, v2 grant,
  intent persistence, status reduction, provider call-entry, identity durability,
  and API lifecycle rejection.
- Trace `persist_state()`, `update_run_status()`, the v2 intent executor,
  lifecycle/temporal selection, and native terminal publication.
- Identify exactly which facts are proved by logs/source and which still require
  retained checkpoint evidence.
- Create a provider-free characterization test if the source-level transition
  can be reproduced without protected access.

Gate — **Voof-paws 1**:

- API review of the corrected timeline and authorization for the exact
  generation-18 `HEAD`/`GET`.

## Slice 1 — bounded generation-18 inspection

Before access:

- Validate the coordinate packet fields and approved object identity.
- Confirm required R2 variables are present without printing values.
- Freeze expected size, archive digest, inventory digest, ETag/provider version,
  logical root, native run ID, generation, and compatibility identity.

Access:

- Exactly one `HEAD` and one `GET` for generation 18.
- No listing, writes, provider access, or implicit neighboring-object reads.
- Validate archive and inner snapshot safety before semantic inspection.

Inspect:

- outer run/subject/pass status and revision;
- polish action binding, authorization, consumption, provider identity,
  reconciliation timing, and reporting state;
- live v2 dispatch intent and any retired history;
- lifecycle v0.5/v0.7/v0.8 and temporal v0.6 artifacts, where retained;
- local-work inventory and consumed-operation history;
- native result index, sealed result, receipt, and invocation envelope;
- exact snapshot membership joining all above facts.

Generation 17 may be retrieved only if generation 18 cannot answer this specific
differential: whether the terminal-looking status arose during the grant/intent
checkpoint rather than already existing in the authority checkpoint.

Gate — **Voof-paws 2**:

- Review the exact mixed-custody projection and decide whether generation 17 is
  still necessary.

## Slice 2 — causal matrix and contract freeze

Construct a field-level matrix across:

- final assembly and subject QA state;
- prepared/authorized/consumed/provider-bound polish action;
- live v2 intent;
- outer run status;
- public lifecycle/temporal disposition;
- native terminal result availability;
- API reservation/provider-operation/terminal-ingress facts.

Classify separately:

- provisional editorial finding versus terminal native result;
- terminal status label versus terminal closeout authority;
- provider custody versus local continuation;
- SBE reducer defect versus v2 executor missing fence;
- API strict-consumer behavior versus API scheduling defect;
- proven cause versus adjacent hardening opportunity.

Freeze the desired state ordering and public consumer rule. Prefer existing
contracts if they can represent the truth; version only an artifact whose closed
shape truly lacks the necessary fact.

Gate — **Voof-paws 3** before runtime mutation.

## Slice 3 — provider-free production-path reproduction

Build a sanitized exact-interactive fixture through real runtime boundaries:

1. reach `AUTHORING_COMPLETE` with final assembly producing `FINAL_QA_WARN`;
2. prepare one polish ordinary-v2 action;
3. export the real lifecycle/request;
4. apply a matching external grant under the writer;
5. checkpoint intent and inspect status before provider call-entry;
6. use a scripted provider to record one identity;
7. inspect the resulting lifecycle and terminal-result availability; and
8. restore/replay without duplicate creation.

Required perturbations:

- providerless prepared polish;
- authorized but call-not-entered;
- call-entered ambiguity;
- provider identity durable/pending;
- provider completed but not adopted;
- provider reported and polish accepted;
- provider reported and polish rejected after max attempts;
- no-polish legitimate review terminal;
- malformed/contradictory terminal evidence.

The fixture must prove that no state can simultaneously authorize terminal
closeout and conceal retained provider custody.

Gate — **Voof-paws 4** with minimal counterexample and proposed fix.

## Slice 4 — narrow runtime/contract correction

Depending on the frozen decision:

- correct `update_run_status()` precedence for polish/provider custody;
- add a v2 pre-call invariant refusing provider I/O from a truly terminal
  checkpoint;
- ensure lifecycle selects reconciliation while durable provider custody exists;
- publish terminal review only after custody and required local closeout are
  resolved;
- preserve explicit providerless denial and API reservation ownership;
- preserve exact replay and ambiguity behavior.

Add crash/replay tests around state persistence, snapshot publication, provider
call-entry, identity durability, reconciliation, and terminal sealing.

Gate — **Voof-paws 5** for API consumer review.

## Slice 5 — packaged consumer qualification

- Publish closed provider-free fixtures for legitimate terminal review and the
  mixed-custody regression.
- Exercise the installed public command/runtime boundary, not test-only helpers.
- Prove the exact invocation/result/receipt join for terminal closeout.
- Prove existing provider custody selects reconciliation and permits no new
  create.
- Prove zero external network/spend and privacy-bounded output.
- Provide API handoff and compatibility notes for retained 0.4.34 workspaces.

Gate — **Voof-paws 6** before release preparation.

## Conditional Slice 6 — release

Only if packaged/runtime SBE bytes change:

- freeze a fresh patch version before expensive tests;
- run a risk-proportionate affected matrix and installed qualifications;
- build reproducibly and record exact wheel/receipt hashes;
- obtain separate API and owner approval before commit/tag/publication.

## Test strategy

- Logs and exact retained evidence before mutation.
- Provider-free real-boundary characterization.
- Status/custody cross-product tests rather than one Glimmer-shaped case.
- Rehashed semantic mutations for public artifacts.
- Fresh-process restore and exact replay.
- Explicit counters for POST, GET, spend, and publication.
- No full-suite repetition due to a late version bump: candidate version freezes
  before any release suite.
