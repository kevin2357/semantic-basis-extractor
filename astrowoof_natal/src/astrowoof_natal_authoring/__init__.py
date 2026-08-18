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

__all__ = [
    "ProviderReconciliationAdapters",
    "__version__",
    "reconcile_authoring_provider_cycle",
]
