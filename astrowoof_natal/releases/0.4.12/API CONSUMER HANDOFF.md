# SBE 0.4.12 API Consumer Handoff

Replace the 0.4.11 wheel and hash in worker-image builds with the published 0.4.12
artifact. No API code, schema, profile, lifecycle, spend, or logging configuration
change is required.

The release gate executes the same installed command used by the API image:

```console
astrowoof-release-smoke --work-dir /tmp/sbe-smoke --require-installed
```
