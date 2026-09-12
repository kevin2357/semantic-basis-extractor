# Totally Unrelated Wild Tangent for Finding Brandi's Song

A small, auditable audio-search engine for finding **Careless Whisper** inside
opaque files and multi-hour DJ sets. It uses Shazam-style constellations of local
spectrogram peaks: pairs of peaks become compact hashes, and matching hashes vote
for a playback offset. A real match therefore produces both a score and the point
in the set where the song begins.

The base pass targets exact or sampled audio surviving transcoding, noise, and
level changes. The supplied variant generator adds ±3/6% tempo and ±1-semitone
pitch references for remix detection. It will
not reliably identify a completely re-recorded cover with no shared source audio.

## Build and test

```powershell
docker build -t brandi-song-finder .
docker run --rm --entrypoint python brandi-song-finder -m unittest discover -s /app/tests
```

## Scan manifests

Mount the reference, manifests, and source drives read-only; mount only the result
folder writable. The CSV is flushed after every file, so a long scan is resumable
as evidence even if interrupted.

```powershell
docker run --rm `
  -v "D:\:/drives/d:ro" `
  -v "D:\2026 Extracted Archives\Audio Fingerprinting:/results" `
  brandi-song-finder `
  --reference /results/references/careless-whisper.m4a `
  --manifest "/drives/d/2026 Extracted Archives/Drive Manifests/Graham Audio Library Candidates/graham-library-long-audio-candidates.csv" `
  --map-prefix "D:=/drives/d" `
  --output /results/long-set-results.csv
```

Reference audio should be lawfully obtained. The acquisition helper used by this
sprint records the Apple Search API metadata and downloads only Apple's public
preview URL, not an unauthorized full recording.
