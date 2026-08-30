# AstroWoof Natal Authoring Maintainer Release Playbook

## Purpose

This is the living maintainer guide for qualifying a new
`astrowoof-natal-authoring` release. Version-specific installation and consumer
instructions remain under `astrowoof_natal/releases/<version>/`; sprint records
remain historical evidence.

The runtime packages more than Python code. Its behavior includes extraction,
authoring guidance, response schemas, deterministic acceptance, validation,
lint, approved references, orchestration, retry, assembly, polish, provenance,
and delivery. Those resources release atomically and are fingerprinted as one
policy bundle.

## Qualification sequence

Use bounded sprint slices with explicit gates:

1. **Freeze the fresh release identity before expensive testing.** Select an
   unreleased version, update `pyproject.toml`, and refresh every deterministic
   fixture, manifest, receipt, expected wheel name, and handoff field whose
   content identity includes the distribution version. Run the focused
   release-identity/packaged-fixture tests first. The full suite MUST NOT begin
   while the candidate still carries an already-published version or while a
   version-bound fixture still expects the previous release.
2. **Package and dependency audit.** Inventory modules, entry points, package
   data, subprocesses, external contracts, compatibility shims, and generated
   material that must remain excluded.
3. **Installable package boundary.** Build and install outside the checkout;
   resolve resources through the package; exercise every supported CLI.
4. **Stable contracts.** Version input, parameters, authoring profile,
   operator/public state, provenance, and delivery behavior before publication.
5. **Provenance.** Hash normalized inputs, packaged resources, final artifacts,
   QA, and delivery; copy upstream declarations only when present.
6. **Packaged deterministic QA.** Run `astrowoof-release-smoke
   --require-installed` from outside the source tree and exercise retry, resume,
   assembly, delivery integrity, and cleanup.
7. **Adversarial lifecycle qualification.** For lifecycle, provider-custody, or
   authority changes, run the installed provider-free adversarial qualification.
   If API translation, leases, capacity, or scheduling are affected, require the
   API joined campaign against the same candidate and catalog.
8. **Controlled live candidate.** Use a known subject and real provider only
   after deterministic gates pass. Record attempts, usage, cost, QA, and any
   defect found.
9. **Reproducibility and publication.** Build twice with controlled timestamps,
   require byte-identical wheels, produce checksums and handoff documents, tag
   the qualified commit, publish assets, download them again, and reverify.

Every slice updates `PLAN.md`, `LOG.md`, and a compact result under
`results/`. A discovered defect is a successful QA finding: add regression
coverage, rerun affected gates, and do not waive the exit criterion.

## Installed-runtime discipline

Source-checkout tests cannot prove packaging. The strongest deterministic gate
uses a fresh environment, a working directory outside the repository, and
`--require-installed`. It must verify that console entry points, executable
modules embedded into handoffs, schemas, guidance, fixtures, and reference
resources all come from `site-packages`.

Keep legacy source scripts only as compatibility shims. The installed package
and versioned JSON contracts are the production boundary; internal module
layout is not a public v0.1 API.

## Compatibility discipline

Before each release, test the exact intended AGF/SPC boundary rather than
assuming a version range is sufficient. Verify:

- all four projected contexts and their embedded context IDs;
- canonical source identity and graph references;
- engine, profile, context, ontology, and projected-term registry identities;
- exact source-object and source-relationship coverage;
- accepted subject-parameter versions; and
- downstream deck/delivery contract compatibility.

Filenames are discovery and transport labels. Embedded versioned metadata is
semantic authority and must be validated rather than reconstructed from a
filename.

The v0.1 runtime couples package `subject_id` to canonical source identity
`natal:<subject_id>`. AGF 0.6's caller-owned opaque `source_chart_id` is a known
future contract-evolution point. Resolve it explicitly before claiming an
AGF-0.6 production compatibility set.

## Retry and state invariants

- Transport retries do not consume creative attempts.
- Creative attempts are independent responses, but their public repair
  constraints are cumulative within one pass. A later retry must retain every
  distinct earlier rejection issue so fixing one constraint cannot regress
  another.
