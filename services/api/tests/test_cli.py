"""Tests for the URLSentinel Command Line Interface (CLI)."""

import pytest
import json
from unittest.mock import patch, MagicMock
from urlsentinel.cli import main, format_sarif


class TestCLI:
    """Test suite for CLI arguments, scan execution, and exit codes."""

    def test_version_command(self, capsys):
        exit_code = main(["version"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "URLSentinel CLI v1.0.0" in captured.out

    def test_scan_benign_url_returns_zero(self, capsys):
        with patch("urlsentinel.cli.httpx.post") as mock_post:
            mock_post.side_effect = Exception("Offline mode")
            with patch("urlsentinel.core.ssrf_guard.validate_destination_safety", return_value=("https://example.com", ["93.184.216.34"])):
                exit_code = main(["scan", "https://example.com"])
                captured = capsys.readouterr()
                assert exit_code == 0
                assert "BENIGN" in captured.out

    def test_scan_malicious_url_returns_code_two(self, capsys):
        with patch("urlsentinel.cli.httpx.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                "id": "scan-123",
                "url": "http://evil-phish.top/login",
                "verdict": "MALICIOUS",
                "risk_score": 95,
                "confidence": "HIGH",
                "summary": "Confirmed phishing threat",
                "recommended_action": "Block",
                "evidence": [],
            }
            mock_post.return_value = mock_resp

            exit_code = main(["scan", "http://evil-phish.top/login"])
            assert exit_code == 2

    def test_scan_ssrf_blocked_returns_code_three(self, capsys):
        with patch("urlsentinel.cli.httpx.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 400
            mock_resp.json.return_value = {"message": "SSRF violation"}
            mock_post.return_value = mock_resp

            exit_code = main(["scan", "http://127.0.0.1:8000/secret"])
            assert exit_code == 3

    def test_sarif_export_structure(self):
        verdict_data = {
            "id": "test-id",
            "url": "https://malicious.example.com",
            "verdict": "MALICIOUS",
            "risk_score": 98,
            "confidence": "HIGH",
            "summary": "Active phishing domain",
        }
        sarif = format_sarif(verdict_data)
        assert sarif["version"] == "2.1.0"
        assert len(sarif["runs"]) == 1
        run = sarif["runs"][0]
        assert run["tool"]["driver"]["name"] == "URLSentinel"
        assert len(run["results"]) == 1
        assert run["results"][0]["level"] == "error"
