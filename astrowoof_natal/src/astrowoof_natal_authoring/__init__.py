"""AstroWoof natal semantic-basis extraction and authoring runtime."""

from importlib.metadata import PackageNotFoundError, version

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
    "validate_transition_journal",
]
