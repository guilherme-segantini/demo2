"""Grok/LiteLLM service for AI-powered radar analysis."""

import json
import logging
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import litellm
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# LiteLLM configuration
LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "http://localhost:4010")
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "sk-radar-local-dev")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-3")

# SAP Generative AI Hub configuration
# See: https://docs.litellm.ai/docs/providers/sap
AICORE_SERVICE_KEY = os.getenv("AICORE_SERVICE_KEY")  # Recommended: JSON service key
AICORE_AUTH_URL = os.getenv("AICORE_AUTH_URL")
AICORE_CLIENT_ID = os.getenv("AICORE_CLIENT_ID")
AICORE_CLIENT_SECRET = os.getenv("AICORE_CLIENT_SECRET")
AICORE_BASE_URL = os.getenv("AICORE_BASE_URL")
AICORE_RESOURCE_GROUP = os.getenv("AICORE_RESOURCE_GROUP", "default")

# Prompt file mapping
PROMPT_FILES = {
    "voice_ai_ux": "voice_ai_prompt.md",
    "agent_orchestration": "agent_orchestration_prompt.md",
    "durable_runtime": "durable_runtime_prompt.md",
}

# Project root for locating prompt files
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"


def is_sap_configured() -> bool:
    """Check if SAP Generative AI Hub credentials are configured."""
    # Check for service key (recommended method)
    if AICORE_SERVICE_KEY:
        return True
    # Check for individual credentials
    return all([AICORE_AUTH_URL, AICORE_CLIENT_ID, AICORE_CLIENT_SECRET, AICORE_BASE_URL])


def get_model_name() -> str:
    """Get the appropriate model name based on configuration."""
    if is_sap_configured():
        # Use SAP prefix for Generative AI Hub
        return f"sap/{GROK_MODEL}"
    # Default to openai prefix for local LiteLLM proxy
    return f"openai/{GROK_MODEL}"


def load_prompt(focus_area: str) -> Optional[str]:
    """
    Load prompt template from external markdown file.

    Extracts the "User Prompt" section from the markdown file.
    Returns None if file not found or parsing fails.
    """
    if focus_area not in PROMPT_FILES:
        logger.warning(f"No prompt file mapping for focus area: {focus_area}")
        return None

    prompt_path = PROMPTS_DIR / PROMPT_FILES[focus_area]

    if not prompt_path.exists():
        logger.warning(f"Prompt file not found: {prompt_path}")
        return None

    try:
        content = prompt_path.read_text(encoding="utf-8")

        # Extract User Prompt section (everything after "## User Prompt")
        user_prompt_match = re.search(
            r"## User Prompt\s*\n(.*)",
            content,
            re.DOTALL | re.IGNORECASE,
        )

        if user_prompt_match:
            user_prompt = user_prompt_match.group(1).strip()
            logger.debug(f"Loaded external prompt for {focus_area} ({len(user_prompt)} chars)")
            return user_prompt

        logger.warning(f"No '## User Prompt' section found in {prompt_path}")
        return None

    except Exception as e:
        logger.error(f"Error reading prompt file {prompt_path}: {e}")
        return None

# Retry configuration
MAX_RETRIES = 3
INITIAL_BACKOFF = 1.0  # seconds

FOCUS_AREAS = {
    "voice_ai_ux": {
        "name": "Voice AI UX",
        "evaluation_criteria": """
- Latency benchmarks (target: sub-200ms voice-to-voice)
- Interruption handling and VAD (Voice Activity Detection) implementation
- WebRTC/streaming architecture details
- SDK availability and async streaming support
""",
    },
    "agent_orchestration": {
        "name": "Agent Orchestration",
        "evaluation_criteria": """
- BKG/Knowledge Graph integration capabilities
- Tool chaining patterns and workflow composition
- State persistence and checkpoint/recovery mechanisms
- Human-in-the-loop specifications
""",
    },
    "durable_runtime": {
        "name": "Durable Runtime",
        "evaluation_criteria": """
- Durability guarantees and SLAs
- Cold-start benchmarks (target: <100ms)
- Checkpoint/recovery specifications
- Fault tolerance and automatic retry mechanisms
""",
    },
}

DISCOVERY_PROMPT_TEMPLATE = """Using your real-time knowledge of X/Twitter discussions and tech news from the past 7 days,
SEARCH for and ANALYZE tools related to {focus_area}.

STEP 1 - DISCOVER:
Search your knowledge for tools being discussed in the {focus_area_name} space.
Look for announcements, releases, technical discussions, and trending topics.

STEP 2 - CLASSIFY each discovered tool as SIGNAL or NOISE:

SIGNAL criteria (worth evaluating):
- Has published benchmarks or performance data
- Shows production usage or real case studies
- Provides specific technical architecture details
- Has active technical community discussion

NOISE criteria (skip):
- Uses marketing language without substance
- No benchmarks or only vague claims
- Pre-announcement hype or vaporware
- Engagement farming without technical depth

For {focus_area_name}, specifically evaluate:
{evaluation_criteria}

Return a JSON array with 2-4 tools (mix of signal and noise). Format:
[
  {{
    "tool_name": "string",
    "classification": "signal" or "noise",
    "confidence_score": 1-100,
    "technical_insight": "specific technical details you found",
    "signal_evidence": ["evidence1", "evidence2"],
    "noise_indicators": ["indicator1", "indicator2"],
    "architectural_verdict": true or false
  }}
]

IMPORTANT: Return ONLY the JSON array, no other text."""


