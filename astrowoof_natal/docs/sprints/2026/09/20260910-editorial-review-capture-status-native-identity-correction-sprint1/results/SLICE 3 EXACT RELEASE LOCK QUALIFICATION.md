# Slice 3 exact release-lock qualification

Status: passed; paused before tag and publication

| Evidence | Result |
| --- | --- |
| release-lock commit | `a43067f580c5d4b727333a0eb54422191f73fa77` |
| `SOURCE_DATE_EPOCH` | `1789031187` |
| broad/full suite | 1,161 tests; 60 expected skips; passed |
| test inventory SHA-256 | `888609c217425c0afc20f1ffef5feaf436cc3779def38c7c8aa1f065767d1740` |
| exact wheel filename | `astrowoof_natal_authoring-0.4.56-py3-none-any.whl` |
| exact wheel size | 1,379,722 bytes |
| exact wheel SHA-256 | `31a82e5121a3a43c62843f7ee39e8359ecd8485245e6b35f555892a41f4ed551` |
| wheel members | 307; identical inventories; no forbidden residue |
| installed boundary | version/import/public symbols passed from `site-packages` |
| installed focused tests | 27 passed, no skips |
| installed public QA | release smoke and editorial-review QA passed |
| API consumer | 4 functional cells plus independent `0.4.56` assertion passed |
| publication operations | none |

This documentation result is later than the immutable artifact-source lock.
The eventual component tag must point to `a43067f580c5d4b727333a0eb54422191f73fa77`,
not to the later documentation-only evidence commit.
