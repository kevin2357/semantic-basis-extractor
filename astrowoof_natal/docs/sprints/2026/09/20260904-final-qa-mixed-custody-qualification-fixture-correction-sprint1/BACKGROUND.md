# Background — final-QA mixed-custody qualification fixture correction

API Sprint 76's provider-free SBE/API release-pair gate failed after the healthy
deployment of immutable SBE `0.4.46`. The exact published wheel was verified as:

- wheel: `astrowoof_natal_authoring-0.4.46-py3-none-any.whl`;
- SHA-256: `c6155ed71428865faa49eaeaf3442f5f64bb670e2317b1ec6dfd0bda54dcbb14`;
- API revision: `a52bb5bf2dfe410cfadfe3e218a70f02fb17b308`; and
- API manifest SHA-256:
  `9f4865420b8e01e820adc2da6e4e3dd2395f39c740d8250f1fa915ff8a87a406`.

The installed `astrowoof-final-qa-mixed-custody-qa` command failed while its
fixture called `build_external_authority_request_v2()`. The fixture had first
committed a native final-QA review conclusion and then tried to create a new
polish action/request. SBE `0.4.46` correctly applies terminal dominance at that
point, so the lifecycle checkpoint contains no external-authority request.

This is a qualification-fixture ordering defect, not evidence of a live worker,
provider, API-ingress, or terminal-dominance runtime defect. QA remains clean and
paid cohort admission remains blocked until a replacement immutable SBE wheel
passes the same API release-pair gate.

The release-process lesson is also explicit: the `0.4.46` focused matrix omitted
an already-packaged qualification that transitively exercised the changed
terminal/finalization selector. The full suite would have found the failure, but
a correctly selected affected qualification matrix should also have found it.
