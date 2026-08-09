# AstroWoof Natal Authoring 0.2.1

This patch corrects the cross-platform installed release smoke discovered while
promoting the 0.2.0 wheel into the Linux API-worker image.

## Changed

- deterministic fake-provider values no longer depend on platform-sensitive
  workspace traversal order;
- fake uniqueness tokens remain distinct after the production editorial
  tokenizer's normalization;
- installed smoke now runs delivery and completed-run cleanup checks only after
  `DELIVERY_COMPLETE`; and
- a smoke run that stops in QA review returns structured failure evidence and
  reports cleanup as skipped instead of masking the original result with an
  uncaught cleanup exception.

There is no change to extraction, scoring, synthesis, production OpenAI routes,
spend enforcement, disclosure, snapshots, acceptance/lint rules, provenance,
delivery contracts, or API ownership. All 0.2.0 production qualification is
reused; this patch made no provider request and spent USD 0.

## Qualification

The complete deterministic suite passes (148 tests). Two 0.2.1 wheel builds are
byte-identical. The exact wheel clean-installs and passes installed-runtime
smoke on Windows and in the retained offline Python 3.11 Linux worker-image
shape. Both platforms reach `DELIVERY_COMPLETE` and produce the same 19-resource
aggregate digest:
`439c8771fe7944ddb1b5b83465b7d2f76f252340624f1b85c85f9278fba55404`.

Tagging and publication remain pending explicit authorization. After
publication, this paragraph will point to the post-publication evidence.
