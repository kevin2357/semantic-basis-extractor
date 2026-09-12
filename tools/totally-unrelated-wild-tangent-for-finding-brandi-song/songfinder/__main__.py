from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import subprocess
import sys
from pathlib import Path

from .core import compare_landmarks, decode, index_reference, landmarks


def duration(path: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip()
    return float(out)


def paths_from_manifest(path: Path, mappings: list[tuple[str, str]]) -> list[Path]:
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        rows = list(csv.DictReader(handle))
    choices = ("AccessiblePath", "RecoveredPath", "FullName", "Path", "FilePath", "full_path", "path")
    key = next((key for key in choices if key in (rows[0] if rows else {})), None)
    if not key:
        raise ValueError(f"No path column found in {path}")
    paths = []
    for row in rows:
        value = row.get(key)
        if not value:
            continue
        for source, target in mappings:
            if value.lower().startswith(source.lower()):
                value = target.rstrip("/") + "/" + value[len(source):].lstrip("\\/").replace("\\", "/")
                break
        paths.append(Path(value))
    return paths


def scan_one(references, path: Path, chunk: float, overlap: float) -> dict:
    row = {"path": str(path), "error": ""}
    try:
        length = duration(path)
        best = None
        start = 0.0
        while start < length:
            samples = decode(path, start, min(chunk, length - start))
            candidate_landmarks = landmarks(samples)
            for variant, reference in references.items():
                match = compare_landmarks(reference, candidate_landmarks, start)
                if best is None or (match.unique_hashes, match.votes) > (best[1].unique_hashes, best[1].votes):
                    best = (variant, match)
            start += chunk - overlap
        variant, best = best
        row.update(duration_seconds=round(length, 3), best_timestamp_seconds=round(best.offset_seconds, 3),
                   votes=best.votes, unique_hashes=best.unique_hashes,
                   confidence=round(best.confidence, 6), reference_variant=variant)
    except Exception as exc:
        row["error"] = str(exc)[:500]
    return row


def scan(reference_paths: list[Path], files: list[Path], output: Path, chunk: float, overlap: float, workers: int) -> None:
    references = {path.stem: index_reference(decode(path)) for path in reference_paths}
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["path", "duration_seconds", "best_timestamp_seconds", "votes", "unique_hashes", "confidence", "reference_variant", "error"]
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(scan_one, references, path, chunk, overlap): path for path in files}
            for number, future in enumerate(concurrent.futures.as_completed(futures), 1):
                row = future.result()
                writer.writerow(row)
                handle.flush()
                print(f"[{number}/{len(files)}] {row['path']} :: {row.get('unique_hashes', 0)} hashes", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Find a song inside long audio using spectral landmark hashes.")
    parser.add_argument("--reference", type=Path, required=True, action="append")
    parser.add_argument("--manifest", type=Path, action="append", default=[])
    parser.add_argument("--file", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--map-prefix", action="append", default=[], metavar="HOST=CONTAINER",
                        help="translate manifest paths, e.g. D:=/drives/d")
    parser.add_argument("--chunk-seconds", type=float, default=180)
    parser.add_argument("--overlap-seconds", type=float, default=12)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    mappings = [tuple(value.split("=", 1)) for value in args.map_prefix]
    files = list(args.file)
    for manifest in args.manifest:
        files.extend(paths_from_manifest(manifest, mappings))
    files = list(dict.fromkeys(path for path in files if path.exists()))
    print(json.dumps({"references": [str(path) for path in args.reference], "files": len(files), "output": str(args.output)}))
    scan(args.reference, files, args.output, args.chunk_seconds, args.overlap_seconds, args.workers)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        raise
