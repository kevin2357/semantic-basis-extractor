#!/usr/bin/env python3
"""Compatibility wrapper for the packaged projected-registry merger."""

from astrowoof_natal_authoring.registries import *  # noqa: F401,F403
from astrowoof_natal_authoring.registries import main


if __name__ == "__main__":
    main()

