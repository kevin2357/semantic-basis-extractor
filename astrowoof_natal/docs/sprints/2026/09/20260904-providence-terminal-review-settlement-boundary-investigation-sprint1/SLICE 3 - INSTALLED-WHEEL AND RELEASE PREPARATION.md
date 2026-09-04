# Slice 3 — installed-wheel and release preparation

## Decision

Use the maintainer playbook's focused patch gate for candidate `0.4.48`.
The released behavior is an additive provider-free qualification surface:
module, strict Python validators, v1/v2 schemas, packaged fixture, public
exports, and one CLI. It does not alter lifecycle selection, state mutation,
provider custody, denial execution, terminal publication, or API disposition.

## Required installed proof

The exact candidate wheel must prove from a working directory outside the
checkout:

- installed version `0.4.48` and SPC `0.11.1`;
- clean `pip check` and imports resolving from `site-packages`;
- v1 semantic qualification and v2 identity-rich qualification;
- strict v1/v2 schema readers and Python validators;
- packaged fixture equality with the installed v1 runner;
- exact eight-action topology and singleton providerless-denial inventory;
- immutable precursor, one applied denial, inert exact replay, refused changed
  replay, and contiguous final-custody successor;
- zero provider create, retrieval, and transport activity; and
- wheel inventory containing exactly the new expected module, two schemas,
  fixture, and CLI metadata without private or generated source material.

## Release boundary

Two builds from the committed artifact source and then the release-lock commit
must be byte-identical under one recorded `SOURCE_DATE_EPOCH`. The exact final
wheel SHA and installed receipt will be submitted at Voof-paws 4. Tagging,
publication, deployment, and live Providence settlement remain outside this
slice until explicit owner authorization.
