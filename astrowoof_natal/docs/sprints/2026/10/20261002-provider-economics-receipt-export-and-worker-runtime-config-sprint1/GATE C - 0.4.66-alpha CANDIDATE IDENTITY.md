# Gate C — 0.4.66-α candidate identity

**Status:** candidate source identity frozen for provider-free joined replay only.

The human-facing candidate label is **0.4.66-α**.  Its PEP 440 distribution
version is **`0.4.66a0`**; the literal hyphen/Greek-alpha spelling is not a
valid Python wheel version.

The profile-owned SBE package descriptor is therefore updated with the same
candidate version.  This deliberately changes the canonical profile identity:

| Identity | Value |
| --- | --- |
| SBE candidate distribution | `astrowoof-natal-authoring==0.4.66a0` |
| SBE worker descriptor SHA-256 | `f9bafdb2ecd1491efa2ad492f2d687ce2409b0cdaa9aa77cf1f27eb9d9338b80` |
| Processing profile SHA-256 | `daf7cbacca620f578fcba9928e84e042904449176f65cf9808ccd9a1292d2212` |
| Profile catalog SHA-256 | `94d98557afe262672fde96b8e2f466f01e6c6f614d4cc0d2564b53d7f836c05e` |

API must use this replacement profile digest only in the bounded Gate C replay
fixture.  It does not authorize profile activation, worker deployment, tagging,
publication, or provider-backed QA.  The exact retained wheel SHA-256 and size
will be added after two committed-source builds agree.
