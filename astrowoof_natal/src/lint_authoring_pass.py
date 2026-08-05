#!/usr/bin/env python3
"""Compatibility wrapper for the packaged per-pass acceptance checker."""

from astrowoof_natal_authoring.pass_acceptance import *  # noqa: F401,F403
from astrowoof_natal_authoring.pass_acceptance import main


if __name__ == "__main__":
    main()