- A timed-out local polling window resumes the persisted provider response; it
  does not submit a duplicate request.
- Durable acceptance evidence wins over stale state and cannot be demoted by
  resume.
- `run.json` is operator recovery/audit state. `public-run.json` is the atomic,
  path-free polling contract. HTTP status handling reads public state and never
  mutates the run.
- Only one worker may mutate a run directory; distributed lease ownership
  belongs to the API/control plane.

## Release identity and secrets

The release record must tie together:

- distribution version and release commit;
- annotated component-scoped tag;
- wheel filename, size, and SHA-256;
- aggregate packaged-resource SHA-256;
- supported contract/profile versions;
- installed-smoke evidence; and
- downloaded publication verification.

The private GitHub credential used to retrieve a wheel is an ephemeral build
secret. `OPENAI_API_KEY` is a runtime worker secret. Neither belongs in source,
requirements, image layers, logs, run artifacts, public state, or delivery.

## Release exit criteria

For any release containing Semantic Closure v0.8 or later, promotion also
requires:

- no OpenAI path can submit without a prepared and consumed paid action;
- initial authoring, creative retry, polish, critic, and qualitative candidate
  appear as separate ledger stages;
- prepare/authorize/execute and polling-only resume pass from an installed
  artifact;
- failure injection proves the PREPARED, SUBMITTING, provider-ID, and reported
  usage persistence boundaries;
- legacy OpenAI state fails closed;
- hard exhaustion, optional profile-driven skipping, and ambiguous submission
  remain distinct machine states;
- the pinned price book and all generation-specific ceilings are explicit;
- provider idempotency claims match published provider guarantees; and
- the consumer handoff assigns cross-run reservation and billing authority to
  the API.

For a release that changes lifecycle commands/results, local-work projection,
provider custody, external authority, wrapper translation, capacity disposition,
or scheduler-facing evidence, promotion also requires:

- installed `astrowoof-adversarial-qa` from the exact candidate wheel;
- zero external network/provider calls, spend, and retained-QA access;
- named historical and malformed fixtures returning their expected classification;
- fixed seed/depth/time budgets and any unexplored frontier recorded;
- newly discovered failures minimized and promoted to deterministic fixtures; and
- a joined API receipt when the changed claim depends on API persistence, lease,
  capacity, reservation, or scheduler behavior.

See
[Adversarial Lifecycle Simulation Playbook](Adversarial%20Lifecycle%20Simulation%20Playbook.md).

For v0.9 or later, also verify the provider-disclosure allowlist across
initial authoring, creative retry and Batch construction, polish, critic, and
candidate requests. Exercise exact-path snapshot restore and rejection of a
missing, additional, truncated, changed, or relocated member. Retain release
assertions for selected-card versus broader whole-dog evidence provenance,
projected-term registry merge and closure, monotonic accepted evidence, all
machine-distinguishable run outcomes, and exact AGF 0.6 / SPC 0.10 identity
propagation through claims, synthesis, authoring state, delivery provenance,
and the installed-wheel smoke. Unknown-time suppression, variable basis size,
Quick/Complete, hierarchy redesign, and critic product policy remain deferred.

A release is complete only when:

1. the full relevant suite passes;
2. the wheel builds reproducibly;
3. clean installed-runtime smoke passes outside the checkout;
4. the intended exact upstream compatibility set passes;
5. controlled live QA passes when authoring behavior changed materially;
6. manifests, checksums, compatibility, release notes, and consumer handoff
   agree;
7. the annotated tag points to the qualified commit;
8. published assets verify after download;
9. temporary large artifacts are cleaned; and
10. component and cross-project documentation reflect the released baseline.

If one condition is unmet, the result is a candidate or a blocked release, not
a release with an implicit waiver.

## Related procedures

- [Native Worker Change Playbook](Native%20Worker%20Change%20Playbook.md)
- [Adversarial Lifecycle Simulation Playbook](Adversarial%20Lifecycle%20Simulation%20Playbook.md)
