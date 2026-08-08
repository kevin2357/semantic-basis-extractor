# AstroWoof Natal Authoring Runtime Contracts

This document defines the stable v0.1 boundary presented by the installed
`astrowoof-natal-authoring` runtime. Contract versions identify data shape and
meaning; the Python distribution version identifies implementation behavior.

## Projected input bundle

Canonical schema: `astrowoof.projected_natal_input.v0.1`.

The runtime accepts either the historical directory convention or an explicit
`astrowoof-input-manifest.json`. Both normalize to the same internal manifest.
An explicit manifest has this shape:

```json
{
  "schema_version": "astrowoof.projected_natal_input.v0.1",
  "subjects": [
    {
      "subject_id": "ella",
      "contexts": {
        "general": "ella/natal.ella.woof.general.json",
        "direct_to_dog": "ella/natal.ella.woof.d2d.json",
        "handler": "ella/natal.ella.woof.handler.json",
        "hybrid": "ella/natal.ella.woof.hybrid.json"
      }
    }
  ]
}
```

Paths are relative to the package root, cannot escape it, and must identify
files. A subject's four projected contexts must share one directory. Optional
`params.json` remains beside those contexts.

Legacy direct or one-directory-per-subject layouts remain supported. Their
normalized manifest records `source_format: legacy-directory-v0`; explicit
manifests record `source_format: manifest-v0.1`.

Manifest context keys are the caller's explicit routing declaration. Legacy
filenames are used only to discover candidate files. In both forms, extraction
validates the embedded SPC projection-context metadata and rejects a file whose
declared context does not match its assigned route. Renaming or routing a file
does not rewrite its semantic context.

### Subject routing and canonical-source identity

The input-package `subject_id` is a routing key. It identifies the subject's
four context files and joins optional `params.json`; it does not determine or
constrain the canonical source identity embedded in those projected graphs.

Every context must declare the same non-empty `source_identity` object. Its
identifiers are opaque and are preserved unchanged, so an AGF UUID
`source_chart_id` is valid and need not resemble `natal:<subject_id>`. SBE
rejects mixed canonical identities across contexts but does not infer identity
from the routing key, display name, filenames, or subject metadata.

Historical `natal:<subject_id>` identities remain valid opaque identifiers for
legacy packages.

## Subject parameters

Canonical schema: `astrowoof.subject_params.v0.1`.

Unversioned historical `params.json` files are accepted and normalized to this
version. Supported fields are `subject_id`, `display_name`, `subject_type`,
`gender`, `pronouns`, `breed`, `birth_date`, `birth_datetime`,
`birth_latitude`, `birth_longitude`, `birth_location`, and
`birth_date_precision`. Coordinates are range checked. Pronouns may contain
`subject`, `object`, `possessive_adjective`, `possessive_pronoun`, and
`reflexive`.

## Authoring profile

Canonical schema: `astrowoof.authoring_profile.v0.1`.

Every new run freezes its behavior-affecting extraction, authoring, routing,
cache, QA, polish, and qualitative-review options into `run.json`. The current
profile ID is `astrowoof-natal-default-v0.1`. This makes a completed run
interpretable without reconstructing its command line.

## Operator run state

Canonical schema: `astrowoof.semantic_closure_run.v0.9`.

`run.json` is the durable operator record and resume source. It intentionally
contains filesystem locations, pass attempts, provider configuration,
acceptance evidence, usage, costs, final QA, and delivery records. V0.8 added a
state revision, stable run ID, and durable provider-spend ledger. V0.9 adds an
explicit provider-disclosure inventory and a hashed complete-workspace
snapshot bound to one stable logical absolute path.

Legacy fake-provider states remain test-migratable. OpenAI states older than
v0.9 fail closed because creation-time commitments and authorization evidence
cannot be reconstructed safely. See `Provider Spend Enforcement.md` and
`Spend Authorization Consumer Handoff.md`. Every v0.9 resume also validates
`workspace-snapshot.json`; missing, changed, additional, or relocated snapshot
content fails closed before persisted paths or provider work are used.

## Public run state

Canonical schema: `astrowoof.semantic_closure_public_run.v0.1`.

Every operator-state save also atomically writes `public-run.json`. This is the
API polling view: status and timestamps, service level, accepted/total pass
progress, per-subject state, and delivery readiness. It excludes paths,
provider configuration, prompts, attempts, and internal evidence.

## Delivery manifest

Canonical schema: `astrowoof.natal_delivery_manifest.v0.1`.

Each subject delivery ZIP contains its deck, assembly report, validation
report, lint report, and delivery manifest. The manifest identifies the
subject, final status, run contract, authoring profile, artifact roles, byte
sizes, and SHA-256 digests. The ZIP digest is recorded in operator run state,
avoiding the impossible requirement that a ZIP contain its own checksum.

## Provenance

Canonical schema: `astrowoof.natal_authoring_provenance.v0.1`.

New runs record the installed runtime version and Python class, the exact
packaged-resource set and aggregate digest, every normalized input artifact
and SHA-256 digest, declared upstream AGF/SPC metadata found in each projected
graph, the authoring profile, observed model names, attempt count, final QA
report identities, and delivery ZIP digest.

Declared upstream metadata is copied only when present. Missing engine,
profile, graph, context, or source identifiers remain absent; the runtime never
infers them. Runs migrated from older state explicitly mark input provenance as
unavailable because creation-time hashes cannot be reconstructed reliably.

The aggregate packaged-resource digest is release identity for the complete
authoring policy bundle, not just Python source. A change to bundled schemas,
authoring guidance, validators, or approved references requires a new qualified
runtime artifact even when the public Python entry point is unchanged.

## Compatibility policy

- Additive fields may appear within a contract version when old consumers can
  safely ignore them.
- Meaning changes, required-field changes, or renamed fields require a new
  contract version.
- Readers must reject unsupported explicit input versions rather than guessing.
- Legacy inputs are accepted only through documented normalization paths.
- The reader-facing deck remains independent of operator-state contracts.
