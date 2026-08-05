#!/usr/bin/env python3
"""Compatibility wrapper for the packaged Semantic Closure CLI."""

from astrowoof_natal_authoring.closure import *  # noqa: F401,F403
from astrowoof_natal_authoring.closure import main


if __name__ == "__main__":
    main()

