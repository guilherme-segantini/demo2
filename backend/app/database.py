"""Database connection and session management."""

import json
import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

from app.models import Base, Trend

load_dotenv()

DATABASE_URL = os.getenv("RADAR_DATABASE_URL", "sqlite:///./radar.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Mock data from PRD (6 items)
SEED_DATA = [
    {
        "radar_date": "2026-01-30",
        "focus_area": "voice_ai_ux",
        "tool_name": "LiveKit Agents",
        "classification": "signal",
        "confidence_score": 92,
        "technical_insight": "Sub-200ms voice-to-voice latency with WebRTC. Supports interruption handling via VAD (Voice Activity Detection). Native Python SDK with async streaming. Published benchmarks show P95 latency <250ms.",
        "signal_evidence": [
            "Published latency benchmarks",
            "Production usage at scale (Daily.co integration)",
            "Open-source with active technical community",
        ],
        "noise_indicators": [],
        "architectural_verdict": True,
        "timestamp": "2026-01-30T08:00:00Z",
    },
    {
        "radar_date": "2026-01-30",
        "focus_area": "voice_ai_ux",
        "tool_name": "VoiceHype AI",
        "classification": "noise",
        "confidence_score": 85,
        "technical_insight": "Claims 'revolutionary conversational AI' but provides no latency benchmarks. Demo video only, no SDK or architecture documentation available.",
        "signal_evidence": [],
        "noise_indicators": [
            "No published benchmarks",
            "Marketing language ('revolutionary', 'human-like')",
            "Demo-only, no production evidence",
        ],
        "architectural_verdict": False,
        "timestamp": "2026-01-30T08:00:00Z",
    },
    {
        "radar_date": "2026-01-30",
        "focus_area": "agent_orchestration",
        "tool_name": "LangGraph",
        "classification": "signal",
        "confidence_score": 87,
        "technical_insight": "Graph-based agent orchestration with built-in state persistence. Supports cyclic workflows and human-in-the-loop patterns. Native integration with LangChain tools. Checkpoint API enables workflow recovery.",
        "signal_evidence": [
            "Detailed architecture documentation",
            "Production case studies (multiple enterprises)",
            "Active GitHub with technical discussions",
        ],
        "noise_indicators": [],
        "architectural_verdict": True,
        "timestamp": "2026-01-30T08:00:00Z",
    },
    {
        "radar_date": "2026-01-30",
        "focus_area": "agent_orchestration",
        "tool_name": "AutoAgent Pro",
        "classification": "noise",
        "confidence_score": 78,
        "technical_insight": "Promises 'fully autonomous agents' but lacks integration documentation. Roadmap-heavy announcements without shipping history.",
        "signal_evidence": [],
        "noise_indicators": [
            "AGI-adjacent marketing claims",
            "No integration specifications",
            "Roadmap announcements without releases",
        ],
        "architectural_verdict": False,
        "timestamp": "2026-01-30T08:00:00Z",
    },
    {
        "radar_date": "2026-01-30",
        "focus_area": "durable_runtime",
        "tool_name": "Temporal.io",
        "classification": "signal",
        "confidence_score": 94,
        "technical_insight": "Workflow durability with automatic retries and state recovery. Cold-start ~50ms for cached workers. Supports long-running workflows (days/weeks) with checkpoint persistence. Published SLAs for cloud offering.",
        "signal_evidence": [
            "Published cold-start benchmarks",
            "SLA documentation for durability guarantees",
            "Enterprise production usage (Netflix, Snap)",
        ],
        "noise_indicators": [],
        "architectural_verdict": True,
        "timestamp": "2026-01-30T08:00:00Z",
    },
    {
        "radar_date": "2026-01-30",
        "focus_area": "durable_runtime",
        "tool_name": "InfiniScale Runtime",
        "classification": "noise",
        "confidence_score": 81,
        "technical_insight": "Claims 'infinite scale with zero cold starts' but provides no benchmark data. Private beta with waitlist, no architecture documentation.",
        "signal_evidence": [],
        "noise_indicators": [
            "Impossible claims ('zero cold starts')",
            "No published benchmarks",
            "Waitlist-only, no technical docs",
        ],
        "architectural_verdict": False,
        "timestamp": "2026-01-30T08:00:00Z",
    },
]


def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)


def seed_db(db: Optional[Session] = None):
    """Seed the database with mock data from PRD (6 items).

    Args:
        db: Optional database session. If not provided, creates a new one.
    """
    close_session = False
    if db is None:
        db = SessionLocal()
        close_session = True

    try:
        for item in SEED_DATA:
            # Check if trend already exists (unique constraint)
            existing = (
                db.query(Trend)
                .filter(
                    Trend.radar_date == item["radar_date"],
                    Trend.focus_area == item["focus_area"],
                    Trend.tool_name == item["tool_name"],
                )
                .first()
            )
            if existing:
                continue

            trend = Trend(
                radar_date=item["radar_date"],
                focus_area=item["focus_area"],
                tool_name=item["tool_name"],
                classification=item["classification"],
                confidence_score=item["confidence_score"],
                technical_insight=item["technical_insight"],
                signal_evidence=json.dumps(item["signal_evidence"]),
                noise_indicators=json.dumps(item["noise_indicators"]),
                architectural_verdict=item["architectural_verdict"],
                timestamp=item["timestamp"],
            )
            db.add(trend)
        db.commit()
    finally:
        if close_session:
            db.close()


def get_db():
    """Dependency for getting database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_trends_by_date(db: Session, radar_date: str) -> list[Trend]:
    """Query trends for a specific date.

    Args:
        db: Database session.
        radar_date: Date in YYYY-MM-DD format.

    Returns:
        List of Trend objects for the given date.
    """
    return db.query(Trend).filter(Trend.radar_date == radar_date).all()


def get_trends_by_focus_area(db: Session, focus_area: str) -> list[Trend]:
    """Query trends for a specific focus area.

    Args:
        db: Database session.
        focus_area: One of 'voice_ai_ux', 'agent_orchestration', 'durable_runtime'.

    Returns:
        List of Trend objects for the given focus area.
    """
    return db.query(Trend).filter(Trend.focus_area == focus_area).all()


def get_trends_by_classification(db: Session, classification: str) -> list[Trend]:
    """Query trends by classification (signal or noise).

    Args:
        db: Database session.
        classification: 'signal' or 'noise'.

    Returns:
        List of Trend objects with the given classification.
    """
    return db.query(Trend).filter(Trend.classification == classification).all()


def get_latest_trends(db: Session) -> list[Trend]:
    """Get trends from the most recent radar date.

    Args:
        db: Database session.

    Returns:
        List of Trend objects from the latest date.
    """
    latest_date = db.query(Trend.radar_date).order_by(Trend.radar_date.desc()).first()
    if latest_date:
        return db.query(Trend).filter(Trend.radar_date == latest_date[0]).all()
    return []


def get_all_trends(db: Session) -> list[Trend]:
    """Get all trends from the database.

    Args:
        db: Database session.

    Returns:
        List of all Trend objects.
    """
    return db.query(Trend).all()
