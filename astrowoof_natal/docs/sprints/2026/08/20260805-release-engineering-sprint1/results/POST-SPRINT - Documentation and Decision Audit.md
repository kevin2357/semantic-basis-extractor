# Post-Sprint Documentation and Decision Audit

## Scope

This audit reread the August editorial-quality, cleanup, and release-engineering
sprint logs against the durable component and project documentation after an
active six-repository integration day.

## Findings promoted to durable documentation

1. Added a maintainer release playbook so reproducible-build, installed-runtime,
   controlled-live, publication-verification, and cleanup practices do not
   remain implicit in one sprint log.
2. Clarified that filenames discover or route candidates while embedded SPC
   context metadata remains semantic authority.
3. Promoted cumulative creative-retry constraints as a durable invariant: a
   later repair retains all distinct earlier rejection issues.
4. Clarified that the aggregate resource digest identifies the complete
   authoring policy bundle, not merely Python source.
5. Corrected the documented sprint-directory convention for new work while
   preserving historical paths.
6. Marked the completed `Pending SBE and LLM Handoff Updates.md` checklist as
   historical and routed readers away from its superseded free-text
   `theme_group` design to the current v0.4 registry contract.

## Newly identified compatibility boundary

The released v0.1 extractor requires projected canonical source identity
`natal:<subject_id>`. AGF 0.6 now accepts caller-owned opaque
`source_chart_id`, intentionally separate from display name and product dog ID.

This is not a defect in the already qualified v0.1 Bre/Ella release basis, and
the retrospective does not alter released runtime behavior. It is a required
future contract-evolution and compatibility-test item before the project claims
an AGF-0.6-to-authoring-v0.1 production set. The durable runtime and v0.1
compatibility documents now state the boundary explicitly.

## ADR audit

No new component or project ADR is justified solely by the release sprint:

- keeping Semantic Closure with SBE and releasing it atomically is already
  accepted by project ADR-0002;
- treating LLM work as a durable artifact pipeline is already accepted by
  project ADR-0003;
- independent aspect/synthesis organization is already accepted by project
  ADR-0005;
- immutable artifact pinning and release qualification are operational policy
  in the project Release Strategy; and
- cumulative retry constraints, metadata-over-filename validation, packaged
  resource hashing, and accepted-state recovery are component implementation
  invariants rather than cross-system architecture choices.

The AGF opaque-identity integration may require a shared contract update, but
the identity architecture itself is already represented in the project
canonical-chart contract and AGF documentation. SBE should not create a
competing ADR before that integration is designed.

## What surprised us

- Packaging was more direct than expected once the runtime was isolated behind
  a strict allowlist and `importlib.resources`; the installed wheel remained
  dependency-free.
- Source-tree success hid real release risks. Installed smoke caught resource
  and subprocess assumptions, while controlled live QA found retry-feedback
  oscillation that deterministic happy-path testing did not expose.
- The first live candidate's safe failure was valuable evidence. Accumulating
  rejection constraints removed the oscillation without exposing opaque
  thresholds or continuing a rejected model conversation.
- Release qualification needed both deterministic smoke and controlled live QA:
  neither substituted for the other.

## Authority and follow-up

The sprint logs remain historical evidence. The new maintainer playbook and
runtime-contract updates are component authority. Cross-system ownership,
release baselines, and shared identity policy remain owned by
`astrowoof-project`.

AGF 0.6 is now published. The remaining follow-up is to design and test a new
authoring input contract that separates package subject identity from canonical
`source_chart_id`, then update the API worker handoff and exact compatibility
matrix before promoting the real domain adapter.

## Cross-project reconciliation

A subsequent bidirectional audit compared this component's released behavior
and documentation with the living authority in `astrowoof-project`. No material
project-level statement about the authoring runtime required correction. In
particular, the project accurately records the six-pass artifact workflow, the
division between deterministic acceptance and bounded editorial polish, the
v0.4 independent aspect/synthesis chapter registries, the immutable v0.1.0
release coordinates, and the current `natal:<subject_id>` compatibility seam.

The project record did disprove two stale time-relative assumptions here: AGF
0.6 is published, and the AstroWoof API now has an implemented control-plane
foundation. Neither fact means that the real AGF/SPC/SBE production adapter is
complete or that the three released wheels have passed the planned exact-tuple
integration gate.

## Verification

- Full regression suite: 118 tests passed.
- `git diff --check`: passed.
- New component-document links: resolved locally.
- No production code, schema, packaged resource, tag, or published release
  artifact was changed by this retrospective.
