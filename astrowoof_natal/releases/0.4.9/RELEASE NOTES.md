# AstroWoof Natal Authoring 0.4.9 Release

Status: qualified immutable artifact; publication authorized

## Summary

SBE 0.4.9 adds a supported installed-wheel, provider-free four-route deployment
qualification command:

```console
astrowoof-deployed-qa
```

The command exercises exact interactive, exact Batch, bounded interactive, and
bounded Batch from installed SBE code. Interactive cells use the production
initial-wave coordinator for six concurrent scripted creates, serialized durable
outcomes, detach, and fresh-reader fan-in. Batch cells use the production exact
Batch authoring path and production bounded Batch authoring cycle, each proving one
scripted Batch operation/authority with six ordered logical members and durable
native round reconstruction.

It also proves bounded final-QA review precedence and native duplicate-claim
refusal before provider work.

The command accepts no provider credentials, network endpoint, spend authority,
production input, or retained run workspace. Its closed receipt explicitly states
that it is qualification-only and carries no production authority.

## Public additions

- `run_deployed_qa_qualification()`;
- `validate_deployed_qa_receipt()`;
- `read_deployed_qa_schema()`;
- `astrowoof-deployed-qa`; and
- `astrowoof.deployed_qa_four_route_qualification.v1`.

The AstroWoof API consumer approved the V2 native Batch mechanism coverage and
recommended the fresh immutable 0.4.9 release.

The final wheel is 836,513 bytes with SHA-256
`3b900cc3216dd07e164af1a18a4a607c17e3fa1190711893808ba6527042f83d`.
Two fixed-epoch builds were byte-identical. Full source, installed Windows, and
network-isolated Linux gates passed without external provider calls or paid spend.
Post-publication verification will be recorded in `release-manifest.json` without
moving the immutable tag.
