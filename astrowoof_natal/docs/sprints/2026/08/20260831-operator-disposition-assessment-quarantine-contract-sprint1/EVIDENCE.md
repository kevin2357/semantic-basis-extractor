# Evidence

## Slice 0 source inventory

Reviewed public implementation boundaries:

- `lifecycle.py`: `inspect_lifecycle`, observation, action inventory, custody,
  capacity, branch, and external-authority projection.
- `lifecycle_contracts.py`: strict v0.5 validation and provider-custody /
  authority precedence predicates.
- `temporal_lifecycle.py`: v0.6 immutable basis / temporal decision split.
- `post_fan_in_contracts.py`: v0.7 concrete local-work inventory and cumulative
  consumption semantics.
- `retry_lineage_contracts.py`: v0.8 exact lineage-to-action/custody joins.
- `native_transition_availability.py`: bounded snapshot-valid result discovery
  explicitly documented as non-authoritative.
- `native_transitions.py`: exact result, receipt, retained snapshot, checkpoint
  basis, and journal validation.
- `terminal_review_contracts.py`: v0.2 terminal-review result/receipt and API
  immutable-action join.
- `operator_retirement.py`: existing strict provider-free dry-run assessment
  precedent.

## Findings

1. Existing public evidence is sufficient for a read-only assessment.
2. Existing status and result-index labels are not sufficient for terminal
   classification; the exact reader is required.
3. v0.7 is the minimum safe source for positive local-work claims.
4. v0.8 is the minimum safe source for retry-lineage conflict classification.
5. Existing logical-root fields can expose restored absolute paths; the new
   public assessment needs an opaque logical-root identity.
6. The original custody vocabulary needed one additive class for concrete local
   work.

## Safety evidence

- Provider calls: 0.
- Provider retrievals: 0.
- Retained QA/R2 access: 0.
- Workspace mutations: 0.
- Runtime/source/schema changes: 0.
- Version/tag/release changes: 0.

Slice 0 is documentation and source analysis only. No tests were required or
run because no executable artifact changed.

## Slice 1 focused evidence

Command (with bundled Python and source path):

```text
python -m unittest discover -s astrowoof_natal/tests -p test_operator_disposition_contract_slice1.py
```

Result:

```text
Ran 12 tests
OK (skipped=1)
```

The skip is only the optional Draft 2020-12 `jsonschema` mirror check; all
strict Python semantic validation runs and passes without that dependency.

Runtime/provider evidence remains unchanged:

- External provider calls/retrievals: 0.
- Retained QA/R2 access: 0.
- Workspace mutations: 0.
- Lifecycle/reconciliation/provider behavior changes: 0.
- Deployment/version/tag/release changes: 0.

## Slices 2–3 focused evidence

```text
python -m unittest discover -s astrowoof_natal/tests -p test_operator_disposition_*slice*.py
Ran 21 tests
OK (skipped=1)

python -m unittest \
  astrowoof_natal.tests.test_lifecycle_contracts \
  astrowoof_natal.tests.test_retry_lineage_contract_slice3
Ran 31 tests
OK
```

The 21-test matrix includes the strict contract, real reader, exact terminal
join, all four route/mechanism provider-custody cells, mixed precedence, and
legacy unsupported evidence. No provider adapter was installed or invoked.

## Voof-paws 3 correction evidence

```text
python -m unittest \
  astrowoof_natal.tests.test_operator_disposition_reader_slice2 \
  astrowoof_natal.tests.test_operator_disposition_cross_route_slice3 \
  astrowoof_natal.tests.test_operator_disposition_contract_slice1
Ran 22 tests
OK (skipped=1)
```

The added test patches the public availability-reader dependency and proves a
default assessment calls it zero times. Availability recovery remains possible
only when `allow_availability_recovery=True` is passed explicitly.

## Slice 4 source packaging evidence

```text
python -m unittest \
  astrowoof_natal.tests.test_operator_disposition_packaging_slice4 \
  astrowoof_natal.tests.test_operator_disposition_reader_slice2 \
  astrowoof_natal.tests.test_operator_disposition_cross_route_slice3 \
  astrowoof_natal.tests.test_operator_disposition_contract_slice1
Ran 26 tests
OK (skipped=1)
```

The source qualification ran the public CLI in two fresh subprocesses. Provider
calls, retrievals, external network calls, and spend were all zero. No retained
QA/R2 workspace was accessed.

## Installed-wheel and lean candidate evidence

Candidate:

```text
astrowoof-natal-authoring 0.4.37
wheel sha256: 032a2ab0d9367e4dad68c1a9814b75bbf7e108a00fde44c2fdc1602875ec0a7c
controlled build A == controlled build B
SPC compatibility: 0.11.1
pip check: No broken requirements found.
```

Installed qualification:

```text
schema_version: astrowoof.operator_disposition_qualification.v1
status: pass
receipt_sha256: 09294f61c5582ef207960048f0b50c5b1a4d3f9b79a97f508fd9e8198074c94f
fixture_bundle_sha256: f7d0a63fa034909506af28f6e5afb4142e18d51541799fbab7affbf1bcd11cb1
external_network_call_count: 0
provider_create_count: 0
provider_retrieval_count: 0
provider_spend_usd: 0
```

Affected lean regression matrix:

```text
Ran 84 tests
OK (skipped=5)
```

The five skips are optional JSON Schema mirror checks in the lean source
interpreter; strict Python validators ran in all cases. The final installed
environment includes JSON Schema support and passed `pip check`. The full
runtime suite was deliberately not run because this patch changes only a
read-only default, public projection packaging, CLI, fixtures, and qualification
surface—not lifecycle mutation, reconciliation, scheduling, or provider logic.

## Publication verification

- Release: `astrowoof-natal-authoring-v0.4.37`
- Release URL:
  `https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.4.37`
- Source commit: `bb94fe1c5b9f63e9dd2b60ca07d886dbcca2c5a5`
- Downloaded wheel SHA-256:
  `032a2ab0d9367e4dad68c1a9814b75bbf7e108a00fde44c2fdc1602875ec0a7c`
- Downloaded-wheel `pip check`: clean.
- Downloaded-wheel qualification: pass; receipt identity unchanged.
