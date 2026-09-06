# Release candidate — SBE 0.4.51

## Identity

- Version: `0.4.51`
- Artifact-source commit:
  `527a74c1289e8ace6909e780d662e69b346691a9`
- Build epoch: `1788712494`
- Wheel: `astrowoof_natal_authoring-0.4.51-py3-none-any.whl`
- Wheel bytes: `1,228,560`
- Wheel members: `269`
- Wheel SHA-256:
  `ba39020b6d7f37ab422c99766839067603127d104ea15cde44b7e53e10491b6d`
- Forbidden cache/bytecode/private members: `0`
- SPC compatibility: `0.11.1`

## Regression evidence

- Candidate version and the version-derived fixture were frozen before testing.
- Focused logging/contract/event/trace/reporter/version matrix: 60 passed, 3
  expected optional-schema skips in 16.109 seconds.
- Full repository suite under Windows Python 3.12.14: 1,076 passed, 56 expected
  skips in 1,095.939 seconds.
- No runtime, schema, validator, or test correction occurred after the full
  suite.

## Reproducibility

Two independent clean exports of the artifact-source commit were built with the
same epoch. Filenames, byte sizes, ordered member inventories, individual member
hashes, and complete wheel hashes match.

An intervening build accidentally targeted the live repository root. It was
different, immediately disqualified, and is not part of the candidate pair.

## Installed qualification

The exact candidate was installed from outside the source package into Windows
Python 3.12.14 with SPC 0.11.1.

- `pip check`: no broken requirements.
- Import path: isolated `site-packages`; version `0.4.51`.
- Packaged `sbe-worker-log.v1` schema and event catalog: present.
- Generic `astrowoof-release-smoke --require-installed`: pass; file SHA-256
  `3d3431ab99b9b8fdf058d246478cf7d4347c383d4e02839fd1e825e971d2e05c`.
- Trace observability: pass; qualification SHA-256
  `8246fd1b0fbe669b52ce16975c4fdfcb6819745729825ef3a6933a5cb9686460`.
- Run-report qualification: pass; receipt SHA-256
  `8174607eaf11516d830e14a2cef27e5754ff3cd8177b930dcbf8b3820481f78b`.
- Decision-evidence observability: pass; qualification SHA-256
  `46f7cd50711359360dbf25eadc801d4a6826d608fe18245ae03db33ae5fb4afe`.
- Providerless-denial qualification: pass; receipt SHA-256
  `a3f9d5fff8ff22eb738f60503d655a1e20f048cfc0a458236bf924b7011daf25`.

## Cross-repository relay evidence

The API provider-free route matrix passed 37 focused tests. Reconciliation
relays structured stderr verbatim; ordinary resume and constrained v2 inherit or
intentionally suppress diagnostics according to event-stream configuration.
Application logs remain unable to satisfy authoritative command-result parsing.
The API evidence is a test/docs-only working tree based on current `main`, not
an immutable API revision.

## Safety and scope

- Provider creates/retrievals, external network calls, R2 access, retained-QA
  access, and deployment changes: zero.
- Lifecycle, authority, custody, terminal-result, and API disposition contracts:
  unchanged.
- Structured records are diagnostic only.

## Remaining release-lock gate

Commit this record as the release lock, rebuild twice from that exact commit and
its commit epoch, require byte-identical wheels, repeat installed public
qualifications against the resulting artifact, and then pause for final review
and explicit owner authorization before tag/publication.
