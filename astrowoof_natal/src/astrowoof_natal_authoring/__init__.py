"""AstroWoof natal semantic-basis extraction and authoring runtime."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("astrowoof-natal-authoring")
except PackageNotFoundError:
    __version__ = "0.4.0.dev0"

__all__ = ["__version__"]
