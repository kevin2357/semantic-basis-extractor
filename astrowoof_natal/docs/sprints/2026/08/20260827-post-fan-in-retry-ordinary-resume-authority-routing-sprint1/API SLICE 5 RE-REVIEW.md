# API Slice 5 Re-Review — Post-4A Replacement Candidate

Status: approved as the exact SBE input to API's joined provider-free campaign.

The repeated installed qualification correctly supersedes the earlier candidate.
Its evidence is coherent and complete for this gate:

- corrected source: `9205235`;
- unpublished version label: `0.4.27`;
- exact wheel SHA-256:
  `db5ff09afce53b063dea1b29d8fcb94af581bcf383f7cab5da1d65cc0d4e48ed`;
- exact SPC dependency: `semantic-projection-core==0.11.1`;
- installed receipt SHA-256:
  `982f8e3044c7e20a9324d44c61867af5e1787d2d996289ad7fe57aff19e6f2b9`;
- installed projection-bundle SHA-256:
  `75247d8652698e122c46fc79480bbf5b73fd0671b8cb38cb6aa5671eaab2a8a4`.

The installed receipt/bundle join, adversarial qualification, and generic release
smoke all passed with zero external provider/network calls, spend, or retained-QA
access. The new wheel—not a version-only lookup—must be pinned by API.

No release/tag/publication/deployment follows from this approval. SBE is now at
the planned API/Linux joined-campaign gate. API should implement and execute that
campaign first; SBE's final release decision follows only after its evidence is
accepted.

