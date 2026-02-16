"""Tests for radar API endpoints."""

import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db
from app.models import Base, Trend


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Set up test database before each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint():
    """Test root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "CodeScale Research Radar API"
    assert data["version"] == "1.0.0"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_radar_empty():
    """Test radar endpoint returns empty trends when no data."""
    response = client.get("/api/radar")
    assert response.status_code == 200
    data = response.json()
    assert "radar_date" in data
    assert data["trends"] == []


def test_get_radar_with_data():
    """Test radar endpoint returns data when present."""
    # Insert test data
    db = TestingSessionLocal()
    trend = Trend(
        radar_date="2026-01-30",
        focus_area="voice_ai_ux",
        tool_name="TestTool",
        classification="signal",
        confidence_score=85,
        technical_insight="Test insight",
        signal_evidence=json.dumps(["evidence1", "evidence2"]),
        noise_indicators=json.dumps([]),
        architectural_verdict=True,
        timestamp="2026-01-30T08:00:00Z",
    )
    db.add(trend)
    db.commit()
    db.close()

    response = client.get("/api/radar")
    assert response.status_code == 200
    data = response.json()
    assert data["radar_date"] == "2026-01-30"
    assert len(data["trends"]) == 1
    assert data["trends"][0]["tool_name"] == "TestTool"
    assert data["trends"][0]["classification"] == "signal"
    assert data["trends"][0]["signal_evidence"] == ["evidence1", "evidence2"]


def test_get_radar_by_date():
    """Test radar endpoint filters by date parameter."""
    db = TestingSessionLocal()

    # Insert data for two different dates
    trend1 = Trend(
        radar_date="2026-01-30",
        focus_area="voice_ai_ux",
        tool_name="OlderTool",
        classification="noise",
        confidence_score=75,
        technical_insight="Older insight",
        signal_evidence=json.dumps([]),
        noise_indicators=json.dumps(["hype"]),
        architectural_verdict=False,
        timestamp="2026-01-30T08:00:00Z",
    )
    trend2 = Trend(
        radar_date="2026-02-01",
        focus_area="voice_ai_ux",
        tool_name="NewerTool",
        classification="signal",
        confidence_score=90,
        technical_insight="Newer insight",
        signal_evidence=json.dumps(["benchmarks"]),
        noise_indicators=json.dumps([]),
        architectural_verdict=True,
        timestamp="2026-02-01T08:00:00Z",
    )
    db.add(trend1)
    db.add(trend2)
    db.commit()
    db.close()

    # Query older date
    response = client.get("/api/radar?date_param=2026-01-30")
    assert response.status_code == 200
    data = response.json()
    assert data["radar_date"] == "2026-01-30"
    assert len(data["trends"]) == 1
    assert data["trends"][0]["tool_name"] == "OlderTool"

    # Query newer date
    response = client.get("/api/radar?date_param=2026-02-01")
    data = response.json()
    assert data["radar_date"] == "2026-02-01"
    assert data["trends"][0]["tool_name"] == "NewerTool"


def test_response_time():
    """Test API responds within acceptable time (<200ms)."""
    import time

    start = time.time()
    response = client.get("/api/radar")
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 0.2, f"Response took {elapsed:.3f}s, expected <0.2s"


def test_refresh_endpoint_with_mock():
    """Test refresh endpoint with mocked Grok service."""
    from unittest.mock import patch

    mock_result = {
        "radar_date": "2026-02-03",
        "trends": [
            {
                "focus_area": "voice_ai_ux",
                "tool_name": "MockTool",
                "classification": "signal",
                "confidence_score": 88,
                "technical_insight": "Mock insight",
                "signal_evidence": ["mock evidence"],
                "noise_indicators": [],
                "architectural_verdict": True,
                "timestamp": "2026-02-03T12:00:00Z",
            }
        ],
    }

    with patch("app.services.grok_service.run_full_analysis", return_value=mock_result):
        response = client.post("/api/radar/refresh")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["trends_count"] == 1
    assert data["radar_date"] == "2026-02-03"

    # Verify data was persisted
    response = client.get("/api/radar")
    data = response.json()
    assert len(data["trends"]) == 1
    assert data["trends"][0]["tool_name"] == "MockTool"


def test_refresh_endpoint_empty_results():
    """Test refresh endpoint when no trends are discovered."""
    from unittest.mock import patch

    mock_result = {
        "radar_date": "2026-02-03",
        "trends": [],
    }

    with patch("app.services.grok_service.run_full_analysis", return_value=mock_result):
        response = client.post("/api/radar/refresh")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "warning"
    assert data["trends_count"] == 0


def test_refresh_replaces_existing_data():
    """Test that refresh replaces data for the same date."""
    from unittest.mock import patch

    # Insert existing data
    db = TestingSessionLocal()
    trend = Trend(
        radar_date="2026-02-03",
        focus_area="voice_ai_ux",
        tool_name="OldTool",
        classification="noise",
        confidence_score=50,
        technical_insight="Old insight",
        signal_evidence=json.dumps([]),
        noise_indicators=json.dumps(["old"]),
        architectural_verdict=False,
        timestamp="2026-02-03T08:00:00Z",
    )
    db.add(trend)
    db.commit()
    db.close()

    # Refresh with new data
    mock_result = {
        "radar_date": "2026-02-03",
        "trends": [
            {
                "focus_area": "voice_ai_ux",
                "tool_name": "NewTool",
                "classification": "signal",
                "confidence_score": 95,
                "technical_insight": "New insight",
                "signal_evidence": ["new evidence"],
                "noise_indicators": [],
                "architectural_verdict": True,
                "timestamp": "2026-02-03T12:00:00Z",
            }
        ],
    }

    with patch("app.services.grok_service.run_full_analysis", return_value=mock_result):
        response = client.post("/api/radar/refresh")

    assert response.status_code == 200

    # Verify old data was replaced
    response = client.get("/api/radar?date_param=2026-02-03")
    data = response.json()
    assert len(data["trends"]) == 1
    assert data["trends"][0]["tool_name"] == "NewTool"
