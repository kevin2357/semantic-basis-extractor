# Plan — packaged fixture byte canonicalization

Status: complete. Corrective version `0.4.57` was qualified, approved, tagged at
the exact artifact-source commit, published, and verified after fresh download.

## Goal

Make every digest-bearing packaged adversarial fixture byte-identical across
source checkout, Git archive, wheel, and installed package by freezing JSON
resources to LF independently of host Git configuration.

## Focused patch gate

- inventory and canonicalize every packaged fixture referenced by the
  adversarial consumer catalog;
- regenerate all catalog digests from canonical LF bytes;
- prove source, Git-exported, wheel, and installed bytes agree;
- run all adversarial catalog/fixture readers and validators, package/release
  contracts, installed public QA, and the API failing vertical slice;
- build twice from the exact release-lock commit and require identical wheels;
  and
- escalate to the broad/full suite if any runtime semantics change or focused
  evidence reveals collateral behavior.

The published `0.4.56` tag and assets remain immutable. A corrected artifact
requires a fresh `0.4.57` release after review and owner authorization.
