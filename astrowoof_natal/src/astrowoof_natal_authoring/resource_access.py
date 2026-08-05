"""Access package-owned authoring, schema, reference, and fixture assets."""

from __future__ import annotations

import shutil
from importlib import import_module
from importlib.resources import files
from pathlib import Path


RESOURCE_PACKAGE = "astrowoof_natal_authoring"


def resource(relative_path: str):
    """Return the traversable for one package resource."""
    return files(RESOURCE_PACKAGE).joinpath("resources", relative_path)


def read_resource_text(relative_path: str) -> str:
    return resource(relative_path).read_text(encoding="utf-8")


def read_resource_bytes(relative_path: str) -> bytes:
    return resource(relative_path).read_bytes()


def copy_resource(relative_path: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(read_resource_bytes(relative_path))


def module_source_path(module_name: str) -> Path:
    """Resolve an installed package module's shipped Python source."""
    module = import_module(module_name)
    source = getattr(module, "__file__", None)
    if not source:
        raise RuntimeError(f"Module has no filesystem source: {module_name}")
    path = Path(source)
    if path.suffix != ".py" or not path.is_file():
        raise RuntimeError(f"Module source is unavailable: {module_name} -> {path}")
    return path


def copy_module_source(module_name: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(module_source_path(module_name), target)
