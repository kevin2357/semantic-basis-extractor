# API Consumer Handoff — SBE 0.4.24

The detailed recovery contract and operator sequence are frozen in:

- `docs/sprints/2026/08/20260825-external-authority-v2-payload-digest-recovery-sprint2/PAYLOAD RECOVERY API HANDOFF.md`

API must:

1. pin and attest the exact 0.4.24 wheel;
2. restore the complete retained workspace at its stable logical path;
3. obtain a fresh v0.6 inspection and v2 request;
4. make and persist a fresh API authority decision and exact v2 grant;
5. invoke only `astrowoof-external-authority-v2`; and
6. ingest the sealed native result before changing API custody or reservations.

Never reuse the refused 0.4.23 grant. Never infer request bytes from redacted files,
logs, or API state. The `astrowoof-payload-recovery-qa` receipt is qualification
evidence only, not execution or release authority.
