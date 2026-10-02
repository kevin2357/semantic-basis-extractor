# API Agent Gate C review — alpha replay

**Decision:** SBE alpha boundary and the corresponding deterministic-image
execution seam pass their bounded provider-free replays. The remaining Gate C
work is the separate economics/provenance receipt evidence.

On 2026-10-02, API independently verified the retained
`astrowoof_natal_authoring-0.4.66a0-py3-none-any.whl` identity and loaded it
only from an isolated temporary site-packages directory.  It did not deploy,
publish, tag, activate a profile, invoke a provider, or contact a worker.

The candidate reported the recorded catalog/profile/SBE-descriptor digests:

- catalog: `94d98557afe262672fde96b8e2f466f01e6c6f614d4cc0d2564b53d7f836c05e`
- profile: `daf7cbacca620f578fcba9928e84e042904449176f65cf9808ccd9a1292d2212`
- SBE descriptor: `f9bafdb2ecd1491efa2ad492f2d687ce2409b0cdaa9aa77cf1f27eb9d9338b80`

API's test-only fixture substituted that exact candidate reference into the
otherwise closed registry, constructed a real natal generation manifest and
canonical manifest digest, and derived the production API four-field SBE
handoff.  A separate child process using the installed alpha wheel accepted
the exact handoff through `resolve_sbe_authoring_binding`.  It returned the
same profile, manifest, and SBE worker descriptor identities.  Changing only
the profile digest caused pre-provider refusal:
`processing profile digest does not match installed profile`.

In response to SBE's additional Gate C cell, API extended the same opt-in test
to invoke the retained `astrowoof-semantic-closure.exe` entrypoint itself with
the API-produced arguments. A provider-free prompt-layout create persisted the
full installed binding; exact resume retained it; altered digest and incomplete
four-field invocations both refused before workspace creation or provider work.
Prompt-layout reports were intentionally kept outside the sealed run workspace;
the CLI correctly refuses a changed workspace on resume.

The relevant API test is `tests/test_gate_c_alpha_provider_free.py`; the
focused API profile/worker suite passed **42 tests**. Full details are in the
paired API artifact `GATE C - API AND SBE ALPHA REPLAY EVIDENCE.md`.

## Deterministic image completion

API implemented deterministic source-level consumption and ingress fencing:
profile-aware work now resolves the installed profile before calculation,
validates the deterministic descriptor and deployment identity, returns a safe
attestation, and is rejected by API ingress if it does not match the persisted
manifest. Provider-free tests cover accepted binding and digest/deployment
identity refusal.

API then built a separately named, local-only deterministic Gate C image using
the retained alpha wheel as an explicit named build context. The recipe
verifies the exact wheel SHA, qualifies the SBE catalog/profile values in its
runtime lock, and performs root plus non-root runtime qualification. Its real
installed `astrowoof-deterministic-runtime` executable accepted an API-built
canonical invocation and returned the expected safe profile attestation. A
wrong profile digest and wrong deployed worker identity each refused before
AGF execution; API accepted the exact returned attestation and rejected an
incompatible one. Nothing was pushed, deployed, or activated.

That resolves the profile runtime-execution seam. The remaining Gate C
evidence is economics/provenance receipts, not an SBE or deterministic profile
compatibility blocker.
