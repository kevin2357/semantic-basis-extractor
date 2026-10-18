# 0.4.72 release precheck — 2026-10-18

**Disposition: precheck complete; see the release-lock record for the current
release process.**

The retained canonical candidate has SHA-256
`298273523a05c7a72cdd5404ca1727ef3f03c5c922785a7c5ba4da6f2990c364`;
its source, fixed epoch, size and two matching canonical archive builds are
recorded in [Slice 3B](SLICE%203B%20-%20CANONICAL%20REPLACEMENT%20CANDIDATE.md).
The earlier `dadd…` candidate is superseded and must not be published.

The manifest-driven source qualification recorded for `986e05ea` ran 1,267
tests with 62 skips and no failures or errors. On 2026-10-18, the existing
isolated environment installed from the retained canonical candidate passed:

- `pip check`;
- `astrowoof-release-smoke --require-installed`, with `status: pass`; and
- `astrowoof-adversarial-qa`, with `status: pass`, zero external network
  calls and zero real-provider creates.

The retained provider-free receipts are
`C:\tmp\sbe-0472-release-smoke-20261018.json` and
`C:\tmp\sbe-0472-adversarial-20261018.json`. The first sandboxed attempts
failed to create temporary files due to Windows sandbox permissions; both
checks were rerun outside the sandbox and passed. These are prechecks using
the existing candidate environment, not the playbook's final fresh-install
qualification or a release-lock rebuild.

API's sprint status reports that the joined installed-candidate grant, command,
receipt, exact-replay and altered-grant test passed. Its later custody work
also records a 28-case installed-wheel matrix with explicit limitations.
At the time of this precheck API's status said Gate D was open, so publication
was paused. API subsequently updated its status and approved the exact candidate
for package release on 2026-10-18. See its `API GATE D - 0.4.72 PACKAGE
RELEASE REVIEW.md`. This does not constitute QA deployment approval; the API
review records remaining coverage and alerting limitations.

No release-lock commit, release tag, publication, deployment, activation, or
real-provider work was performed during this precheck.
