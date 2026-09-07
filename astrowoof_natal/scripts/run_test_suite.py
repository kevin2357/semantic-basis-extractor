"""Deterministic provider-free test shard coordinator.

This repository-only tool deliberately wraps unittest instead of changing the
installed package or its production logging defaults.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[2]
TEST_ROOT = ROOT / "astrowoof_natal" / "tests"
SOURCE_ROOT = ROOT / "astrowoof_natal" / "src"
DEFAULT_MANIFEST = TEST_ROOT / "test_suite_manifest.json"
SCHEMA_VERSION = "astrowoof.test-suite-run.v1"
DEFAULT_WORKERS = 1

DENIED_ENV_EXACT = {
    "DATABASE_URL",
    "RENDER_API_KEY",
    "OPENAI_API_KEY",
}
DENIED_ENV_PREFIXES = (
    "ASTROWOOF_",
    "AWS_",
    "CLOUDFLARE_",
    "RENDER_",
)


def _module_name(filename: str) -> str:
    return f"astrowoof_natal.tests.{Path(filename).stem}"


def _flatten(suite: unittest.TestSuite) -> list[unittest.TestCase]:
    tests: list[unittest.TestCase] = []
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            tests.extend(_flatten(item))
        else:
            tests.append(item)
    return tests


def _worker(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--inject-failure", action="store_true")
    parser.add_argument("modules", nargs="+")
    args = parser.parse_args(argv)

    started = time.perf_counter()
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromNames(args.modules)
    if args.inject_failure:
        class InjectedShardFailure(unittest.TestCase):
            def runTest(self) -> None:
                self.fail("deterministic Slice 4 shard failure")

            def id(self) -> str:
                return "astrowoof_test_runner.injected_failure"

        suite.addTest(InjectedShardFailure())
    identities = [test.id() for test in _flatten(suite)]
    runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=1, buffer=True)
    result = runner.run(suite)
    payload = {
        "schema_version": "astrowoof.test-suite-worker-result.v1",
        "duration_seconds": round(time.perf_counter() - started, 6),
        "test_count": result.testsRun,
        "skip_count": len(result.skipped),
        "success": result.wasSuccessful(),
        "test_identities": sorted(identities),
        "failures": [test.id() for test, _ in result.failures],
        "errors": [test.id() for test, _ in result.errors],
        "skipped": [test.id() for test, _ in result.skipped],
        "expected_failures": [test.id() for test, _ in result.expectedFailures],
        "unexpected_successes": [test.id() for test in result.unexpectedSuccesses],
    }
    args.result.write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    return 0 if result.wasSuccessful() else 1


def load_manifest(path: Path) -> dict:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema_version") != "astrowoof.test-suite-manifest.v1":
        raise ValueError("unsupported test-suite manifest version")
    return document


def validate_manifest(document: dict, test_root: Path = TEST_ROOT) -> None:
    discovered = {path.name for path in test_root.glob("test_*.py")}
    safe = [entry["module"] for entry in document["parallel_safe"]]
    provisional = list(document["provisional"])
    serial = list(document["serial_only"])
    classified = safe + provisional + serial
    duplicates = sorted({name for name in classified if classified.count(name) > 1})
    if duplicates:
        raise ValueError(f"duplicate manifest classifications: {duplicates}")
    missing = sorted(discovered - set(classified))
    extra = sorted(set(classified) - discovered)
    if missing or extra:
        raise ValueError(f"manifest mismatch: missing={missing}, extra={extra}")
    unknown_logging = sorted(set(document["logging_sensitive"]) - set(classified))
    if unknown_logging:
        raise ValueError(f"unknown logging-sensitive modules: {unknown_logging}")


def assign_weighted(entries: list[dict], worker_count: int) -> list[list[str]]:
    if worker_count < 1:
        raise ValueError("worker count must be positive")
    shards: list[list[str]] = [[] for _ in range(worker_count)]
    totals = [0.0] * worker_count
    ordered = sorted(
        entries,
        key=lambda item: (-float(item["weight_seconds"]), item["module"]),
    )
    for entry in ordered:
        target = min(range(worker_count), key=lambda index: (totals[index], index))
        shards[target].append(entry["module"])
        totals[target] += float(entry["weight_seconds"])
    return shards


def measurement_modules(document: dict, classification: str) -> list[str]:
    if classification == "parallel_safe":
        modules = [entry["module"] for entry in document["parallel_safe"]]
    elif classification in {"provisional", "serial_only"}:
        modules = list(document[classification])
    else:
        raise ValueError(f"unsupported measurement classification: {classification}")
    return sorted(modules)


def selected_measurement_modules(
    document: dict,
    classification: str,
    requested: list[str] | None,
) -> list[str]:
    available = measurement_modules(document, classification)
    if not requested:
        return available
    duplicates = sorted({name for name in requested if requested.count(name) > 1})
    if duplicates:
        raise ValueError(f"duplicate requested measurement modules: {duplicates}")
    unknown = sorted(set(requested) - set(available))
    if unknown:
        raise ValueError(
            f"measurement modules are not classified as {classification}: {unknown}"
        )
    return sorted(requested)


def serial_groups(document: dict) -> tuple[list[str], list[str]]:
    """Return provisional/serial modules split by quiet logging posture."""
    logging_sensitive = set(document["logging_sensitive"])
    serial = [*document["provisional"], *document["serial_only"]]
    return (
        [name for name in serial if name not in logging_sensitive],
        [name for name in serial if name in logging_sensitive],
    )


def sanitized_environment(base: dict[str, str] | None = None) -> dict[str, str]:
    source = dict(os.environ if base is None else base)
    for key in list(source):
        if key in DENIED_ENV_EXACT or any(key.startswith(prefix) for prefix in DENIED_ENV_PREFIXES):
            source.pop(key, None)
    return source


def _write_quiet_bootstrap(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "sitecustomize.py").write_text(
        "import logging\nlogging.disable(logging.INFO)\n",
        encoding="utf-8",
    )


def _run_group(
    *,
    name: str,
    modules: list[str],
    work_root: Path,
    quiet: bool,
    inject_failure: bool = False,
) -> dict:
    group_root = work_root / name
    group_root.mkdir(parents=True, exist_ok=True)
    result_path = group_root / "result.json"
    env = sanitized_environment()
    python_path = [str(SOURCE_ROOT), str(ROOT)]
    if quiet:
        bootstrap = group_root / "quiet-bootstrap"
        _write_quiet_bootstrap(bootstrap)
        python_path.insert(0, str(bootstrap))
    existing = env.get("PYTHONPATH")
    if existing:
        python_path.append(existing)
    env["PYTHONPATH"] = os.pathsep.join(python_path)
    for key in ("TMP", "TEMP", "TMPDIR"):
        env[key] = str(group_root / "tmp")
    env["XDG_CACHE_HOME"] = str(group_root / "cache")
    env["COVERAGE_FILE"] = str(group_root / ".coverage")
    env["ASTROWOOF_TEST_OUTPUT_ROOT"] = str(group_root / "output")
    for child in ("tmp", "cache", "output"):
        (group_root / child).mkdir(exist_ok=True)

    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker",
        "--result",
        str(result_path),
    ]
    if inject_failure:
        command.append("--inject-failure")
    command.extend(_module_name(module) for module in modules)
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    duration = time.perf_counter() - started
    result = (
        json.loads(result_path.read_text(encoding="utf-8"))
        if result_path.exists()
        else {
            "success": False,
            "test_count": 0,
            "skip_count": 0,
            "test_identities": [],
            "failures": [],
            "errors": ["worker_result_missing"],
            "skipped": [],
            "expected_failures": [],
            "unexpected_successes": [],
        }
    )
    result.update(
        {
            "name": name,
            "modules": modules,
            "command": command,
            "returncode": completed.returncode,
            "wall_seconds": round(duration, 6),
            "stdout_path": None,
            "stderr_path": None,
        }
    )
    if completed.returncode or os.environ.get("ASTROWOOF_TEST_VERBOSE") == "1":
        stdout_path = group_root / "stdout.log"
        stderr_path = group_root / "stderr.log"
        stdout_path.write_text(completed.stdout, encoding="utf-8")
        stderr_path.write_text(completed.stderr, encoding="utf-8")
        result["stdout_path"] = str(stdout_path)
        result["stderr_path"] = str(stderr_path)
    return result


def _inventory_digest(identities: list[str]) -> str:
    encoded = ("\n".join(sorted(identities)) + "\n").encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _outcome_inventory(results: list[dict]) -> list[str]:
    inventory: dict[str, str] = {}
    for result in results:
        for identity in result["test_identities"]:
            inventory[identity] = "passed"
        for key, classification in (
            ("skipped", "skipped"),
            ("expected_failures", "expected_failure"),
            ("unexpected_successes", "unexpected_success"),
            ("failures", "failed"),
            ("errors", "error"),
        ):
            for identity in result[key]:
                inventory[identity] = classification
    return [f"{identity}\t{inventory[identity]}" for identity in sorted(inventory)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--inject-failure", action="store_true")
    parser.add_argument("--result")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--parallel-only", action="store_true")
    parser.add_argument("--measure-weights", type=Path)
    parser.add_argument(
        "--measure-class",
        choices=("parallel_safe", "provisional", "serial_only"),
        default="parallel_safe",
    )
    parser.add_argument("--measure-module", action="append")
    parser.add_argument("--inject-failure-shard", type=int)
    parser.add_argument("modules", nargs="*")
    args = parser.parse_args(argv)
    if args.worker:
        worker_args = ["--result", args.result]
        if args.inject_failure:
            worker_args.append("--inject-failure")
        worker_args.extend(args.modules)
        return _worker(worker_args)

    manifest = load_manifest(args.manifest)
    validate_manifest(manifest)
    if args.measure_weights:
        measure_root = args.work_root or Path(
            tempfile.mkdtemp(prefix="astrowoof-test-weights-")
        )
        measurements = []
        for module in selected_measurement_modules(
            manifest, args.measure_class, args.measure_module
        ):
            result = _run_group(
                name=f"measure-{Path(module).stem}",
                modules=[module],
                work_root=measure_root,
                quiet=module not in manifest["logging_sensitive"],
            )
            measurements.append(
                {
                    "classification": args.measure_class,
                    "module": module,
                    "protected_logging": module in manifest["logging_sensitive"],
                    "success": result["success"],
                    "test_count": result["test_count"],
                    "skip_count": result["skip_count"],
                    "weight_seconds": result["wall_seconds"],
                }
            )
            if not result["success"]:
                break
        args.measure_weights.parent.mkdir(parents=True, exist_ok=True)
        args.measure_weights.write_text(
            json.dumps(measurements, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        return 0 if all(item["success"] for item in measurements) else 1
    shards = assign_weighted(manifest["parallel_safe"], args.workers)
    if args.inject_failure_shard is not None and not (
        1 <= args.inject_failure_shard <= args.workers
    ):
        raise ValueError("injected failure shard must name an existing worker")
    work_root = args.work_root or Path(tempfile.mkdtemp(prefix="astrowoof-tests-"))
    work_root.mkdir(parents=True, exist_ok=True)

    started = time.perf_counter()
    specifications: list[tuple[str, list[str], Path]] = []
    # Launch through this script's group helper in child coordinator processes so
    # each worker remains independently reproducible.
    for index, modules in enumerate(shards, start=1):
        specifications.append((f"parallel-{index}", modules, work_root))

    # Threading only coordinates independent subprocesses; unittest itself stays
    # process-isolated.
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [
            executor.submit(
                _run_group,
                name=name,
                modules=modules,
                work_root=root,
                quiet=True,
                inject_failure=args.inject_failure_shard == int(name.rsplit("-", 1)[1]),
            )
            for name, modules, root in specifications
        ]
        results = [future.result() for future in futures]

    if not args.parallel_only:
        quiet_serial, protected_serial = serial_groups(manifest)
        if quiet_serial:
            results.append(
                _run_group(
                    name="serial-quiet",
                    modules=quiet_serial,
                    work_root=work_root,
                    quiet=True,
                )
            )
        if protected_serial:
            results.append(
                _run_group(
                    name="serial-observability",
                    modules=protected_serial,
                    work_root=work_root,
                    quiet=False,
                )
            )

    identities = [identity for result in results for identity in result["test_identities"]]
    outcomes = _outcome_inventory(results)
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "manifest_sha256": hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
        "worker_count": args.workers,
        "parallel_only": args.parallel_only,
        "success": all(result["success"] and result["returncode"] == 0 for result in results),
        "test_count": sum(result["test_count"] for result in results),
        "skip_count": sum(result["skip_count"] for result in results),
        "test_inventory_sha256": _inventory_digest(identities),
        "outcome_inventory_sha256": _inventory_digest(outcomes),
        "wall_seconds": round(time.perf_counter() - started, 6),
        "groups": results,
    }
    receipt_path = args.receipt or work_root / "receipt.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: receipt[key] for key in (
        "success", "test_count", "skip_count", "test_inventory_sha256", "wall_seconds"
    )}, sort_keys=True))
    print(f"receipt={receipt_path}")
    return 0 if receipt["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
