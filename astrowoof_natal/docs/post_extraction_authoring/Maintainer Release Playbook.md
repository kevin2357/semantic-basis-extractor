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

## Normative release invariants

Every release MUST satisfy these rules:

- The distribution version is frozen to a fresh, unreleased value before any
  release-bound regression suite, fixture digest, wheel name, or receipt is
  treated as final.
- The released source is a committed identity. Wheels are not promoted from an
  uncommitted or tracked-dirty checkout.
- Two builds from the same committed identity use one recorded
  `SOURCE_DATE_EPOCH` and MUST be byte-identical.
- The wheel is inspected for expected package data and for forbidden stale,
  generated, cache, bytecode, private, or untracked members.
- The exact qualified wheel—not a later rebuild with the same version—is the
  artifact uploaded to GitHub.
- The component-scoped annotated tag is exactly
  `astrowoof-natal-authoring-v<version>` and points to the release-lock commit.
  A bare `v<version>` tag is not an SBE release tag.
- The GitHub Release contains the exact wheel and `SHA256SUMS.txt`.
- A fresh authenticated download of both assets MUST reproduce the qualified
  wheel SHA-256 and checksum line before the release is called complete.
- Publication evidence is recorded in a later ordinary documentation commit.
  That commit MUST NOT move, replace, or recreate the immutable release tag.

The artifact-source commit, release-lock/tag commit, and post-publication
evidence commit may be different. The release record must name each one
accurately; `main` after publication is not necessarily the tag target.

## Regression-test gate selection

SBE uses two release regression gates. In this repository, **broad suite** and
**full suite** mean the complete supported repository test discovery. A selected
multi-module matrix is an **expanded focused suite**, not a broad/full suite.

Choose the gate from the final diff and the semantic blast radius, not from the
requested version label or desired release speed. Record the choice and rationale
in sprint evidence before release approval.

### Focused patch gate

The focused gate MAY be used when all changed behavior is demonstrably narrow
and every affected caller/consumer can be enumerated. Typical examples are:

- documentation or packaged-fixture corrections;
- an additive read-only reader, schema, fixture, or qualification command;
- a localized validator/policy correction with no shared lifecycle mutation;
- a narrowly fenced defect whose production callers and route/stage cells are
  all covered directly; or
- build/release metadata with no runtime semantic change.

The focused gate MUST include:

1. the regression that reproduces the reported defect or contract gap;
2. all directly changed unit/schema/validator tests;
3. tests for every known production caller and every affected route, stage, and
   mechanism cell, including every packaged qualification whose fixture calls
   the changed selector/reducer even when that qualification's own source file
   did not change;
4. adjacent negative controls proving nearby unsupported or safety-critical
   behavior did not widen;
5. release-identity and version-bound fixture tests;
6. `git diff --check` and a review of the complete final diff;
7. clean installed-wheel `pip check`, package/resource inventory, public reader
   and CLI smoke, and the feature-specific installed qualification; and
8. an explicit evidence statement that the broad/full suite was not run, plus
   reviewer and owner acceptance of that proportionate gate.

If the affected callers or semantic consequences cannot be enumerated with
confidence, the focused gate is not sufficient.

### Broad/full regression gate

Run the broad/full suite when a change can affect multiple subsystems or an
open-ended set of callers. This includes changes to shared orchestration,
workspace/snapshot persistence, state transitions, reconciliation, provider
custody, authority, retry lineage, finalization, concurrency/writer fencing,
common validators/reducers, package/dependency layout, or cross-repository
public contracts. It is also required when focused testing reveals unexplained
collateral behavior or when review cannot bound the blast radius.

The broad gate MUST still begin with the focused gate. Only after the focused
matrix is green should the complete suite run, normally as:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
```

Record total cases, passes, expected skips, failures, duration, interpreter, and
the exact commit/version tested. A broad run with any unexplained failure is not
green.

### Rerun policy after a late correction

- Any runtime, schema, validator, package-data, or test-harness logic change
  after the broad suite starts requires the affected focused matrix again and,
  by default, another broad run.
- A correction limited to a release-derived expected version, wheel filename,
  checksum, receipt digest, or documentation may use an affected focused rerun
  plus final installed-wheel qualification instead of repeating an otherwise
  successful broad run. The evidence MUST identify the original failure, the
  exact correction, why runtime behavior was untouched, and that the broad run
  was not repeated. Reviewer and owner acceptance is required.
- Never silently describe a partially failing broad run as passing. Preserve
  the actual result and the narrower superseding evidence.
- Do not rerun a successful broad suite merely because the version was bumped
  afterward: that situation is prevented by freezing the version before the
  first release-bound suite.

## Exact immutable publication procedure

Use this sequence for every GitHub release:

1. Confirm `main`, upstream compatibility pins, and the next unused version.
   Update `pyproject.toml` and every version-derived fixture before expensive
   testing.
2. Run the selected focused or broad regression gate and record exactly what
   ran.
3. Commit the final artifact source. Confirm no unintended tracked drift and
   inspect untracked files under package-data roots.
4. Remove or isolate stale generated build directories. Prefer a clean committed
   source export/worktree so old `build/lib` content or untracked package data
   cannot enter the wheel.
5. Set one recorded `SOURCE_DATE_EPOCH`, build into two independent directories,
   and require identical
   filenames, sizes, member inventories, and SHA-256 hashes.
6. Clear `SOURCE_DATE_EPOCH` before installing on Windows; an epoch before 1980
   can break pip's generated console-script ZIP metadata even when the wheel is
   valid.
7. Install the exact candidate wheel into a clean isolated environment. Run
   `pip check`, confirm imports resolve from `site-packages`, verify the installed
   version, and execute required generic and feature-specific public commands.
8. Record the exact candidate coordinates and qualification evidence in a
   release-lock commit. Rebuild twice from that exact commit using its recorded
   `SOURCE_DATE_EPOCH` (normally the release-lock commit timestamp), and repeat
   the installed qualification. If any package-affecting content changed, return
   to the applicable regression gate.
9. Obtain required consumer/reviewer approval and explicit owner authorization
   to tag and publish this exact candidate.
10. Create `SHA256SUMS.txt` for that exact wheel. Do not rebuild or substitute
    the wheel after qualification.
11. Create annotated tag `astrowoof-natal-authoring-v<version>` at the
   release-lock commit; push `main` and that exact tag. Verify the remote peeled
   tag target.
12. Create the GitHub Release for that tag and upload only the exact qualified
    wheel and `SHA256SUMS.txt`. Read back the release ID, asset IDs, sizes, and
    GitHub-reported digests.
13. Download both published assets into a fresh separate directory. Recompute
    the wheel SHA-256 and compare it with the qualified build, GitHub asset
    digest, and downloaded checksum manifest.
14. Record the release URL, release/tag/asset identities, published time, and
    download verification in a post-publication documentation commit. Push that
    commit while proving the tag still resolves to the release-lock commit.

If a wrong tag is pushed before asset publication, stop and inspect it. Delete
or replace even an unpublished tag only with explicit owner authorization. Never
move a tag that has been used for an immutable published release; publish a fresh
patch version instead.

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

1. the selected focused or broad/full regression gate passes and its rationale
   is recorded;
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
