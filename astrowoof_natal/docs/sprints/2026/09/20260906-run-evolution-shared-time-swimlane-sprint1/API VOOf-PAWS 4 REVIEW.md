# API Voof-paws 4 review — reducer corrections and shared-axis renderer

## Decision

**Approved.** The two prior reducer mismatches are corrected consistently:

- `adapter_coverage` is a defined, required closed projection member; and
- `observed_execution_allocation` is a defined closed classification with the
  conservative observed-allocation meaning, not global slot authority.

The added end-to-end fixture proves a nonzero adapter-coverage projection with
a paired acquire/release interval survives the public reader/validator.

## Renderer review

`render_run_cohort_timeline_html()` is aligned with the diagnostic boundary:

- it uses the validated canonical projection and a single absolute axis;
- it retains evidence details, labels, patterns, and accessible controls;
- it preserves timezone as presentation only;
- it makes no lifecycle, provider, custody, or scheduler decision; and
- it embeds no remote asset or network dependency.

Focused verification observed: 36 tests passed, with one expected optional
JSON-Schema-library skip. API approves the sprint to proceed to CLI/existing
output integration.
