import uuid
import enum
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class CrimeStatus(str, enum.Enum):
    REPORTED = "REPORTED"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"
    CHARGESHEET_FILED = "CHARGESHEET_FILED"
    CLOSED = "CLOSED"
    COLD_CASE = "COLD_CASE"


class CrimeCategory(str, enum.Enum):
    THEFT = "THEFT"
    ROBBERY = "ROBBERY"
    ASSAULT = "ASSAULT"
    HOMICIDE = "HOMICIDE"
    CYBERCRIME = "CYBERCRIME"
    NARCOTICS = "NARCOTICS"
    KIDNAPPING = "KIDNAPPING"
    FRAUD = "FRAUD"
    DOMESTIC_VIOLENCE = "DOMESTIC_VIOLENCE"
    OTHER = "OTHER"


class Crime(Base):
    __tablename__ = "crimes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fir_number = Column(String(50), unique=True, nullable=False, index=True)
    category = Column(Enum(CrimeCategory), nullable=False, index=True)
    status = Column(Enum(CrimeStatus), default=CrimeStatus.REPORTED, index=True)
    description = Column(Text)
    modus_operandi = Column(Text)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    address = Column(String(255))
    district_id = Column(UUID(as_uuid=True), ForeignKey("districts.id"), nullable=False, index=True)
    police_station_id = Column(UUID(as_uuid=True), ForeignKey("police_stations.id"), nullable=False, index=True)
    assigned_officer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reported_at = Column(DateTime(timezone=True), nullable=False, index=True)
    occurred_at = Column(DateTime(timezone=True), nullable=True)
    risk_score = Column(Float, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    district = relationship("District")
    police_station = relationship("PoliceStation")
    victims = relationship("Victim", back_populates="crime", cascade="all, delete-orphan")
    suspects = relationship("Suspect", back_populates="crime", cascade="all, delete-orphan")
    witnesses = relationship("Witness", back_populates="crime", cascade="all, delete-orphan")
    evidence = relationship("Evidence", back_populates="crime", cascade="all, delete-orphan")
    timeline = relationship("CrimeTimeline", back_populates="crime", cascade="all, delete-orphan")


class Victim(Base):
    __tablename__ = "victims"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crime_id = Column(UUID(as_uuid=True), ForeignKey("crimes.id"), nullable=False)
    name = Column(String(150))
    age = Column(String(10))
    gender = Column(String(20))
    contact = Column(String(50))
    statement = Column(Text)

    crime = relationship("Crime", back_populates="victims")


class Suspect(Base):
    __tablename__ = "suspects"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crime_id = Column(UUID(as_uuid=True), ForeignKey("crimes.id"), nullable=False)
    name = Column(String(150))
    aliases = Column(String(255))
    age = Column(String(10))
    gender = Column(String(20))
    address = Column(String(255))
    face_image_url = Column(String(500))
    fingerprint_ref = Column(String(255))
    is_repeat_offender = Column(String(10), default="false")
    risk_score = Column(Float, nullable=True)

    crime = relationship("Crime", back_populates="suspects")


class Witness(Base):
    __tablename__ = "witnesses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crime_id = Column(UUID(as_uuid=True), ForeignKey("crimes.id"), nullable=False)
    name = Column(String(150))
    contact = Column(String(50))
    statement = Column(Text)

    crime = relationship("Crime", back_populates="witnesses")


class Evidence(Base):
    __tablename__ = "evidence"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crime_id = Column(UUID(as_uuid=True), ForeignKey("crimes.id"), nullable=False)
    file_type = Column(String(30))  # image, video, document
    file_url = Column(String(500), nullable=False)
    description = Column(String(255))
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    crime = relationship("Crime", back_populates="evidence")


class CrimeTimeline(Base):
    __tablename__ = "crime_timeline"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crime_id = Column(UUID(as_uuid=True), ForeignKey("crimes.id"), nullable=False)
    event = Column(String(255), nullable=False)
    notes = Column(Text)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    crime = relationship("Crime", back_populates="timeline")


class Relationship(Base):
    """Edges for the crime network graph: links suspects/victims/vehicles/phones/orgs."""
    __tablename__ = "relationships"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_type = Column(String(50), nullable=False)   # suspect, victim, vehicle, phone, bank_account, location, weapon, organization
    source_id = Column(String(100), nullable=False)
    target_type = Column(String(50), nullable=False)
    target_id = Column(String(100), nullable=False)
    relationship_type = Column(String(50), nullable=False)  # call, financial, travel, social, family
    weight = Column(Float, default=1.0)
    metadata_json = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
