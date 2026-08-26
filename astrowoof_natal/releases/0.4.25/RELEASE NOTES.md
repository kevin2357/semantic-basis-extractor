# AstroWoof Natal Authoring 0.4.25

Status: published and independently digest-verified

SBE 0.4.25 closes the post-fan-in ordinary-resume proof gap. A native worker now
advertises concrete local work through lifecycle inspection v0.7 rather than
asking an API consumer to infer executability from a broad run status.

Every local operation is bound to the exact native checkpoint and also carries a
basis-independent semantic key. Consumption history is cumulative and append-only;
an operation cannot be renamed by republishing a snapshot, resurrected later, or
replayed after it has already been consumed.

The provider-free `astrowoof-provider-pending-qa-v2` command preserves the honest
v1 six-create/4+2 proof and adds fresh-process exact/bounded post-fan-in proof through
retry-2 external authority. The qualification command is not production authority.

## Qualification

- Artifact source commit: `c8641c3a16e944e1e0d1392db8167901c4224ce2`.
- Fixed build epoch: `1787709856`.
- Full source suite: 755 passed; 38 expected environment/opt-in skips.
- Two byte-identical wheels; SHA-256
  `ba08d58390392a9fa2fe5748b26b04122082f821f7898bf33d70eada0cbe98f5`.
- Generic installed release smoke: pass with 50 cards and four summaries.
- Installed provider-pending lifecycle v2 qualification: pass; receipt SHA-256
  `6d87f86da8545c22e48e2a7ab2f7415e78efc6ee53f9379e6d7cdbcba15154b9`.
- Exact installed dependency: `semantic-projection-core==0.11.1`.
- External provider/network calls and spend: 0.
- Retained QA cohort access/mutation: 0.

The immutable tag is `astrowoof-natal-authoring-v0.4.25`. GitHub reports the
published 1,003,058-byte wheel with SHA-256
`ba08d58390392a9fa2fe5748b26b04122082f821f7898bf33d70eada0cbe98f5`;
an independent post-publication download reproduced that digest exactly.
