import uuid
import enum
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class RoleEnum(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    SCRB_OFFICER = "SCRB_OFFICER"
    DISTRICT_SP = "DISTRICT_SP"
    POLICE_INSPECTOR = "POLICE_INSPECTOR"
    CRIME_ANALYST = "CRIME_ANALYST"
    INVESTIGATION_OFFICER = "INVESTIGATION_OFFICER"
    READ_ONLY_OFFICER = "READ_ONLY_OFFICER"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    badge_number = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.READ_ONLY_OFFICER)
    district_id = Column(UUID(as_uuid=True), ForeignKey("districts.id"), nullable=True)
    police_station_id = Column(UUID(as_uuid=True), ForeignKey("police_stations.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    district = relationship("District", back_populates="users")
    police_station = relationship("PoliceStation", back_populates="users")
    login_history = relationship("LoginHistory", back_populates="user")


class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    ip_address = Column(String(64))
    user_agent = Column(String(255))
    success = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="login_history")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100))
    entity_id = Column(String(100))
    details = Column(String(1000))
    ip_address = Column(String(64))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
