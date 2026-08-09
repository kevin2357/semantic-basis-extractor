# AstroWoof Natal Authoring 0.2.2

This patch corrects SBE 0.2.1 checkpoint integrity and recovery at a polish
retry spend-authorization boundary.

## Changed

- spend callbacks persist early ledger/public evidence without publishing a
  non-quiescent workspace snapshot;
- coordinator exits publish one complete checkpoint after paid-stage mutation
  unwinds;
- subject and polish-attempt state survive a next-attempt authorization pause;
- pending `SUBMITTED` polish attempts are reused on resume;
- background Response markers precede ledger-ID persistence, matching markers
  reconcile with GET only, and conflicts fail closed as ambiguity;
- local polish installation failures stop before another paid attempt;
- `astrowoof-repair-polish-checkpoint` provides constrained dry-run/apply
  recovery for the proven 0.2.1 shape; and
- `critic-findings.json` is now the versioned private
  `astrowoof.qualitative_critic_findings.v0.1` consumer artifact with direct
  provenance, packaged schema/catalog authority, and a sanitized fixture.

The canonical retained 0.2.1 run was not changed. A separate copy was repaired,
validated, and resumed offline to the exact unused action-2 boundary with zero
provider transport calls.

## Qualification

- complete repository suite: 166 passed;
- two wheel builds: byte-identical;
- wheel SHA-256:
  `98e8ab142bc4c1dc97fdc53019fb6d2e16d23736f12ca9085119b79fdc842b7e`;
- Windows and Linux clean-install smoke: pass;
- installed resource count/digest: 21 /
  `eb08dcde591479a943ab4461bba08d68361631d748634830ba36888e459b7a7f`;
- exact-wheel Linux repair dry run against the retained backup: eligible;
- new provider operations and spend: zero.

Tagging and publication remain pending separate authorization.
