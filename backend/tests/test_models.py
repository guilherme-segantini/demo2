"""Tests for SQLAlchemy models."""

import json
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models import Base, Trend


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Set up test database before each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestTrendModel:
    """Tests for the Trend model."""

    def test_create_signal_trend(self):
        """Test creating a signal trend."""
        db = TestingSessionLocal()
        trend = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="LiveKit Agents",
            classification="signal",
            confidence_score=92,
            technical_insight="Sub-200ms voice-to-voice latency with WebRTC.",
            signal_evidence=json.dumps(["Published benchmarks", "Production usage"]),
            noise_indicators=json.dumps([]),
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        db.add(trend)
        db.commit()

        saved = db.query(Trend).first()
        assert saved.id is not None
        assert saved.tool_name == "LiveKit Agents"
        assert saved.classification == "signal"
        assert saved.confidence_score == 92
        assert saved.architectural_verdict is True
        db.close()

    def test_create_noise_trend(self):
        """Test creating a noise trend."""
        db = TestingSessionLocal()
        trend = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="VoiceHype AI",
            classification="noise",
            confidence_score=85,
            technical_insight="Claims 'revolutionary' but no benchmarks.",
            signal_evidence=json.dumps([]),
            noise_indicators=json.dumps(["No benchmarks", "Marketing language"]),
            architectural_verdict=False,
            timestamp="2026-01-30T08:00:00Z",
        )
        db.add(trend)
        db.commit()

        saved = db.query(Trend).first()
        assert saved.classification == "noise"
        assert saved.architectural_verdict is False
        db.close()

    def test_to_dict_method(self):
        """Test the to_dict method for JSON serialization."""
        db = TestingSessionLocal()
        trend = Trend(
            radar_date="2026-01-30",
            focus_area="agent_orchestration",
            tool_name="LangGraph",
            classification="signal",
            confidence_score=87,
            technical_insight="Graph-based agent orchestration.",
            signal_evidence=json.dumps(["Architecture docs", "Case studies"]),
            noise_indicators=json.dumps([]),
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        db.add(trend)
        db.commit()

        result = trend.to_dict()
        assert result["focus_area"] == "agent_orchestration"
        assert result["tool_name"] == "LangGraph"
        assert result["classification"] == "signal"
        assert result["confidence_score"] == 87
        assert result["signal_evidence"] == ["Architecture docs", "Case studies"]
        assert result["noise_indicators"] == []
        assert result["architectural_verdict"] is True
        assert result["timestamp"] == "2026-01-30T08:00:00Z"
        db.close()

    def test_to_dict_with_empty_evidence(self):
        """Test to_dict when evidence fields are None."""
        db = TestingSessionLocal()
        trend = Trend(
            radar_date="2026-01-30",
            focus_area="durable_runtime",
            tool_name="TestTool",
            classification="signal",
            confidence_score=75,
            technical_insight="Test insight.",
            signal_evidence=None,
            noise_indicators=None,
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        db.add(trend)
        db.commit()

        result = trend.to_dict()
        assert result["signal_evidence"] == []
        assert result["noise_indicators"] == []
        db.close()

    def test_query_by_focus_area(self):
        """Test querying trends by focus area."""
        db = TestingSessionLocal()

        # Add trends for different focus areas
        areas = ["voice_ai_ux", "agent_orchestration", "durable_runtime"]
        for area in areas:
            trend = Trend(
                radar_date="2026-01-30",
                focus_area=area,
                tool_name=f"Tool for {area}",
                classification="signal",
                confidence_score=80,
                technical_insight="Test insight.",
                signal_evidence=json.dumps([]),
                noise_indicators=json.dumps([]),
                architectural_verdict=True,
                timestamp="2026-01-30T08:00:00Z",
            )
            db.add(trend)
        db.commit()

        # Query specific focus area
        voice_trends = db.query(Trend).filter(Trend.focus_area == "voice_ai_ux").all()
        assert len(voice_trends) == 1
        assert voice_trends[0].focus_area == "voice_ai_ux"
        db.close()

    def test_query_by_date(self):
        """Test querying trends by radar date."""
        db = TestingSessionLocal()

        # Add trends for different dates
        dates = ["2026-01-30", "2026-02-06", "2026-02-13"]
        for date in dates:
            trend = Trend(
                radar_date=date,
                focus_area="voice_ai_ux",
                tool_name=f"Tool for {date}",
                classification="signal",
                confidence_score=80,
                technical_insight="Test insight.",
                signal_evidence=json.dumps([]),
                noise_indicators=json.dumps([]),
                architectural_verdict=True,
                timestamp=f"{date}T08:00:00Z",
            )
            db.add(trend)
        db.commit()

        # Query specific date
        feb_trends = db.query(Trend).filter(Trend.radar_date == "2026-02-06").all()
        assert len(feb_trends) == 1
        assert feb_trends[0].radar_date == "2026-02-06"
        db.close()

    def test_query_by_classification(self):
        """Test querying trends by classification (signal/noise)."""
        db = TestingSessionLocal()

        # Add signal trend
        signal = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="SignalTool",
            classification="signal",
            confidence_score=90,
            technical_insight="Good tool.",
            signal_evidence=json.dumps(["evidence"]),
            noise_indicators=json.dumps([]),
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        # Add noise trend
        noise = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="NoiseTool",
            classification="noise",
            confidence_score=85,
            technical_insight="Hype tool.",
            signal_evidence=json.dumps([]),
            noise_indicators=json.dumps(["hype"]),
            architectural_verdict=False,
            timestamp="2026-01-30T08:00:00Z",
        )
        db.add(signal)
        db.add(noise)
        db.commit()

        signals = db.query(Trend).filter(Trend.classification == "signal").all()
        assert len(signals) == 1
        assert signals[0].tool_name == "SignalTool"

        noises = db.query(Trend).filter(Trend.classification == "noise").all()
        assert len(noises) == 1
        assert noises[0].tool_name == "NoiseTool"
        db.close()

    def test_confidence_score_range(self):
        """Test that confidence scores within valid range work."""
        db = TestingSessionLocal()

        # Test minimum valid score
        trend_min = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="MinScore",
            classification="signal",
            confidence_score=1,
            technical_insight="Minimum confidence.",
            signal_evidence=json.dumps([]),
            noise_indicators=json.dumps([]),
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        db.add(trend_min)

        # Test maximum valid score
        trend_max = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="MaxScore",
            classification="signal",
            confidence_score=100,
            technical_insight="Maximum confidence.",
            signal_evidence=json.dumps([]),
            noise_indicators=json.dumps([]),
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        db.add(trend_max)
        db.commit()

        min_saved = db.query(Trend).filter(Trend.tool_name == "MinScore").first()
        max_saved = db.query(Trend).filter(Trend.tool_name == "MaxScore").first()
        assert min_saved.confidence_score == 1
        assert max_saved.confidence_score == 100
        db.close()


class TestDatabaseInit:
    """Tests for database initialization."""

    def test_init_db_creates_tables(self):
        """Test that init_db creates the trends table."""
        from app.database import init_db, engine as app_engine
        from app.models import Base

        # Create a fresh engine for this test
        test_engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
        )

        # Bind base to test engine
        Base.metadata.create_all(bind=test_engine)

        # Check table exists
        from sqlalchemy import inspect

        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        assert "trends" in tables

    def test_trends_table_has_correct_columns(self):
        """Test that trends table has all required columns."""
        from sqlalchemy import inspect

        inspector = inspect(engine)
        columns = {col["name"] for col in inspector.get_columns("trends")}

        expected_columns = {
            "id",
            "radar_date",
            "focus_area",
            "tool_name",
            "classification",
            "confidence_score",
            "technical_insight",
            "signal_evidence",
            "noise_indicators",
            "architectural_verdict",
            "timestamp",
        }
        assert expected_columns == columns


