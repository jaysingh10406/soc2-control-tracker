import enum
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from .database import Base


class ControlStatus(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    implemented = "implemented"
    verified = "verified"


class TrustCategory(str, enum.Enum):
    security = "security"
    availability = "availability"
    confidentiality = "confidentiality"
    processing_integrity = "processing_integrity"
    privacy = "privacy"


class Control(Base):
    __tablename__ = "controls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, default="")
    category = Column(Enum(TrustCategory), default=TrustCategory.security, nullable=False)
    status = Column(Enum(ControlStatus), default=ControlStatus.not_started, nullable=False)
    owner = Column(String(120), default="")
    evidence_url = Column(String(500), default="")
    last_reviewed = Column(DateTime, default=lambda: datetime.now(timezone.utc))
