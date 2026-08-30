from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from .models import ControlStatus, TrustCategory


class ControlBase(BaseModel):
    name: str
    description: str = ""
    category: TrustCategory = TrustCategory.security
    status: ControlStatus = ControlStatus.not_started
    owner: str = ""
    evidence_url: str = ""


class ControlCreate(ControlBase):
    pass


class ControlUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[TrustCategory] = None
    status: Optional[ControlStatus] = None
    owner: Optional[str] = None
    evidence_url: Optional[str] = None


class ControlOut(ControlBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_reviewed: datetime


class SummaryOut(BaseModel):
    total: int
    not_started: int
    in_progress: int
    implemented: int
    verified: int
    percent_complete: float