class TestUniqueConstraint:
    """Tests for the unique constraint on (radar_date, focus_area, tool_name)."""

    def test_unique_constraint_prevents_duplicates(self):
        """Test that duplicate (radar_date, focus_area, tool_name) entries are rejected."""
        from sqlalchemy.exc import IntegrityError

        db = TestingSessionLocal()
        trend1 = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="DuplicateTool",
            classification="signal",
            confidence_score=90,
            technical_insight="First entry.",
            signal_evidence=json.dumps([]),
            noise_indicators=json.dumps([]),
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        db.add(trend1)
        db.commit()

        # Try to add duplicate
        trend2 = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="DuplicateTool",
            classification="noise",
            confidence_score=80,
            technical_insight="Duplicate entry.",
            signal_evidence=json.dumps([]),
            noise_indicators=json.dumps([]),
            architectural_verdict=False,
            timestamp="2026-01-30T09:00:00Z",
        )
        db.add(trend2)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
        db.close()

    def test_same_tool_different_date_allowed(self):
        """Test that same tool on different dates is allowed."""
        db = TestingSessionLocal()
        trend1 = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="SameTool",
            classification="signal",
            confidence_score=90,
            technical_insight="Week 1.",
            signal_evidence=json.dumps([]),
            noise_indicators=json.dumps([]),
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        trend2 = Trend(
            radar_date="2026-02-06",
            focus_area="voice_ai_ux",
            tool_name="SameTool",
            classification="signal",
            confidence_score=92,
            technical_insight="Week 2.",
            signal_evidence=json.dumps([]),
            noise_indicators=json.dumps([]),
            architectural_verdict=True,
            timestamp="2026-02-06T08:00:00Z",
        )
        db.add(trend1)
        db.add(trend2)
        db.commit()

        # Both should be saved
        results = db.query(Trend).filter(Trend.tool_name == "SameTool").all()
        assert len(results) == 2
        db.close()


