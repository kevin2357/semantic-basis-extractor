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
    read_native_transition_result,
    validate_transition_journal,
)

__all__ = [
    "ProviderReconciliationAdapters",
    "__version__",
    "read_native_transition_result",
    "reconcile_authoring_provider_cycle",
    "validate_transition_journal",
]
