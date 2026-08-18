# SBE 0.4.8 Compatibility

- Python: 3.11 or newer.
- Direct dependency: `semantic-projection-core==0.11.0`.
- Qualified SPC wheel SHA-256:
  `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d`.
- Qualified upstream AGF identity: 0.8.1, wheel SHA-256
  `860c48793318c82c986b32664cd0f3fe97c4b1e02fb1e489561bc395c8b5a3ed`.
- Installed qualification: CPython 3.12 Windows and CPython 3.11 Linux.

SBE 0.4.8 is additive over 0.4.7. Fresh interactive initial-wave workspaces
publish the joined authority inputs. Legacy workspaces lacking the binding bundle
fail closed for that public read operation and are not silently synthesized.

Batch route authority semantics are unchanged.
