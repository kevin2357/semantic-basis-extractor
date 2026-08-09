# Slice 5 - Patch Artifact and Consumer Handoff

Status: release candidate complete; gate approval pending.

## Candidate

- distribution: `astrowoof-natal-authoring`;
- version: `0.2.2`;
- wheel: `astrowoof_natal_authoring-0.2.2-py3-none-any.whl`;
- bytes: 633,073;
- SHA-256:
  `98e8ab142bc4c1dc97fdc53019fb6d2e16d23736f12ca9085119b79fdc842b7e`;
- entries: 44; bytecode/cache entries: 0;
- two independent builds: byte-identical.

The candidate remains local under `C:\tmp\sbe-0.2.2-build-a`. No tag, release,
asset upload, or publication occurred.

## Qualification

- complete deterministic repository suite: 166 passed;
- Windows clean install and `pip check`: pass;
- Windows installed smoke: `DELIVERY_COMPLETE`;
- Linux Python 3.11 clean install and `pip check`: pass;
- Linux installed smoke: `DELIVERY_COMPLETE`;
- resource count/digest on both platforms: 21 /
  `eb08dcde591479a943ab4461bba08d68361631d748634830ba36888e459b7a7f`;
- exact-wheel Linux installed repair dry run against the read-only retained
  backup: eligible with the frozen three hashes and unused action 2;
- provider operations, authorization consumption, and incremental spend: zero.

## Critic consumer contract

`critic-findings.json` is now the normative private
`astrowoof.qualitative_critic_findings.v0.1` artifact. The wheel packages its
JSON Schema, catalog registration, sanitized canonical fixture, direct deck and
raw-response hash provenance, Response ID/configuration, and run/profile/
runtime/resource identities. Unsupported versions fail closed. The old Kevin
and Ella live files remain noncanonical unversioned evidence.

The API may implement Slice 5 ingestion against v0.1 immediately after pinning
the published 0.2.2 artifact. Complete prose and paths remain in immutable
private JSON; PostgreSQL may index bounded operational dimensions plus the
artifact hash/reference.

## Handoff

- `API AGENT RESPONSES.md` answers all twelve question groups with confidence,
  evidence, uncertainty, authority, compatibility, and consumer consequences.
- `releases/0.2.2/RECOVERY ADVISORY.md` defines constrained repair operations.
- `releases/0.2.2/API WORKER INTEGRATION.md` defines API ownership and pins.
- `releases/0.2.2/release-manifest.json` remains `candidate`, with publication
  pending and source commit intentionally unset until the approved candidate
  commit exists.

Next action: approve the Slice 5 candidate and documentation. Commit, tag,
push, and publication are separate actions; publication requires explicit
authorization.
