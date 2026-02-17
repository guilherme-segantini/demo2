"""Tests for Grok service."""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from app.services.grok_service import (
    analyze_focus_area,
    run_full_analysis,
    check_api_connection,
    validate_trend,
    call_grok_with_retry,
    load_prompt,
    is_sap_configured,
    get_model_name,
    FOCUS_AREAS,
    PROMPT_FILES,
    PROMPTS_DIR,
)


class TestFocusAreas:
    """Test focus area configuration."""

    def test_all_focus_areas_defined(self):
        """Verify all expected focus areas are configured."""
        expected = {"voice_ai_ux", "agent_orchestration", "durable_runtime"}
        assert set(FOCUS_AREAS.keys()) == expected

    def test_focus_areas_have_required_fields(self):
        """Verify each focus area has name and evaluation criteria."""
        for area_id, config in FOCUS_AREAS.items():
            assert "name" in config, f"{area_id} missing 'name'"
            assert "evaluation_criteria" in config, f"{area_id} missing 'evaluation_criteria'"


class TestAnalyzeFocusArea:
    """Test single focus area analysis."""

    def test_invalid_focus_area_raises_error(self):
        """Test that invalid focus area raises ValueError."""
        with pytest.raises(ValueError, match="Unknown focus area"):
            analyze_focus_area("invalid_area")

    @patch("app.services.grok_service.litellm.completion")
    def test_successful_analysis(self, mock_completion):
        """Test successful API response parsing."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = """[
            {
                "tool_name": "TestTool",
                "classification": "signal",
                "confidence_score": 85,
                "technical_insight": "Great benchmarks",
                "signal_evidence": ["published benchmarks"],
                "noise_indicators": [],
                "architectural_verdict": true
            }
        ]"""
        mock_completion.return_value = mock_response

        result = analyze_focus_area("voice_ai_ux")

        assert result is not None
        assert len(result) == 1
        assert result[0]["tool_name"] == "TestTool"
        assert result[0]["focus_area"] == "voice_ai_ux"
        assert "timestamp" in result[0]

    @patch("app.services.grok_service.litellm.completion")
    def test_json_extraction_from_text(self, mock_completion):
        """Test JSON extraction when response has surrounding text."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = """Here are the results:
        [{"tool_name": "Tool1", "classification": "noise", "confidence_score": 70, "technical_insight": "Hype", "signal_evidence": [], "noise_indicators": ["marketing"], "architectural_verdict": false}]
        Hope this helps!"""
        mock_completion.return_value = mock_response

        result = analyze_focus_area("agent_orchestration")

        assert result is not None
        assert len(result) == 1
        assert result[0]["tool_name"] == "Tool1"

    @patch("app.services.grok_service.litellm.completion")
    def test_invalid_json_returns_none(self, mock_completion):
        """Test that invalid JSON returns None."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "This is not valid JSON"
        mock_completion.return_value = mock_response

        result = analyze_focus_area("durable_runtime")

        assert result is None

    @patch("app.services.grok_service.litellm.completion")
    def test_api_error_returns_none(self, mock_completion):
        """Test that API errors return None."""
        mock_completion.side_effect = Exception("API Error")

        result = analyze_focus_area("voice_ai_ux")

        assert result is None


class TestRunFullAnalysis:
    """Test full analysis across all focus areas."""

    @patch("app.services.grok_service.analyze_focus_area")
    def test_aggregates_all_focus_areas(self, mock_analyze):
        """Test that full analysis aggregates results from all areas."""
        mock_analyze.side_effect = [
            [{"tool_name": "VoiceTool", "focus_area": "voice_ai_ux"}],
            [{"tool_name": "AgentTool", "focus_area": "agent_orchestration"}],
            [{"tool_name": "RuntimeTool", "focus_area": "durable_runtime"}],
        ]

        result = run_full_analysis()

        assert "radar_date" in result
        assert "trends" in result
        assert len(result["trends"]) == 3

    @patch("app.services.grok_service.analyze_focus_area")
    def test_handles_partial_failures(self, mock_analyze):
        """Test that partial failures don't break full analysis."""
        mock_analyze.side_effect = [
            [{"tool_name": "VoiceTool", "focus_area": "voice_ai_ux"}],
            None,  # Failed analysis
            [{"tool_name": "RuntimeTool", "focus_area": "durable_runtime"}],
        ]

        result = run_full_analysis()

        assert len(result["trends"]) == 2

    @patch("app.services.grok_service.analyze_focus_area")
    def test_returns_empty_trends_on_total_failure(self, mock_analyze):
        """Test that total failure returns empty trends list."""
        mock_analyze.return_value = None

        result = run_full_analysis()

        assert result["trends"] == []
        assert "radar_date" in result


