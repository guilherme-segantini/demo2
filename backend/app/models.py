"""SQLite ORM models for CodeScale Research Radar."""

from sqlalchemy import Column, Integer, String, Boolean, Text, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Trend(Base):
    """Model for storing radar trend analyses."""

    __tablename__ = "trends"
    __table_args__ = (
        UniqueConstraint("radar_date", "focus_area", "tool_name", name="uq_trend_date_area_tool"),
        CheckConstraint("classification IN ('signal', 'noise')", name="ck_classification_valid"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    radar_date = Column(String, nullable=False)
    focus_area = Column(String, nullable=False)
    tool_name = Column(String, nullable=False)
    classification = Column(String, nullable=False)  # 'signal' or 'noise'
    confidence_score = Column(Integer, nullable=False)
    technical_insight = Column(Text, nullable=False)
    signal_evidence = Column(Text)  # JSON array as TEXT
    noise_indicators = Column(Text)  # JSON array as TEXT
    architectural_verdict = Column(Boolean, nullable=False)
    timestamp = Column(String, nullable=False)  # ISO 8601

    def to_dict(self):
        """Convert model to dictionary for JSON serialization."""
        import json

        return {
            "focus_area": self.focus_area,
            "tool_name": self.tool_name,
            "classification": self.classification,
            "confidence_score": self.confidence_score,
            "technical_insight": self.technical_insight,
            "signal_evidence": json.loads(self.signal_evidence) if self.signal_evidence else [],
            "noise_indicators": json.loads(self.noise_indicators) if self.noise_indicators else [],
            "architectural_verdict": self.architectural_verdict,
            "timestamp": self.timestamp,
        }
