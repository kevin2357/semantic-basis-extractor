from __future__ import annotations

import json
import io
import os
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from importlib.resources import files
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astrowoof_natal_authoring.closure import (  # noqa: E402
    OpenAIServiceError,
    UrllibJsonTransport,
)
from astrowoof_natal_authoring.response_diagnostics import (  # noqa: E402
    build_response_retrieval_diagnostic,
    inspect_response,
    read_response_retrieval_diagnostic_schema,
    sanitize_error_message,
    validate_response_retrieval_diagnostic,
)


class ScriptedTransport:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = []

    def request_json(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return self.result


class TestResponseDiagnostics(unittest.TestCase):
    def probe(self, result=None, error=None):
        transport = ScriptedTransport(result=result, error=error)
        clocks = iter(["2026-08-19T12:00:00.000Z", "2026-08-19T12:00:00.025Z"])
        monotonic = iter([10.0, 10.025])
        value = inspect_response(
            "resp_fixture", api_key="sk-super-secret-fixture",
            base_url="https://api.openai.com/v1?token=nope",
            transport=transport, clock=lambda: next(clocks),
            monotonic=lambda: next(monotonic),
        )
        self.assertEqual(1, len(transport.calls))
        call = transport.calls[0]
        self.assertEqual("GET", call["method"])
        self.assertIsNone(call["payload"])
        validate_response_retrieval_diagnostic(value)
        return value

    def test_completed_and_pending(self):
        complete = self.probe({"id": "resp_fixture", "status": "completed"})
        self.assertEqual("completed", complete["outcome"])
        self.assertEqual(25, complete["duration_ms"])
        self.assertEqual("https://api.openai.com", complete["endpoint"]["configured_host"])
        pending = self.probe({"id": "resp_fixture", "status": "in_progress"})
        self.assertEqual("pending", pending["outcome"])
        provider_failed = self.probe({"id": "resp_fixture", "status": "failed"})
        self.assertEqual("completed", provider_failed["outcome"])
        self.assertEqual("failed", provider_failed["provider_status"])

    def test_http_diagnostics_are_exact_and_sanitized(self):
        for status in (401, 404, 429):
            with self.subTest(status=status):
                value = self.probe(error=OpenAIServiceError(
                    f"HTTP failure Bearer sk-super-secret-fixture body detail {status}",
                    status_code=status, request_id=f"req_{status}",
                ))
                self.assertEqual("transport_warning", value["outcome"])
                self.assertEqual(status, value["http_status"])
                self.assertEqual(f"req_{status}", value["provider_request_id"])
                self.assertEqual("OpenAIServiceError", value["exception_class"])
                self.assertNotIn("super-secret", value["error_message"])
                self.assertRegex(value["error_fingerprint"], r"^[0-9a-f]{64}$")

    def test_urllib_transport_retains_http_request_id(self):
        error = urllib.error.HTTPError(
            "https://api.openai.com/v1/responses/resp_fixture",
            401, "Unauthorized", {"x-request-id": "req_transport_fixture"},
            io.BytesIO(b'{"error":{"message":"bad credential"}}'),
        )
        with patch("urllib.request.urlopen", side_effect=error):
            with self.assertRaises(OpenAIServiceError) as raised:
                UrllibJsonTransport().request_json(
                    method="GET", url=error.url,
                    headers={"Authorization": "Bearer secret"}, payload=None,
                    timeout_seconds=15,
                )
        self.assertEqual(401, raised.exception.status_code)
        self.assertEqual("req_transport_fixture", raised.exception.request_id)

    def test_timeout_malformed_and_identity_conflict(self):
        timeout = self.probe(error=TimeoutError("fixture timeout"))
        self.assertEqual("TimeoutError", timeout["exception_class"])
        malformed = self.probe(["not", "an", "object"])
        self.assertEqual("transport_warning", malformed["outcome"])
        self.assertIn("malformed", malformed["error_message"])
        mismatch = self.probe({"id": "resp_wrong", "status": "completed"})
        self.assertEqual("identity_conflict", mismatch["outcome"])

    def test_schema_and_closed_validator(self):
        schema = read_response_retrieval_diagnostic_schema()
        self.assertEqual("astrowoof.response_retrieval_diagnostic.v1", schema["$id"])
        value = build_response_retrieval_diagnostic(
            provider_response_id="resp_fixture", outcome="pending",
            started_at="2026-08-19T12:00:00Z",
            finished_at="2026-08-19T12:00:01Z", duration_ms=1000,
        )
        value["surprise"] = True
        with self.assertRaisesRegex(ValueError, "not closed"):
            validate_response_retrieval_diagnostic(value)
        fixture = json.loads(files("astrowoof_natal_authoring").joinpath(
            "resources/fixtures/lifecycle/response-retrieval-transport-warning.v1.json"
        ).read_text(encoding="utf-8"))
        validate_response_retrieval_diagnostic(fixture)

    def test_sanitizer_bounds_and_redacts(self):
        value = sanitize_error_message(
            "Bearer abc.def sk-abcdefghijk api_key=secret " + "x" * 1000,
            secret="secret",
        )
        self.assertLessEqual(len(value), 512)
        self.assertNotIn("abc.def", value)
        self.assertNotIn("abcdefghijk", value)
        self.assertNotIn("secret", value)

    def test_cli_schema_and_native_workspace_output_refusal(self):
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        schema = subprocess.run(
            [sys.executable, "-m", "astrowoof_natal_authoring.cli.inspect_response", "--schema"],
            env=env, capture_output=True, text=True, check=True,
        )
        self.assertEqual(
            "astrowoof.response_retrieval_diagnostic.v1",
            json.loads(schema.stdout)["$id"],
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "run.json").write_text("{}", encoding="utf-8")
            (root / "workspace-snapshot.json").write_text("{}", encoding="utf-8")
            refused = subprocess.run(
                [sys.executable, "-m", "astrowoof_natal_authoring.cli.inspect_response",
                 "--schema", "--output", str(root / "diagnostic.json")],
                env=env, capture_output=True, text=True,
            )
            self.assertNotEqual(0, refused.returncode)
            self.assertFalse((root / "diagnostic.json").exists())


if __name__ == "__main__":
    unittest.main()
