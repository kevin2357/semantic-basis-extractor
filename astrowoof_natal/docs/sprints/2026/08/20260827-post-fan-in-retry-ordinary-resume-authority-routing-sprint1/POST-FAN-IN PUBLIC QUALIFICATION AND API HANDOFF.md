# Post-Fan-In Public Qualification and API Handoff

Status: Slice 4 SBE qualification implemented; API joined-campaign review pending.

## Supported installed surface

The installed wheel exposes:

```text
astrowoof-post-fan-in-retry-qa
astrowoof-post-fan-in-retry-qa --fixture
astrowoof-post-fan-in-retry-qa --schema
```

The matching Python readers are exported from `astrowoof_natal_authoring`:

- `read_post_fan_in_retry_fixture()`;
- `read_post_fan_in_retry_qualification_schema()`;
- `run_post_fan_in_retry_qualification()`; and
- `validate_post_fan_in_retry_qualification()`.

The fixture identity is the canonical SHA-256 of the closed packaged fixture. The
receipt binds that fixture digest, the installed package version, every public
phase-evidence digest, the final public lifecycle evidence, and the receipt itself.
Phase and endpoint identities hash closed semantic projections rather than complete
native inspection bytes. Ephemeral logical workspace roots, snapshot identities,
and qualification wall-clock instants are deliberately excluded; route, mechanism,
command, capacity, custody, action inventory, local-work semantics, outcome, and
replay facts remain bound. Two identical invocations under one package version must
produce an identical receipt.

## What the qualification proves

The provider-free command constructs a disposable exact-Natal interactive
workspace and executes this production-shaped sequence:

1. retained provider custody is observed as not due;
2. the not-due cycle performs zero retrieval and no mutation;
3. one due provider response is retrieved through native reconciliation;
4. lifecycle v0.7 advertises provider-result fan-in as local work;
5. the local operation changes native truth and its semantic operation key is
   durably consumed;
6. the successor exposes one ordinary external-authority v2 request;
7. an exact scripted grant/document set is committed with native intent;
8. one scripted provider create returns a durable identity;
9. exact replay performs no second create; and
10. the final SBE endpoint is explicit provider-pending custody.

The historical incident projection records that retained `DETACHED` initial-wave
lineage incorrectly captured this successor as initial-wave admission. The
corrected route treats `DETACHED` as lineage and follows current provider/local/
ordinary-authority facts.

## Privacy and authority boundary

The fixture and receipt expose no raw `run.json`, workspace path, prompt, provider
payload, provider response ID, private selector, credentials, or retained-QA data.
The local provider transport is scripted; external network calls and spend are
zero.

The command is qualification-only. It does not authorize provider work, mutate a
retained run, prove API persistence, or prove reader delivery.

## API joined campaign

The API companion should run this command against the exact installed candidate
wheel, validate the fixture and receipt, and then drive the public projections
through its real persistence, lifecycle translation, scheduler, lease, and
capacity services. With two runs and one slot it must prove that the waiting run
does not retain the slot, the competing eligible run progresses, provider/spend
authority is not released merely with capacity, and stale replay cannot duplicate
dispatch or publication.

The SBE receipt ends at `detached_provider_pending`. Any assertion that a reader
was persisted or delivered belongs to the API joined fixture.
