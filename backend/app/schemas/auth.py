import uuid
from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserOut(BaseModel):
    id: uuid.UUID
    badge_number: str
    full_name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    badge_number: str
    full_name: str
    email: EmailStr
    password: str
    role: RoleEnum
    district_id: uuid.UUID | None = None
    police_station_id: uuid.UUID | None = None
