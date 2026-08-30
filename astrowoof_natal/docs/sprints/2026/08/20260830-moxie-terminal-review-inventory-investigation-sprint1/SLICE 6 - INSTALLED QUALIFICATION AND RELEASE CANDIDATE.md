# Slice 6 — installed qualification and release candidate

## Candidate identity

- Version: `0.4.33`
- Wheel: `astrowoof_natal_authoring-0.4.33-py3-none-any.whl`
- Size: `1,119,466` bytes
- SHA-256: `2559ba0e6edd07c27641d11933928457aae8e4a082c1158a74ca0c523cfd7313`
- Upstream dependency: `semantic-projection-core==0.11.1`
- Controlled build epoch: `1788134400`
- Two final builds: byte-identical

The version was changed from released `0.4.32` to fresh `0.4.33` before the
candidate builds or full release suite began.

## Installed-wheel qualification

The final wheel replaced SBE in the existing dependency-complete isolated
qualification environment. `pip check` passed, import resolved from
`site-packages`, and the runtime reported `0.4.33`.

The following provider-free installed commands passed against the final wheel:

- `astrowoof-release-smoke --require-installed`;
- `astrowoof-external-authority-v2-qa`;
- `astrowoof-adversarial-qa`;
- `astrowoof-post-fan-in-retry-qa`; and
- `astrowoof-terminal-review-qa`.

Receipt SHA-256 values:

| Receipt | SHA-256 |
|---|---|
| generic installed smoke | `c6ccdc11603f8d787063a370331ccf31ca33ba4806f9f9103eb5bb7ab7d1b41d` |
| external-authority v2 | `7649a9d5a583098750da1bcf4e56e55b1034f59b17ad0ee69f2f24754ff351e7` |
| adversarial lifecycle | `3522a90e312e81c12ade0c10e2413520e625ccd7c75c5b54ffc609d083e2445d` |
| post-fan-in retry | `0a3eaffb2346c0d91848d356999adaf6ce720af8c200f1ccc7ee01f33da9fdf1` |
| terminal review | `be2b645bb2f9c194780fa5ebd8a923b789ab0ee58a9da1da3edc77b2d26a9104` |

The installed v2 CLI help surface contains `--events-stdout-jsonl`,
`--events-jsonl`, `--log-level`, and `--invocation-id`.

## Source-suite evidence

The first and only full-suite run executed 925 tests in 1,068.115 seconds:

- 924 cases were nonfailing;
- 48 were expected environment/opt-in skips; and
- one packaged terminal-review qualification fixture failed because it still
  bound historical `sbe_release=0.4.31` and its corresponding derived receipt
  digest.

This was a candidate-version fixture mismatch, not a runtime behavior failure.
The fixture was updated to `0.4.33` with the qualification's recomputed receipt
digest. The directly affected terminal-review, v2 CLI, and Moxie suites then
passed: 17 tests, one expected optional-schema skip.

Per explicit owner direction, the approximately eighteen-minute full suite was
not repeated. This record therefore does not claim a wholly green final full
suite. It claims one completed broad run with one identified version-derived
fixture mismatch, followed by a passing focused correction and passing final
installed-wheel qualifications.

## Safety and scope

- Provider POST/GET, network access, and spend: zero.
- Retained Moxie/R2 access or mutation during implementation/qualification:
  zero.
- API database/job/lease/capacity mutation: zero.
- Public lifecycle, authority, custody, and command-result schemas: unchanged.
- Runtime changes: exact-interactive completed-provider adoption ordering and
  v2 public-command diagnostic emission only.
- API still owns stderr/event relay, retention, and operator presentation.
- Retained-run recovery and deployment remain separately authorized consumer
  work.

## Release gate

The candidate is technically ready for final API/owner review. Commit, tag,
publication, and post-publication verification require separate explicit owner
approval.
