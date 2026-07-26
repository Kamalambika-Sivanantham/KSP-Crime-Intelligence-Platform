import uuid
from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base


class District(Base):
    __tablename__ = "districts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    population = Column(Integer, nullable=True)
    literacy_rate = Column(Float, nullable=True)
    urbanization_rate = Column(Float, nullable=True)
    avg_income = Column(Float, nullable=True)
    geo_boundary = Column(JSONB, nullable=True)  # GeoJSON polygon
    centroid_lat = Column(Float, nullable=True)
    centroid_lng = Column(Float, nullable=True)

    police_stations = relationship("PoliceStation", back_populates="district")
    users = relationship("User", back_populates="district")


class PoliceStation(Base):
    __tablename__ = "police_stations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    code = Column(String(30), unique=True, nullable=False)
    district_id = Column(UUID(as_uuid=True), ForeignKey("districts.id"), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    address = Column(String(255))

    district = relationship("District", back_populates="police_stations")
    users = relationship("User", back_populates="police_station")
