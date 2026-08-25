"""AstroWoof natal semantic-basis extraction and authoring runtime."""

from importlib.metadata import PackageNotFoundError, version
import logging


# Library consumers should not receive surprise stderr output merely by importing
# SBE.  Command entry points install the operational handler explicitly.
logging.getLogger(__name__).addHandler(logging.NullHandler())

try:
    __version__ = version("astrowoof-natal-authoring")
except PackageNotFoundError:
    __version__ = "0.4.0.dev0"

from .reconciliation import (  # noqa: E402
    ProviderReconciliationAdapters,
    reconcile_authoring_provider_cycle,
)
from .native_transitions import (  # noqa: E402
    NativeTransitionResultView,
    latest_native_transition_result,
    read_native_transition_result,
    validate_transition_journal,
)
from .route_parity import (  # noqa: E402
    read_bounded_route_parity_traces,
    read_route_parity_oracle,
    validate_bounded_route_traces,
    validate_route_parity_oracle,
)
from .initial_wave import (  # noqa: E402
    InitialWaveError,
    build_initial_wave_binding_bundle,
    build_wave_authorization,
    preflight_wave_authorization,
    validate_initial_wave,
    validate_initial_wave_binding_bundle,
    validate_initial_wave_binding_bundle_against_wave,
    validate_initial_wave_result,
    validate_wave_authorization_document,
)
from .initial_wave_contract import (  # noqa: E402
    build_initial_wave_authority_inputs,
    read_initial_wave_authority_inputs,
    read_initial_wave_fixture,
    read_initial_wave_schema,
    validate_initial_wave_fixture,
    validate_initial_wave_authority_inputs,
)
from .deployed_qa import (  # noqa: E402
    read_deployed_qa_schema,
    run_deployed_qa_qualification,
    validate_deployed_qa_receipt,
)
from .response_diagnostics import (  # noqa: E402
    inspect_response,
    read_response_retrieval_diagnostic_schema,
    validate_response_retrieval_diagnostic,
)
from .lifecycle_contracts import (  # noqa: E402
    validate_lifecycle_inspection_v04,
    validate_lifecycle_inspection_v05,
)
from .temporal_lifecycle import (  # noqa: E402
    build_external_authority_request_v2,
    build_lifecycle_inspection_v06,
    canonical_utc_instant,
    inspect_temporal_lifecycle,
    read_temporal_external_authority_schema,
    read_temporal_lifecycle_schema,
    temporal_transition_errors,
    validate_external_authority_request_v2,
    validate_external_authority_request_v2_against_inspection,
    validate_lifecycle_inspection_v06,
    validate_temporal_transition,
)
from .pending_lifecycle_qa import (  # noqa: E402
    run_provider_pending_lifecycle_qualification,
)
from .external_authority import (  # noqa: E402
    build_external_authority_refusal,
    build_external_authority_request,
    read_external_authority_request,
    read_external_authority_schema,
    validate_external_authority_grant,
    validate_external_authority_refusal,
    validate_external_authority_request,
)
from .external_authority_qa import (  # noqa: E402
    read_external_authority_qualification_schema,
    run_external_authority_qualification,
    validate_external_authority_qualification_receipt,
)
from .operator_retirement import (  # noqa: E402
    assess_operator_retirement,
    build_operator_retirement_request,
    execute_operator_retirement,
    read_operator_retirement_schema,
    validate_operator_retirement_assessment,
    validate_operator_retirement_request,
    validate_operator_retirement_result,
)
from .operator_retirement_qa import (  # noqa: E402
    read_operator_retirement_qualification_schema,
    run_operator_retirement_qualification,
    validate_operator_retirement_qualification,
)
from .provider_economics import (  # noqa: E402
    MAX_RETRIEVAL_REFERENCES,
    PROVIDER_ECONOMICS_FIXTURE_NAMES,
    SCHEMA_VERSION as PROVIDER_ECONOMICS_SCHEMA_VERSION,
    derive_cohort_identity_sha256,
    derive_revision_id,
    derive_transaction_id,
    finalize_provider_economics_revision,
    project_exact_provider_economics_revision,
    read_provider_economics_schema,
    read_provider_economics_fixture,
    read_provider_economics_mutation_corpus,
    validate_provider_economics_revision,
    validate_provider_economics_revision_sequence,
)

__all__ = [
    "NativeTransitionResultView",
    "ProviderReconciliationAdapters",
    "InitialWaveError",
    "__version__",
    "latest_native_transition_result",
    "build_initial_wave_authority_inputs",
    "build_initial_wave_binding_bundle",
    "build_wave_authorization",
    "preflight_wave_authorization",
    "read_initial_wave_fixture",
    "read_initial_wave_authority_inputs",
    "read_initial_wave_schema",
    "read_native_transition_result",
    "read_bounded_route_parity_traces",
    "read_route_parity_oracle",
    "read_deployed_qa_schema",
    "run_deployed_qa_qualification",
    "inspect_response",
    "read_response_retrieval_diagnostic_schema",
    "reconcile_authoring_provider_cycle",
    "validate_bounded_route_traces",
    "validate_initial_wave",
    "validate_initial_wave_authority_inputs",
    "validate_initial_wave_binding_bundle",
    "validate_initial_wave_binding_bundle_against_wave",
    "validate_initial_wave_fixture",
    "validate_initial_wave_result",
    "validate_wave_authorization_document",
    "validate_route_parity_oracle",
    "validate_deployed_qa_receipt",
    "validate_response_retrieval_diagnostic",
    "validate_transition_journal",
    "validate_lifecycle_inspection_v04",
    "validate_lifecycle_inspection_v05",
    "build_lifecycle_inspection_v06",
    "build_external_authority_request_v2",
    "canonical_utc_instant",
    "inspect_temporal_lifecycle",
    "read_temporal_external_authority_schema",
    "read_temporal_lifecycle_schema",
    "temporal_transition_errors",
    "validate_lifecycle_inspection_v06",
    "validate_external_authority_request_v2",
    "validate_external_authority_request_v2_against_inspection",
    "validate_temporal_transition",
    "run_provider_pending_lifecycle_qualification",
    "build_external_authority_request",
    "build_external_authority_refusal",
    "read_external_authority_request",
    "read_external_authority_schema",
    "validate_external_authority_grant",
    "validate_external_authority_refusal",
    "validate_external_authority_request",
    "read_external_authority_qualification_schema",
    "run_external_authority_qualification",
    "validate_external_authority_qualification_receipt",
    "assess_operator_retirement",
    "build_operator_retirement_request",
    "execute_operator_retirement",
    "read_operator_retirement_schema",
    "validate_operator_retirement_assessment",
    "validate_operator_retirement_request",
    "validate_operator_retirement_result",
    "read_operator_retirement_qualification_schema",
    "run_operator_retirement_qualification",
    "validate_operator_retirement_qualification",
    "MAX_RETRIEVAL_REFERENCES",
    "PROVIDER_ECONOMICS_FIXTURE_NAMES",
    "PROVIDER_ECONOMICS_SCHEMA_VERSION",
    "derive_cohort_identity_sha256",
    "derive_revision_id",
    "derive_transaction_id",
    "finalize_provider_economics_revision",
    "project_exact_provider_economics_revision",
    "read_provider_economics_schema",
    "read_provider_economics_fixture",
    "read_provider_economics_mutation_corpus",
    "validate_provider_economics_revision",
    "validate_provider_economics_revision_sequence",
]
