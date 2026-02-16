"""API endpoints for radar data."""

import json
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models import Trend

router = APIRouter(prefix="/api", tags=["radar"])


class TrendResponse(BaseModel):
    """Response model for a single trend."""

    focus_area: str
    tool_name: str
    classification: str
    confidence_score: int
    technical_insight: str
    signal_evidence: list[str]
    noise_indicators: list[str]
    architectural_verdict: bool
    timestamp: str


class RadarResponse(BaseModel):
    """Response model for radar data."""

    radar_date: str
    trends: list[TrendResponse]


@router.get("/radar", response_model=RadarResponse)
def get_radar(
    date_param: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get radar analysis for a specific date.

    If no date provided, returns the latest available data.
    """
    if date_param:
        query_date = date_param
    else:
        # Get the most recent radar date
        latest = db.query(Trend.radar_date).order_by(Trend.radar_date.desc()).first()
        if not latest:
            # Return empty response if no data
            return RadarResponse(radar_date=str(date.today()), trends=[])
        query_date = latest[0]

    trends = db.query(Trend).filter(Trend.radar_date == query_date).all()

    return RadarResponse(
        radar_date=query_date,
        trends=[
            TrendResponse(
                focus_area=t.focus_area,
                tool_name=t.tool_name,
                classification=t.classification,
                confidence_score=t.confidence_score,
                technical_insight=t.technical_insight,
                signal_evidence=json.loads(t.signal_evidence) if t.signal_evidence else [],
                noise_indicators=json.loads(t.noise_indicators) if t.noise_indicators else [],
                architectural_verdict=t.architectural_verdict,
                timestamp=t.timestamp,
            )
            for t in trends
        ],
    )


class RefreshResponse(BaseModel):
    """Response model for refresh operation."""

    status: str
    radar_date: str
    trends_count: int
    message: str


@router.post("/radar/refresh", response_model=RefreshResponse)
def refresh_radar(db: Session = Depends(get_db)):
    """
    Manually trigger a new radar analysis using Grok.

    This endpoint calls the Grok API to discover and classify
    tools across all focus areas, then persists results to SQLite.
    """
    from app.services.grok_service import run_full_analysis

    try:
        # Run analysis
        result = run_full_analysis()
        radar_date = result["radar_date"]
        trends = result["trends"]

        if not trends:
            return RefreshResponse(
                status="warning",
                radar_date=radar_date,
                trends_count=0,
                message="Analysis completed but no trends discovered. Check API key configuration.",
            )

        # Delete existing data for today (replace with fresh analysis)
        db.query(Trend).filter(Trend.radar_date == radar_date).delete()

        # Insert new trends
        for trend_data in trends:
            trend = Trend(
                radar_date=radar_date,
                focus_area=trend_data["focus_area"],
                tool_name=trend_data["tool_name"],
                classification=trend_data["classification"],
                confidence_score=trend_data["confidence_score"],
                technical_insight=trend_data["technical_insight"],
                signal_evidence=json.dumps(trend_data.get("signal_evidence", [])),
                noise_indicators=json.dumps(trend_data.get("noise_indicators", [])),
                architectural_verdict=trend_data["architectural_verdict"],
                timestamp=trend_data["timestamp"],
            )
            db.add(trend)

        db.commit()

        return RefreshResponse(
            status="success",
            radar_date=radar_date,
            trends_count=len(trends),
            message=f"Successfully analyzed and stored {len(trends)} trends.",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to refresh radar data: {str(e)}",
        )


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@router.get("/health/grok")
def grok_health_check():
    """Check Grok API connection status."""
    from app.services.grok_service import check_api_connection

    return check_api_connection()