class TestValidateTrend:
    """Test trend validation function."""

    def test_valid_signal_trend(self):
        """Test valid signal trend passes validation."""
        trend = {
            "tool_name": "TestTool",
            "classification": "signal",
            "confidence_score": 85,
            "technical_insight": "Good benchmarks",
            "architectural_verdict": True,
        }
        assert validate_trend(trend) is True

    def test_valid_noise_trend(self):
        """Test valid noise trend passes validation."""
        trend = {
            "tool_name": "HypeTool",
            "classification": "noise",
            "confidence_score": 40,
            "technical_insight": "All marketing",
            "architectural_verdict": False,
        }
        assert validate_trend(trend) is True

    def test_missing_required_field(self):
        """Test trend missing required field fails validation."""
        trend = {
            "tool_name": "TestTool",
            "classification": "signal",
            # missing confidence_score
            "technical_insight": "Test",
            "architectural_verdict": True,
        }
        assert validate_trend(trend) is False

    def test_invalid_classification(self):
        """Test invalid classification value fails validation."""
        trend = {
            "tool_name": "TestTool",
            "classification": "maybe",  # invalid
            "confidence_score": 85,
            "technical_insight": "Test",
            "architectural_verdict": True,
        }
        assert validate_trend(trend) is False

    def test_confidence_score_out_of_range(self):
        """Test confidence score out of range fails validation."""
        trend = {
            "tool_name": "TestTool",
            "classification": "signal",
            "confidence_score": 150,  # out of range
            "technical_insight": "Test",
            "architectural_verdict": True,
        }
        assert validate_trend(trend) is False

    def test_confidence_score_zero(self):
        """Test confidence score of 0 fails validation."""
        trend = {
            "tool_name": "TestTool",
            "classification": "signal",
            "confidence_score": 0,
            "technical_insight": "Test",
            "architectural_verdict": True,
        }
        assert validate_trend(trend) is False


class TestCallGrokWithRetry:
    """Test retry logic for Grok API calls."""

    @patch("app.services.grok_service.litellm.completion")
    def test_successful_first_attempt(self, mock_completion):
        """Test successful response on first attempt."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test response"
        mock_completion.return_value = mock_response

        result = call_grok_with_retry("Test prompt")

        assert result == "Test response"
        assert mock_completion.call_count == 1

    @patch("app.services.grok_service.time.sleep")
    @patch("app.services.grok_service.litellm.completion")
    def test_retry_on_failure(self, mock_completion, mock_sleep):
        """Test retry behavior on API failure."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Success"
        mock_completion.side_effect = [
            Exception("First failure"),
            Exception("Second failure"),
            mock_response,
        ]

        result = call_grok_with_retry("Test prompt")

        assert result == "Success"
        assert mock_completion.call_count == 3
        assert mock_sleep.call_count == 2

    @patch("app.services.grok_service.time.sleep")
    @patch("app.services.grok_service.litellm.completion")
    def test_all_retries_exhausted(self, mock_completion, mock_sleep):
        """Test returns None when all retries are exhausted."""
        mock_completion.side_effect = Exception("Always fails")

        result = call_grok_with_retry("Test prompt")

        assert result is None
        assert mock_completion.call_count == 3


