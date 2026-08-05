#!/usr/bin/env python3
"""Compatibility wrapper for the packaged authoring-workspace assembler."""

from astrowoof_natal_authoring.assembly import *  # noqa: F401,F403
from astrowoof_natal_authoring.assembly import main


if __name__ == "__main__":
    main()

