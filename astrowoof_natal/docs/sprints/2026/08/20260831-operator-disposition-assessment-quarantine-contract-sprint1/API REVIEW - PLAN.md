# API review — plan approval with contract refinements

## Decision

Approved to begin Slice 0. The sprint is correctly scoped as a narrow,
snapshot-validating, provider-free public projection. It gives API a supported
answer about native custody without allowing API to reconstruct private state or
to treat logs/status labels as authority.

The release can use the planned lean gate only if it remains strictly
read-only/additive. Any discovery that requires changing lifecycle,
reconciliation, provider, or native mutation behavior must pause and broaden
the qualification plan.

## Freeze these details in Slice 0/1

1. **SBE posture is native-only evidence, not an API resource assertion.**
   `quarantine_posture=permitted` must mean only that the assessed native
   evidence does not require an ordinary local authoring worker to remain
   scheduled. It must not claim a particular API lease/capacity allocation is
   safe, present, target-owned, or releasable. API proves those exact local
   rows under its own writer lock.

2. **Bind one exact assessment identity, not merely a matching run.**
   Include/validate a canonical `assessment_sha256` over every authoritative
   field and bind native run, route family/contract, compatibility identity,
   lifecycle revision, exact snapshot/checkpoint basis identity and digest,
   logical-root identifier, and every joined lifecycle/result/receipt identity
   used by the classification. A changed one requires a fresh assessment.

3. **Logical root must remain a logical identity.**
   Do not expose a host/R2/absolute filesystem path. The schema/validator
   should reject path-like private values if a bounded logical-root identifier
   is the supported public form.

4. **Freeze posture/action compatibility as a table.**
   In particular, `supported_next_actions` needs a canonical representation:
   either an empty ordered list or the singleton `none`, never both and never
   `none` mixed with another action. `sealed_terminal` must direct ordinary
   terminal ingress rather than imply arbitrary quarantine repair. Pending,
   completed-unadopted, providerless-authority, and ambiguous classes must each
   have an explicit permitted/prohibited/native-prior-action-required posture.

5. **Preserve mixed facts rather than flatten them.**
   The dominant class determines safe handling, but bounded subsidiary counts
   and assertions must reveal that, for example, pending provider custody and
   providerless authority coexisted. API will not derive an action subset from
   this summary.

6. **Terminal evidence remains reader-bound.**
   A sealed-terminal class must be established only through a supported exact
   result/receipt/checkpoint join (or the existing narrowly supported
   availability reader, if Slice 0 explicitly documents its bounded semantics).
   A status label, index entry, or discovery heuristic alone is insufficient.

7. **Assessment must be deterministic and diagnostic-only.**
   Same exact public evidence produces byte-identical bytes/digest. Logger or
   event-sink failure must be isolated. The CLI cannot accept credentials,
   provider/recovery/authority input, or a workspace mutation flag.

## API handoff expectation

After Slice 1 freezes the schema and validator, API can implement its durable
request/admission mapping against the exact vocabulary. It should not wire a
real runner operation or local resource release until SBE's reader/projection
and released wheel have qualified the public assessment end-to-end.

No retained-QA access, provider action, workspace mutation, deployment, tag,
or release is authorized by this review.
