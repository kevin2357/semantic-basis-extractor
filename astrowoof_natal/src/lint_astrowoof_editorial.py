#!/usr/bin/env python3
"""Compatibility wrapper for the packaged whole-deck editorial linter."""

from astrowoof_natal_authoring.editorial_lint import *  # noqa: F401,F403
from astrowoof_natal_authoring.editorial_lint import main


if __name__ == "__main__":
    main()

