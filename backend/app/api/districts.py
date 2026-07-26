from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.geography import District, PoliceStation
from app.api.deps import get_current_user

router = APIRouter(prefix="/districts", tags=["Geography"])


@router.get("")
def list_districts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    districts = db.query(District).all()
    return [
        {
            "id": d.id, "name": d.name, "code": d.code,
            "population": d.population, "literacy_rate": d.literacy_rate,
            "centroid_lat": d.centroid_lat, "centroid_lng": d.centroid_lng,
        }
        for d in districts
    ]


@router.get("/{district_id}/police-stations")
def list_police_stations(district_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    stations = db.query(PoliceStation).filter(PoliceStation.district_id == district_id).all()
    return [
        {"id": s.id, "name": s.name, "code": s.code, "lat": s.lat, "lng": s.lng, "address": s.address}
        for s in stations
    ]
