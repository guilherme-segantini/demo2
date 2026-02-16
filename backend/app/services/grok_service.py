"""Grok/LiteLLM service for AI-powered radar analysis."""

import json
import logging
import os
import time
from datetime import datetime, timezone
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

    Returns response content string or None if all retries fail.
    """
    backoff = INITIAL_BACKOFF

    for attempt in range(MAX_RETRIES):
        try:
            # Use openai/ prefix to route through LiteLLM proxy
            response = litellm.completion(
                model=f"openai/{GROK_MODEL}",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                api_base=LITELLM_BASE_URL,
                api_key=LITELLM_API_KEY,
            )
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

    Returns list of trend dictionaries or None if analysis fails.
    """
    if focus_area not in FOCUS_AREAS:
        raise ValueError(f"Unknown focus area: {focus_area}")

    area_config = FOCUS_AREAS[focus_area]
    prompt = DISCOVERY_PROMPT_TEMPLATE.format(
        focus_area=focus_area,
        focus_area_name=area_config["name"],
        evaluation_criteria=area_config["evaluation_criteria"],
    )

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

    Returns dict with status and message.
    """
    try:
        # Use openai/ prefix to route through LiteLLM proxy
        response = litellm.completion(
            model=f"openai/{GROK_MODEL}",
            messages=[{"role": "user", "content": "Say 'OK' if you can hear me."}],
            max_tokens=10,
            api_base=LITELLM_BASE_URL,
            api_key=LITELLM_API_KEY,
        )
        return {
            "status": "ok",
            "message": "Grok API connection successful",
            "model": GROK_MODEL,
            "litellm_base_url": LITELLM_BASE_URL,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Grok API connection failed: {str(e)}",
            "litellm_base_url": LITELLM_BASE_URL,
        }
