# API Slice 4B Review

Status: **conditionally approved; one witness-scope correction required before
release qualification resumes.**

## Approved contract behavior

The implementation correctly takes the aggregate-member interpretation adopted
in `API SLICE 4B PRODUCTION-PATH INTERPRETATION.md`:

- the later-completed retry selects `ordinary_resume` while the earlier provider
  operation remains retained;
- retained provider custody masks successor dispatch until the remaining result
  is reconciled and locally consumed;
- the co-ready successors then appear in one lexical `ordinary_action_set`; and
- that envelope has distinct member bindings and authorization documents, is
  dispatched all-or-none, and replays without extra create or local consumption.

The public surface, closed fixture inventory, digest/receipt joins, installed
CLI, privacy boundary, and the truthful `detached_provider_pending` endpoints
are all aligned with the API request. The qualitative-critic choice is also a
better honest downstream witness than fabricated polish.

## Required scope correction

The current internal builders directly mutate `run.json` to mark retries
reported and append their successor prepared actions:

- `_mark_reported_and_prepare_successor` performs this for both successors in
  the two-retry witness; and
- the critic witness directly marks the retry/pass accepted before invoking the
  real `SpendController` callback to prepare the critic.

That setup can be useful for a narrow production-*shaped* selector/authority
witness, but it is not evidence that normal production continuation generated
those predecessor acceptance facts or successor actions. The handoff and LOG
currently call the artifacts "real-engine witnesses" without exposing that
boundary, which would overstate what API can rely on for Sprint 54 Slice 3B.

Please make one of these explicit resolutions before release qualification:

1. Preferred if a supported production route is available: derive the relevant
   reported/accepted/successor state through that route, so the real-engine claim
   remains end-to-end; or
2. Narrower and acceptable for this release: retain the deterministic private
   fixture setup, but rename/re-document the artifact as a
   **production-shaped, real-selector/authority witness**. State exactly which
   precursor facts are fixture-installed and that the installed claim begins at
   the public post-fan-in/ordinary-v2 boundary. API will use it for the
   mixed-custody selector, custody precedence, ordered aggregate-authority, and
   replay claims only—not as proof of upstream result evaluation or final-stage
   selection.

Option 2 should also make the distinction machine-visible in the public fixture
metadata or witness projection (for example, an exact closed `evidence_scope`),
not merely prose in an internal helper. It must remain privacy-safe and must not
expose workspace state or provider payloads.

Once that evidence-scope correction is made, the witness is good to proceed
through fresh installed-wheel qualification and release preparation.
