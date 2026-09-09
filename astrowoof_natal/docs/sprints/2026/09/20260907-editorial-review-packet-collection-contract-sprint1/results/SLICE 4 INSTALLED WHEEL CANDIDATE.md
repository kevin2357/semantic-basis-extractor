# Slice 4 installed-wheel candidate

- Version: `0.4.54`
- Artifact source commit: `979ac3f`
- `SOURCE_DATE_EPOCH`: `1788995617`
- Wheel size: `1,377,672` bytes
- Wheel SHA-256 (both clean builds):
  `6ade10180b56913fc1a90d88b76f2cd7b84685c026b8acee99a3300d920f9723`
- Full suite: 1,154 passed; 59 expected skips; zero failures
- Full-suite test inventory SHA-256:
  `3042c86a7b9637a99f6c827be0b89e3f8be5c385d677578d664d34b492aa0f62`
- Full-suite outcome inventory SHA-256:
  `b9a645a3f1e92def9ebc21c83178691a2e19222d280e2e65a443096a16507a3f`
- Installed public qualification: 35 passed; zero skips; zero failures
- Repeated public qualification receipt SHA-256:
  `3c0d46fac5a13ddc5b4ea51722ac1626a83c9f0b5898f38a93cc5e9564dec50a`
- Installed version/import: `0.4.54`, resolved from isolated site-packages
- Dependency check: clean
- Provider/R2/Better Stack/API/database/retained-QA activity: zero

The initially built wheel from `0699538` is superseded. Its installed reader
correctly revealed that raw schema-resource hashes were line-ending-sensitive;
the candidate above includes the narrowly tested normalization correction.

The full-suite coordinator completed every worker successfully but could not
write its aggregate receipt to the requested `C:\tmp` destination. The intact
worker results were deterministically recomposed into
`full-suite-post-wheel-fix-recovered-receipt.json`, which explicitly records
that provenance exception.
