# API handoff — 0.4.57 canonical fixture digests

## Review request

Review and, if accepted, update API's frozen `_CASE_SPECS` digest values for the
six fixtures whose prior identities described accidental Windows CRLF checkout
bytes. Owners, evidence kinds, references, assertions, case order, and parsed
JSON values are unchanged.

| Case | 0.4.56/old SHA-256 | 0.4.57 canonical-LF SHA-256 |
| --- | --- | --- |
| `authority_ordinary_action` | `a92602b002867019d723f6b05f43b2936477d240b503400a86ae7268d877ccbb` | `397fc28f6c21be20cae5bce5c52784512efe046334860a3e21702c691082e03d` |
| `operator_retirement` | `bfec2839007afefbf5ef136c795dd821661a48d493f9e404d3e169bfa4bc3cf1` | `95ab1e7191b6949919b70db8b16cdc1cf584e3721e17c03976a34a198606ef17` |
| `muffin_review_capacity` | `50fa354581bf5877e74085e6743b771135a722e8175eb16caf85c7ba15fc0041` | `c305efec456822ceccca3b70e00e004c81784f978b190d7defb80a4098618dc3` |
| `provider_not_due_wait` | `dfe0abfbc053f6d402350d70b1b3a605ec8d18ae7d466ac258bed8976b62f818` | `eacb13788a3f73cca741eafcde4a83f3e509e8c99e6a9115f949738553dfe7e5` |
| `malformed_contradictory_evidence` | `bd13fb2b1167ddf8535cfd21bfc9b5c65d5ac929103a497e642d127e0b7e2644` | `22831c4ad7ae8c2f040ea9f41a74777b65198257d9c61fa8fbabdef040a523a3` |
| `partial_batch_usage` | `314cd15611260ac064b8163c19c3f7a474ac9b267b18c96d1722b0acd713ccd6` | `4d99f85cc87a009af17dc2e5296174e2cbc780402377525def2cc961dd769f18` |

The other three packaged-fixture digests remain unchanged:

- `ambiguous_provider_submission`:
  `2e2d5de510f4141d30309b0a35082eda27a7fd3c0477f976c3eca351c5ad1395`;
- `providerless_denial_terminalization`:
  `66ebf2ea9b900d3868b3b2ff2a7987fdac90bb89a47a954aca9a11187e9d4230`;
  and
- `providerless_batch_denial`:
  `9af0051f54374cb6d92a99dbca17236263ae8fcc35dc767c2ae8295296079626`.

## Candidate coordinates

- source candidate commit: `9158e89`;
- version: `0.4.57`;
- pre-lock wheel size: 1,375,422 bytes;
- pre-lock wheel SHA-256:
  `957f677d46ad01a7a7243e79db611c14fb63763868056aae971d9d50642abc1c`;
- no tag or release exists; and
- immutable `0.4.56` was not modified.
