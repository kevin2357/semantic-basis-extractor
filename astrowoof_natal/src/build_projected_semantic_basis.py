#!/usr/bin/env python3
"""Compatibility wrapper for the packaged semantic-basis extraction CLI."""

from astrowoof_natal_authoring.extractor import *  # noqa: F401,F403
from astrowoof_natal_authoring.extractor import main


if __name__ == "__main__":
    main()

