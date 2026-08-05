#!/usr/bin/env python3
"""Compatibility wrapper for the packaged final-deck validator."""

from astrowoof_natal_authoring.validation import *  # noqa: F401,F403
from astrowoof_natal_authoring.validation import main


if __name__ == "__main__":
    main()

