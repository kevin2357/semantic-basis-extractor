# Slice 4 source regression gate

- Candidate version: `0.4.54`
- Gate: broad/full, preceded by affected focused verification
- Focused result: 41 tests passed; 3 expected optional-schema skips
- Final full result: 1,153 tests passed; 59 expected skips; zero failures
- Full-suite wall time: 895.754865 seconds
- Test inventory SHA-256:
  `44dacd2b85ca745aaddb65581abc05eb1087c0f128aa235dabb7c9260c1ec30f`
- Outcome inventory SHA-256: recorded in the private local machine receipt at
  `C:\tmp\editorial-review-0.4.54-full-suite-final-receipt.json`
- Side effects: zero provider, API, R2, Better Stack, database, or retained-QA
  operations

The earlier 1,151-test broad pass preceded addition of the required installed
public exports and qualification console entry point. It remains honest
superseded evidence and is not the final release-bound regression result.

The 1,153-test result likewise predates correction of an installed-wheel-only,
line-ending-sensitive schema digest failure. It is preserved as successful
source evidence but is superseded as the final release-bound regression result;
a fresh complete run is required after the correction.