def validate_trend(trend: dict) -> bool:
    """Validate a trend dictionary has all required fields."""
    required_fields = [
        "tool_name",
        "classification",
        "confidence_score",
        "technical_insight",
        "architectural_verdict",
    ]
    for field in required_fields:
        if field not in trend:
            return False

    # Validate classification value
    if trend["classification"] not in ("signal", "noise"):
        return False

    # Validate confidence score range
    if not isinstance(trend["confidence_score"], int) or not 1 <= trend["confidence_score"] <= 100:
        return False

    return True


def call_grok_with_retry(prompt: str) -> Optional[str]:
    """
    Call Grok API with exponential backoff retry logic.

    Automatically selects SAP Generative AI Hub or local LiteLLM proxy
    based on environment configuration.

    Returns response content string or None if all retries fail.
    """
    backoff = INITIAL_BACKOFF
    model = get_model_name()

    # Configure API parameters based on provider
    api_params = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    if is_sap_configured():
        # SAP Generative AI Hub - credentials are read from environment
        # by LiteLLM automatically when using sap/ prefix
        logger.debug(f"Using SAP Generative AI Hub with model: {model}")
    else:
        # Local LiteLLM proxy
        api_params["api_base"] = LITELLM_BASE_URL
        api_params["api_key"] = LITELLM_API_KEY
        logger.debug(f"Using local LiteLLM proxy at {LITELLM_BASE_URL}")

    for attempt in range(MAX_RETRIES):
        try:
            response = litellm.completion(**api_params)
            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.warning(
                f"Grok API call failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}"
            )
            if attempt < MAX_RETRIES - 1:
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff

    logger.error(f"All {MAX_RETRIES} Grok API attempts failed")
    return None


def analyze_focus_area(focus_area: str) -> Optional[list[dict]]:
    """
    Analyze a single focus area using Grok via LiteLLM.

    Loads prompt from external markdown file if available,
    falls back to inline template otherwise.

    Returns list of trend dictionaries or None if analysis fails.
    """
    if focus_area not in FOCUS_AREAS:
        raise ValueError(f"Unknown focus area: {focus_area}")

    # Try to load external prompt first
    external_prompt = load_prompt(focus_area)

    if external_prompt:
        prompt = external_prompt
        logger.info(f"Using external prompt for {focus_area}")
    else:
        # Fall back to inline template
        area_config = FOCUS_AREAS[focus_area]
        prompt = DISCOVERY_PROMPT_TEMPLATE.format(
            focus_area=focus_area,
            focus_area_name=area_config["name"],
            evaluation_criteria=area_config["evaluation_criteria"],
        )
        logger.info(f"Using inline template for {focus_area}")

    logger.info(f"Analyzing focus area: {focus_area}")

    # Call Grok API with retry logic
    content = call_grok_with_retry(prompt)
    if not content:
        logger.error(f"Failed to get response for {focus_area}")
        return None

    try:
        # Try to extract JSON from response
        if content.startswith("["):
            trends = json.loads(content)
        else:
            # Try to find JSON array in response
            start = content.find("[")
            end = content.rfind("]") + 1
            if start != -1 and end > start:
                trends = json.loads(content[start:end])
            else:
                logger.warning(f"No JSON array found in response for {focus_area}")
                return None

        # Validate and filter trends
        valid_trends = []
        for trend in trends:
            if validate_trend(trend):
                trend["focus_area"] = focus_area
                trend["timestamp"] = datetime.now(timezone.utc).isoformat()
                # Ensure arrays exist
                trend.setdefault("signal_evidence", [])
                trend.setdefault("noise_indicators", [])
                valid_trends.append(trend)
            else:
                logger.warning(f"Invalid trend skipped: {trend.get('tool_name', 'unknown')}")

        logger.info(f"Found {len(valid_trends)} valid trends for {focus_area}")
        return valid_trends

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for {focus_area}: {e}")
        return None


def run_full_analysis() -> dict:
    """
    Run analysis for all focus areas.

    Returns dict with radar_date and trends list.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    all_trends = []

    logger.info(f"Starting full radar analysis for {today}")

    for focus_area in FOCUS_AREAS:
        trends = analyze_focus_area(focus_area)
        if trends:
            all_trends.extend(trends)

    logger.info(f"Analysis complete: {len(all_trends)} total trends discovered")

    return {
        "radar_date": today,
        "trends": all_trends,
    }


def check_api_connection() -> dict:
    """
    Check if the Grok API connection is working.

    Returns dict with status, provider, and message.
    """
    model = get_model_name()
    provider = "sap_genai_hub" if is_sap_configured() else "litellm_proxy"

    try:
        # Configure API parameters based on provider
        api_params = {
            "model": model,
            "messages": [{"role": "user", "content": "Say 'OK' if you can hear me."}],
            "max_tokens": 10,
        }

        if not is_sap_configured():
            api_params["api_base"] = LITELLM_BASE_URL
            api_params["api_key"] = LITELLM_API_KEY

        response = litellm.completion(**api_params)

        return {
            "status": "ok",
            "message": "Grok API connection successful",
            "provider": provider,
            "model": GROK_MODEL,
            "litellm_base_url": LITELLM_BASE_URL if not is_sap_configured() else None,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Grok API connection failed: {str(e)}",
            "provider": provider,
            "litellm_base_url": LITELLM_BASE_URL if not is_sap_configured() else None,
        }
