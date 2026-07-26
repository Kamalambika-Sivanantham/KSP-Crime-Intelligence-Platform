import uuid
import datetime
from pydantic import BaseModel
from typing import Optional
from app.models.crime import CrimeStatus, CrimeCategory


class CrimeCreate(BaseModel):
    fir_number: str
    category: CrimeCategory
    description: Optional[str] = None
    modus_operandi: Optional[str] = None
    lat: float
    lng: float
    address: Optional[str] = None
    district_id: uuid.UUID
    police_station_id: uuid.UUID
    reported_at: datetime.datetime
    occurred_at: Optional[datetime.datetime] = None


class CrimeUpdate(BaseModel):
    status: Optional[CrimeStatus] = None
    description: Optional[str] = None
    modus_operandi: Optional[str] = None
    assigned_officer_id: Optional[uuid.UUID] = None
    risk_score: Optional[float] = None


class CrimeOut(BaseModel):
    id: uuid.UUID
    fir_number: str
    category: CrimeCategory
    status: CrimeStatus
    description: Optional[str]
    lat: float
    lng: float
    address: Optional[str]
    district_id: uuid.UUID
    police_station_id: uuid.UUID
    reported_at: datetime.datetime
    risk_score: Optional[float]

    class Config:
        from_attributes = True


class CrimeListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[CrimeOut]
