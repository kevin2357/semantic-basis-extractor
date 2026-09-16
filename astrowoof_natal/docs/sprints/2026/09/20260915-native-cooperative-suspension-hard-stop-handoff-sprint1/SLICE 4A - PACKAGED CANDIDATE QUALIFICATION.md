# Slice 4A — Packaged Candidate Qualification

## Purpose

This slice breaks the release-pair dependency cycle. SBE first supplies one
exact installed candidate and a provider-free public receipt. API can then wire
that candidate into its real subprocess adapter in API Slice 3B. Joined API/SBE
behavior remains Slice 4B.

## Public qualification

`astrowoof-native-suspension-qa` uses a disposable exact-interactive
ordinary-v2 workspace and launches `astrowoof-external-authority-v2` as a real
child process. It validates only the exact output document and immutable public
artifacts; stderr text and mutable status names are not authority.

The closed receipt proves:

- exit 0 with an exact suspension command result;
- checkpointed suspension before provider create;
- exact result/receipt/output joins and inert replay;
- no ambiguous or newly created provider custody;
- unrelated-workspace refusal;
- installed contract-schema and fixture-bundle availability; and
- zero provider create/retrieve, spend, network, live process termination, and
  API resource release.

The package root exports the contract schema/fixture readers, document
validators, and qualification reader/validator for API Slice 3B.

## Source evidence

- Qualification module: 3 passed, 1 expected optional-schema skip.
- Suspension plus neighboring v2/reconciliation matrix: 115 passed, 3 expected
  optional skips.
- `compileall` and `git diff --check` are required before the candidate commit.

## Superseded installed candidate result

| Evidence | Exact value |
| --- | --- |
| Candidate source commit | `5f5d9aa6` |
| Candidate version | `0.4.65` |
| `SOURCE_DATE_EPOCH` | `1789531794` |
| Wheel size | `1,407,338` bytes |
| Wheel SHA-256 | `6c5db7b3134805f74343b841ea50ace128c313ab8ac292196fdf483fa6b1ce6b` |
| Pinned SPC | `0.11.1`, SHA-256 `dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612` |
| Qualification SHA-256 | `0282608bd9c0df8c3a4761b3f39a48df9bbdf9ead43c15cbe8cc3b4f16d134dd` |
| Qualification file SHA-256 | `24f4315b8251f8fb2a07cb64eb043e2afc6c1769dfe608f42c9cc7edc0a2e003` |

The clean Python environment installed the candidate from its wheel and
resolved `astrowoof_natal_authoring` from that venv's `site-packages`.
`pip check` reported no broken requirements. The installed public command and
schema command both exited successfully; the root public Python validator and
packaged JSON Schema independently accepted the receipt.

Every receipt check passed. Recorded counts were zero for provider create,
provider retrieve, external network, provider spend, live process termination,
and API resource release.

The first system-site qualification attempt correctly exposed a pre-existing
host-runtime dependency impurity (SPC installed without `jsonschema`). It was
not accepted as clean evidence. The final receipt above comes from a fresh venv
with the immutable SPC wheel and declared dependencies installed explicitly.

API Slice 3B rejected this candidate after discovering that the envelope
required an already-admitted operator force fence before `Popen`, while the
real API admits that fence only after an operator acts on a running lease. The
wheel remains useful evidence that the old bytes were reproducible and
installable, but it is not a valid integration or release candidate.

Slice 4A is reopened for a corrected candidate. The replacement contract uses
an immutable pre-launch supervision capability in the envelope, then a later
operator force fence in the request. Result, receipt, and command-result
artifacts bind both identities. The old `0.4.65` hash must never be substituted
for the corrected candidate.

## Corrected `0.4.66` candidate

Renewed Gate B2 approved the explicit capability → launch → fence → request
model before packaging. The executable schema, packaged fixture, runtime
publication, receipt, and command-result layers independently bind both the
pre-launch supervision capability and later immutable force fence.

| Evidence | Exact value |
| --- | --- |
| Candidate artifact-source commit | `24f2c674` |
| Candidate release-lock commit | `7e4fa13f` |
| Candidate version | `0.4.66` |
| `SOURCE_DATE_EPOCH` | `1789534964` |
| Wheel size | `1,406,483` bytes |
| Wheel SHA-256 | `ec30e79780b7a4ffc47510ec25f5b6cb3b09639a8b6a2ec6b2def0661f871daf` |
| Pinned SPC | `0.11.1`, SHA-256 `dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612` |
| Final lock-build qualification semantic SHA-256 | `e37f8a5c6ace407deb0ce37022dea2571312f56de5485d27af7e849bce76f71b` |
| Final lock-build qualification file SHA-256 | `cbba5107d75fd96ab229b2957494384bfc6fa333d7e825562a0c8d2a0393d76c` |
| Qualification schema file SHA-256 | `a47a7da72dbab7d8db2d3befa057404ac8d7e112755c55784129ee3497cb8096` |

Evidence:

- Expanded source contract/v2/reconciliation matrix: 84 passed, 4 expected
  optional skips.
- Two clean-source builds produced byte-identical filenames, sizes, member
  inventories, and wheel hashes.
- Two further builds from exact release-lock commit `7e4fa13f`, using the same
  recorded epoch, reproduced that exact wheel SHA-256 and size.
- Clean venv installation resolved version `0.4.66` and package imports from
  `site-packages`; `pip check` was clean.
- Installed public qualification and packaged JSON Schema validation passed
  again from the release-lock wheel. Qualification receipt identity changes
  per disposable execution timestamp; its closed semantics and zero-I/O safety
  assertions remained exact.
- All counters remained zero for provider create/retrieve, network, spend,
  live process termination, and API resource release.

This is a provider-free API candidate handoff, not tag, publication,
deployment, live process control, or joined Slice 4B authorization.
