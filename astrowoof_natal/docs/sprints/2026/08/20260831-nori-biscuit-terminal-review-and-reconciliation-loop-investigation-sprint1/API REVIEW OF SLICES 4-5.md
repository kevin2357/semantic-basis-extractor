# API review of Slices 4–5

## Decision

The Nori correction is approved in substance. It may proceed to Slice 6
packaging/release-scope work after the scope correction below is made.

## Confirmed implementation merits

- Deferring the *earlier* authoring-pass progress seal only when every
  advertised operation belongs to an optional/finalization stage is the right
  narrow boundary. It preserves immediate authoring/creative-retry behavior
  and avoids treating all local work as deferrable.
- Reloading writer-committed `run.json` state after local-progress commit is
  necessary: later coordinator publication must not overwrite cumulative
  consumed-operation history.
- The real `finalize_subjects()` / `polish_subject()` regression now meets the
  prior review requirement. It uses persisted completed-response evidence and
  real settlement/adoption, with provider transport fail-on-call, and proves
  consumption, stable-key persistence, absence of the contradiction result,
  and truthful successor disposition.
- Biscuit remains explicitly out of scope. No speculative creative-retry
  workaround should enter this release.

## Required release-scope correction

The current working diff includes unrelated run-evolution reporter exports and
console-script entries in `__init__.py` and `pyproject.toml`, alongside
untracked reporter sources/resources. Those are valuable work, but they belong
to the reporter sprint, not this Nori ordering patch.

Before Slice 6, either commit that reporter work through its own reviewed
sprint/release path, or leave it excluded from this patch/release candidate.
The Nori release candidate should contain only the optional-stage ordering
change, committed-state reload, required regression(s), and directly related
documentation/versioning.

## Slice 6 requirements

- Run the focused suite already identified plus installed-wheel/package checks
  appropriate to the actual changed public/package surface.
- State explicitly that no lifecycle/result schema changes are included.
- Preserve the independent API follow-up: receipt/result ingestion must retain
  reconciliation custody when native v0.2 review says it is required.
- Do not use the retained Nori/Biscuit workspaces as release qualification.

No provider work, QA recovery, or deployment is approved by this review.