class TestClassificationConstraint:
    """Tests for the classification check constraint."""

    def test_invalid_classification_rejected(self):
        """Test that invalid classification values are rejected."""
        from sqlalchemy.exc import IntegrityError

        db = TestingSessionLocal()
        trend = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="InvalidTool",
            classification="invalid_value",  # Invalid!
            confidence_score=90,
            technical_insight="Invalid classification.",
            signal_evidence=json.dumps([]),
            noise_indicators=json.dumps([]),
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        db.add(trend)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
        db.close()


class TestSeedDatabase:
    """Tests for the seed_db function."""

    def test_seed_db_creates_6_records(self):
        """Test that seed_db creates exactly 6 records from PRD mock data."""
        from app.database import seed_db, SEED_DATA

        db = TestingSessionLocal()

        # Verify empty database
        assert db.query(Trend).count() == 0

        seed_db(db)

        # Check 6 records created
        assert db.query(Trend).count() == 6
        db.close()

    def test_seed_db_is_idempotent(self):
        """Test that seed_db can be called multiple times without creating duplicates."""
        from app.database import seed_db

        db = TestingSessionLocal()

        seed_db(db)
        assert db.query(Trend).count() == 6

        # Call again - should not create duplicates
        seed_db(db)
        assert db.query(Trend).count() == 6
        db.close()

    def test_seed_db_data_matches_prd(self):
        """Test that seeded data matches the PRD specifications."""
        from app.database import seed_db

        db = TestingSessionLocal()
        seed_db(db)

        # Check for LiveKit Agents (signal)
        livekit = db.query(Trend).filter(Trend.tool_name == "LiveKit Agents").first()
        assert livekit is not None
        assert livekit.classification == "signal"
        assert livekit.confidence_score == 92
        assert livekit.focus_area == "voice_ai_ux"

        # Check for VoiceHype AI (noise)
        voicehype = db.query(Trend).filter(Trend.tool_name == "VoiceHype AI").first()
        assert voicehype is not None
        assert voicehype.classification == "noise"
        assert voicehype.architectural_verdict is False

        # Check for Temporal.io (signal)
        temporal = db.query(Trend).filter(Trend.tool_name == "Temporal.io").first()
        assert temporal is not None
        assert temporal.classification == "signal"
        assert temporal.confidence_score == 94
        assert temporal.focus_area == "durable_runtime"

        db.close()


