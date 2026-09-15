# Slice 0 — Concrete traversable caller matrix

## Decision

The sweep is narrower than the initial syntactic inventory suggested.

After the predecessor's live helper correction, ten variadic-looking source
calls remain: nine explicit multi-argument calls and one starred-component
call. Real Python 3.11 execution proves six are already compatible because
they operate on the regular top-level package's `pathlib` traversable. Four
operate on namespace-package `MultiplexedPath` values and fail reproducibly.

No source call was changed in this slice.

## Inventory correction

The predecessor inventory contained eleven total call shapes: ten explicit
multi-argument calls, including the now-corrected live helper, plus one starred
call. Therefore ten—not eleven—remain after that correction. Control Room #23
and earlier prose inherited the off-by-one wording; this runtime-backed matrix
is authoritative for implementation scope.

## Real-accessor matrix

The repository was mounted read-only into official Python 3.11.15 and 3.12.14
containers. `slice0_accessor_inventory_probe.py` exercised public or real
internal readers and independently hashed the selected packaged bytes.

| Call site | Role and callers | Python 3.11 | Python 3.12 | Disposition |
| --- | --- | --- | --- | --- |
| `editorial_review_fixtures.py:628` | Public packaged editorial fixtures; contract QA and qualification | `TypeError` for both v5 fixtures | Success | Correct in Slice 1; release blocker. |
| `external_authority_v2.py:276` | Public external-authority v2 fixture; contract tests | `TypeError` | Success | Correct in Slice 2 with real fixture coverage. |
| `provider_economics.py:570` | Public named economics fixture reader; contract tests | `TypeError` | Success | Correct in Slice 2 with closed-name/path tests. |
| `provider_economics.py:578` | Public economics mutation-corpus reader; contract tests | `TypeError` | Success | Correct in Slice 2 with corpus validation tests. |
| `resource_access.py:16` | High-reach internal accessor used by production extraction, bounded authoring/provider, lifecycle, authority, retirement, route parity, smoke, and QA | Success | Success | Do not change; concrete base is regular `astrowoof_natal_authoring`, yielding a compatible `pathlib` traversable. Add/retain representative Python 3.11 caller coverage. |
| `adversarial_consumer.py:64,65,70` | Public adversarial catalog and packaged evidence readers, including starred components | Success | Success | Do not change; all operate beneath the regular top-level package path. Existing catalog digest checks cover selected evidence. |
| `adversarial_trace.py:577,781` | Public adversarial schema/fixture readers and provider-free QA | Success | Success | Do not change; regular top-level package path is compatible. |

## Exact resource witnesses

| Reader | Bytes | SHA-256 |
| --- | ---: | --- |
| Generic contract catalog | 8,633 | `d739a509373949d54e8673e4c57a7041835df50d0eb914dd17674927cfc8f5f3` |
| Editorial accepted-delivery v5 | 86,092 | `54bdae8913e29277de99cd6c69fb1cb5bec2ccf176394cf1a6dc069803c8147e` |
| Editorial closeout v5 | 89,020 | `11b46b4dc8749eb56ec8ec99834e670f1e6272e11316e493866c4ffdad5bd303` |
| Adversarial consumer catalog | 4,401 | `7993dc9283d6a2c1a258981c7879acbf1247e47338ae3be84b503f0abcac73e8` |
| Adversarial trace schema | 11,039 | `8b45fb44b68e180e40e420139bd5e2112b72c09a0abbb2c753c05406c3f3ebda` |
| Adversarial trace fixture | 5,223 | `c305efec456822ceccca3b70e00e004c81784f978b190d7defb80a4098618dc3` |
| External-authority v2 fixture | 10,737 | `397fc28f6c21be20cae5bce5c52784512efe046334860a3e21702c691082e03d` |
| Providerless economics fixture | 3,907 | `5e3cfcad7ecad7726d4e9e19780fa38e01b59f15c04b913dabb1f106ebcdcf63` |
| Economics mutation corpus | 1,745 | `5149b0707452b84cf1161d12b6b0403b30d5ecd70d0c18495bfc8f8e0141303b` |

## Path-component semantics

- The four failing calls supply separate lexical components beneath namespace
  packages. Chaining those same components preserves their intended identity.
- The generic accessor deliberately accepts one relative path string that may
  contain `/`; its current second argument semantics must remain unchanged.
- The adversarial starred form deliberately expands a catalog-owned relative
  path under a regular package root. It works on Python 3.11 and is digest
  checked; rewriting it would add risk without compatibility benefit.

## Test boundary

- Slice 1: both real editorial v5 fixtures, unknown kind, missing resource,
  malformed content, and existing strict/digest validation.
- Slice 2: real external-authority fixture and real provider-economics fixture
  set/corpus, plus missing or rejected-name and malformed-content controls.
- Compatible controls: execute representative generic accessor and adversarial
  readers on Python 3.11 and 3.12 without changing their implementation.
- New test modules, if any, must enter `test_suite_manifest.json` immediately;
  extending existing manifested modules is preferred where cohesive.

## Gate A request

Approve corrections only for the four proven namespace-package failures.
Approve no-op dispositions for the six regular-package calls, subject to
two-runtime source-tree qualification. This avoids a needless rewrite of the
generic accessor and the already compatible starred form.