class TestCheckApiConnection:
    """Test API connection check function."""

    @patch("app.services.grok_service.litellm.completion")
    def test_successful_connection(self, mock_completion):
        """Test successful API connection check."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "OK"
        mock_completion.return_value = mock_response

        result = check_api_connection()

        assert result["status"] == "ok"
        assert "provider" in result

    @patch("app.services.grok_service.litellm.completion")
    def test_connection_failure(self, mock_completion):
        """Test API connection failure."""
        mock_completion.side_effect = Exception("Connection refused")

        result = check_api_connection()

        assert result["status"] == "error"
        assert "Connection refused" in result["message"]


class TestLoadPrompt:
    """Test external prompt loading functionality."""

    def test_load_voice_ai_prompt(self):
        """Test loading voice_ai_ux prompt from external file."""
        prompt = load_prompt("voice_ai_ux")

        assert prompt is not None
        assert "Voice AI" in prompt
        assert "SIGNAL" in prompt or "signal" in prompt.lower()
        assert "NOISE" in prompt or "noise" in prompt.lower()

    def test_load_agent_orchestration_prompt(self):
        """Test loading agent_orchestration prompt from external file."""
        prompt = load_prompt("agent_orchestration")

        assert prompt is not None
        assert "Agent" in prompt or "agent" in prompt
        assert "orchestration" in prompt.lower()

    def test_load_durable_runtime_prompt(self):
        """Test loading durable_runtime prompt from external file."""
        prompt = load_prompt("durable_runtime")

        assert prompt is not None
        assert "Durable" in prompt or "durable" in prompt
        assert "runtime" in prompt.lower()

    def test_load_unknown_focus_area_returns_none(self):
        """Test that unknown focus area returns None."""
        prompt = load_prompt("unknown_focus_area")

        assert prompt is None

    def test_prompt_files_exist(self):
        """Verify all mapped prompt files exist."""
        for focus_area, filename in PROMPT_FILES.items():
            prompt_path = PROMPTS_DIR / filename
            assert prompt_path.exists(), f"Missing prompt file: {prompt_path}"

    def test_prompts_contain_json_schema(self):
        """Verify prompts include JSON output schema."""
        for focus_area in PROMPT_FILES.keys():
            prompt = load_prompt(focus_area)
            assert prompt is not None
            assert "tool_name" in prompt
            assert "classification" in prompt
            assert "confidence_score" in prompt


class TestSapConfiguration:
    """Test SAP Generative AI Hub configuration detection."""

    @patch.dict("os.environ", {}, clear=True)
    @patch("app.services.grok_service.AICORE_SERVICE_KEY", None)
    @patch("app.services.grok_service.AICORE_AUTH_URL", None)
    @patch("app.services.grok_service.AICORE_CLIENT_ID", None)
    @patch("app.services.grok_service.AICORE_CLIENT_SECRET", None)
    @patch("app.services.grok_service.AICORE_BASE_URL", None)
    def test_no_sap_config_returns_false(self):
        """Test is_sap_configured returns False when no SAP credentials."""
        assert is_sap_configured() is False

    @patch("app.services.grok_service.AICORE_SERVICE_KEY", '{"key": "value"}')
    def test_service_key_config_returns_true(self):
        """Test is_sap_configured returns True with service key."""
        assert is_sap_configured() is True

    @patch("app.services.grok_service.AICORE_SERVICE_KEY", None)
    @patch("app.services.grok_service.AICORE_AUTH_URL", "https://auth.example.com")
    @patch("app.services.grok_service.AICORE_CLIENT_ID", "client-id")
    @patch("app.services.grok_service.AICORE_CLIENT_SECRET", "secret")
    @patch("app.services.grok_service.AICORE_BASE_URL", "https://api.example.com")
    def test_individual_credentials_returns_true(self):
        """Test is_sap_configured returns True with individual credentials."""
        assert is_sap_configured() is True

    @patch("app.services.grok_service.is_sap_configured")
    def test_get_model_name_sap(self, mock_sap_configured):
        """Test model name uses sap/ prefix when SAP is configured."""
        mock_sap_configured.return_value = True
        model = get_model_name()
        assert model.startswith("sap/")

    @patch("app.services.grok_service.is_sap_configured")
    def test_get_model_name_local(self, mock_sap_configured):
        """Test model name uses openai/ prefix when SAP is not configured."""
        mock_sap_configured.return_value = False
        model = get_model_name()
        assert model.startswith("openai/")


class TestAnalyzeFocusAreaWithExternalPrompts:
    """Test analyze_focus_area uses external prompts."""

    @patch("app.services.grok_service.load_prompt")
    @patch("app.services.grok_service.litellm.completion")
    def test_uses_external_prompt_when_available(self, mock_completion, mock_load_prompt):
        """Test that external prompt is used when available."""
        mock_load_prompt.return_value = "External prompt content"
        mock_response = MagicMock()
        mock_response.choices[0].message.content = """[
            {
                "tool_name": "TestTool",
                "classification": "signal",
                "confidence_score": 85,
                "technical_insight": "Test insight",
                "signal_evidence": ["evidence"],
                "noise_indicators": [],
                "architectural_verdict": true
            }
        ]"""
        mock_completion.return_value = mock_response

        result = analyze_focus_area("voice_ai_ux")

        mock_load_prompt.assert_called_once_with("voice_ai_ux")
        # Verify the prompt passed to completion contains external content
        call_args = mock_completion.call_args
        assert "External prompt content" in str(call_args)

    @patch("app.services.grok_service.load_prompt")
    @patch("app.services.grok_service.litellm.completion")
    def test_falls_back_to_inline_when_external_missing(self, mock_completion, mock_load_prompt):
        """Test fallback to inline template when external prompt not found."""
        mock_load_prompt.return_value = None  # Simulate missing file
        mock_response = MagicMock()
        mock_response.choices[0].message.content = """[
            {
                "tool_name": "TestTool",
                "classification": "signal",
                "confidence_score": 85,
                "technical_insight": "Test insight",
                "signal_evidence": ["evidence"],
                "noise_indicators": [],
                "architectural_verdict": true
            }
        ]"""
        mock_completion.return_value = mock_response

        result = analyze_focus_area("voice_ai_ux")

        # Should still succeed using inline template
        assert result is not None
        assert len(result) == 1
