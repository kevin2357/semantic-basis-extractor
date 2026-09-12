from __future__ import annotations

import collections
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy import ndimage, signal

SAMPLE_RATE = 11025
FFT_SIZE = 2048
HOP = 512


@dataclass(frozen=True)
class Match:
    votes: int
    unique_hashes: int
    offset_seconds: float
    confidence: float


def decode(path: Path, start: float | None = None, duration: float | None = None) -> np.ndarray:
    cmd = ["ffmpeg", "-nostdin", "-v", "error"]
    if start is not None:
        cmd += ["-ss", str(start)]
    cmd += ["-i", str(path)]
    if duration is not None:
        cmd += ["-t", str(duration)]
    cmd += ["-vn", "-ac", "1", "-ar", str(SAMPLE_RATE), "-f", "f32le", "pipe:1"]
    completed = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return np.frombuffer(completed.stdout, dtype="<f4")


def landmarks(samples: np.ndarray) -> list[tuple[tuple[int, int, int], int]]:
    """Return (packed landmark hash, anchor frame) pairs."""
    if len(samples) < FFT_SIZE:
        return []
    _, _, z = signal.stft(samples, fs=SAMPLE_RATE, nperseg=FFT_SIZE,
                          noverlap=FFT_SIZE - HOP, boundary=None, padded=False)
    power = np.log1p(np.abs(z))
    floor = np.quantile(power, 0.82)
    maxima = power == ndimage.maximum_filter(power, size=(15, 7), mode="constant")
    freq, frame = np.nonzero(maxima & (power >= floor))
    strengths = power[freq, frame]
    # Keep the strongest landmarks, capped per time frame for noisy recordings.
    order = np.argsort(strengths)[::-1]
    peaks: list[tuple[int, int]] = []
    per_frame: collections.Counter[int] = collections.Counter()
    for i in order:
        f, t = int(freq[i]), int(frame[i])
        if per_frame[t] < 5:
            peaks.append((t, f))
            per_frame[t] += 1
    peaks.sort()
    result: list[tuple[tuple[int, int, int], int]] = []
    for i, (t1, f1) in enumerate(peaks):
        fanout = 0
        for t2, f2 in peaks[i + 1:]:
            dt = t2 - t1
            if dt < 2:
                continue
            if dt > 86:  # roughly four seconds
                break
            # Coarse bins tolerate codec artifacts and arbitrary STFT frame alignment.
            qf1, qf2, qdt = f1 // 2, f2 // 2, dt // 2
            result.append(((qf1, qf2, qdt), t1))
            fanout += 1
            if fanout == 8:
                break
    return result


def index_reference(samples: np.ndarray) -> dict[tuple[int, int, int], list[int]]:
    index: dict[tuple[int, int, int], list[int]] = collections.defaultdict(list)
    for digest, frame in landmarks(samples):
        qf1, qf2, qdt = digest
        # Index a tiny neighborhood; peak bins often move by one after lossy
        # encoding, EQ, or because the excerpt begins between analysis frames.
        for df1 in (-1, 0, 1):
            for df2 in (-1, 0, 1):
                for ddt in (-1, 0, 1):
                    if qf1 + df1 >= 0 and qf2 + df2 >= 0 and qdt + ddt >= 0:
                        variant = (qf1 + df1, qf2 + df2, qdt + ddt)
                        index[variant].append(frame)
    return dict(index)


def compare(reference: dict[tuple[int, int, int], list[int]], samples: np.ndarray, base_seconds: float = 0.0) -> Match:
    return compare_landmarks(reference, landmarks(samples), base_seconds)


def compare_landmarks(reference: dict[tuple[int, int, int], list[int]], candidate_landmarks, base_seconds: float = 0.0) -> Match:
    offsets: collections.Counter[int] = collections.Counter()
    unique: collections.defaultdict[int, set[int]] = collections.defaultdict(set)
    for digest, candidate_frame in candidate_landmarks:
        for reference_frame in reference.get(digest, ()):
            offset = candidate_frame - reference_frame
            offsets[offset] += 1
            unique[offset].add(digest)
    if not offsets:
        return Match(0, 0, base_seconds, 0.0)
    offset, votes = offsets.most_common(1)[0]
    distinct = len(unique[offset])
    confidence = distinct / max(1, len(reference))
    return Match(votes, distinct, base_seconds + offset * HOP / SAMPLE_RATE, confidence)
