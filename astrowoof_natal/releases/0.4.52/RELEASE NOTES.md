# AstroWoof Natal Authoring 0.4.52

SBE 0.4.52 adds a diagnostic-only shared-time cohort swimlane to the existing
run evolution reporter.

The release adds:

- the closed `astrowoof.sbe_run_cohort_timeline.v1` projection, schema, reader,
  validator, and deterministic reducer;
- explicit native-SBE versus API-wrapper evidence ownership and clock fields;
- a self-contained interactive horizontal timeline with one common axis;
- `astrowoof-run-report timeline` and `timeline-html` rendering;
- optional timeline artifacts from ordinary reporter builds when suitable
  mixed evidence is present; and
- the provider-free `astrowoof-run-timeline-qa` installed qualification with a
  closed deterministic receipt.

The existing run-evolution report v1 and its four established native-only
outputs remain unchanged. Timeline artifacts are diagnostic observations, not
lifecycle, custody, scheduler, settlement, or terminal authority. Observed
lease windows do not assert global slot ownership, and witnessed handoffs are
not SLAs.

Compatibility remains pinned to `semantic-projection-core==0.11.1`. Windows
installs now declare `tzdata`, which the standard-library timezone renderer
requires when the operating system provides no IANA timezone database. No
provider or retained-QA access is required for qualification.