class TestQueryFunctions:
    """Tests for the database query functions."""

    def test_get_trends_by_date(self):
        """Test get_trends_by_date returns correct trends."""
        from app.database import get_trends_by_date

        db = TestingSessionLocal()

        # Add trends for different dates
        for date in ["2026-01-30", "2026-02-06"]:
            for i in range(2):
                trend = Trend(
                    radar_date=date,
                    focus_area="voice_ai_ux",
                    tool_name=f"Tool {date}-{i}",
                    classification="signal",
                    confidence_score=80,
                    technical_insight="Test.",
                    signal_evidence=json.dumps([]),
                    noise_indicators=json.dumps([]),
                    architectural_verdict=True,
                    timestamp=f"{date}T08:00:00Z",
                )
                db.add(trend)
        db.commit()

        results = get_trends_by_date(db, "2026-01-30")
        assert len(results) == 2
        for trend in results:
            assert trend.radar_date == "2026-01-30"
        db.close()

    def test_get_trends_by_focus_area(self):
        """Test get_trends_by_focus_area returns correct trends."""
        from app.database import get_trends_by_focus_area

        db = TestingSessionLocal()

        # Add trends for different focus areas
        areas = ["voice_ai_ux", "agent_orchestration", "durable_runtime"]
        for area in areas:
            trend = Trend(
                radar_date="2026-01-30",
                focus_area=area,
                tool_name=f"Tool for {area}",
                classification="signal",
                confidence_score=80,
                technical_insight="Test.",
                signal_evidence=json.dumps([]),
                noise_indicators=json.dumps([]),
                architectural_verdict=True,
                timestamp="2026-01-30T08:00:00Z",
            )
            db.add(trend)
        db.commit()

        results = get_trends_by_focus_area(db, "agent_orchestration")
        assert len(results) == 1
        assert results[0].focus_area == "agent_orchestration"
        db.close()

    def test_get_trends_by_classification(self):
        """Test get_trends_by_classification returns correct trends."""
        from app.database import get_trends_by_classification

        db = TestingSessionLocal()

        # Add signals and noise
        for i, cls in enumerate(["signal", "signal", "noise"]):
            trend = Trend(
                radar_date="2026-01-30",
                focus_area="voice_ai_ux",
                tool_name=f"Tool {i}",
                classification=cls,
                confidence_score=80,
                technical_insight="Test.",
                signal_evidence=json.dumps([]),
                noise_indicators=json.dumps([]),
                architectural_verdict=cls == "signal",
                timestamp="2026-01-30T08:00:00Z",
            )
            db.add(trend)
        db.commit()

        signals = get_trends_by_classification(db, "signal")
        assert len(signals) == 2

        noises = get_trends_by_classification(db, "noise")
        assert len(noises) == 1
        db.close()

    def test_get_latest_trends(self):
        """Test get_latest_trends returns trends from most recent date."""
        from app.database import get_latest_trends

        db = TestingSessionLocal()

        # Add trends for different dates
        dates = ["2026-01-30", "2026-02-06", "2026-02-13"]
        for date in dates:
            trend = Trend(
                radar_date=date,
                focus_area="voice_ai_ux",
                tool_name=f"Tool for {date}",
                classification="signal",
                confidence_score=80,
                technical_insight="Test.",
                signal_evidence=json.dumps([]),
                noise_indicators=json.dumps([]),
                architectural_verdict=True,
                timestamp=f"{date}T08:00:00Z",
            )
            db.add(trend)
        db.commit()

        results = get_latest_trends(db)
        assert len(results) == 1
        assert results[0].radar_date == "2026-02-13"
        db.close()

    def test_get_latest_trends_empty_db(self):
        """Test get_latest_trends returns empty list on empty database."""
        from app.database import get_latest_trends

        db = TestingSessionLocal()
        results = get_latest_trends(db)
        assert results == []
        db.close()

    def test_get_all_trends(self):
        """Test get_all_trends returns all records."""
        from app.database import get_all_trends

        db = TestingSessionLocal()

        # Add some trends
        for i in range(5):
            trend = Trend(
                radar_date="2026-01-30",
                focus_area="voice_ai_ux",
                tool_name=f"Tool {i}",
                classification="signal",
                confidence_score=80,
                technical_insight="Test.",
                signal_evidence=json.dumps([]),
                noise_indicators=json.dumps([]),
                architectural_verdict=True,
                timestamp="2026-01-30T08:00:00Z",
            )
            db.add(trend)
        db.commit()

        results = get_all_trends(db)
        assert len(results) == 5
        db.close()
