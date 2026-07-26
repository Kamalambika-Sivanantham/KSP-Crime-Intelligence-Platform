import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.crime import Crime, Relationship
from app.api.deps import get_current_user
from app.ml.hotspot import detect_hotspots
from app.ml.risk_score import risk_model
from app.ml import network_analysis

router = APIRouter(prefix="/ai", tags=["AI & Analytics"])


@router.get("/hotspots")
def get_hotspots(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    district_id: uuid.UUID | None = None,
    eps_km: float = Query(0.5, gt=0),
    min_samples: int = Query(5, ge=2),
):
    q = db.query(Crime.id, Crime.lat, Crime.lng)
    if district_id:
        q = q.filter(Crime.district_id == district_id)
    points = [{"id": str(c.id), "lat": c.lat, "lng": c.lng} for c in q.all()]
    return {"hotspots": detect_hotspots(points, eps_km=eps_km, min_samples=min_samples)}


@router.post("/risk-score")
def compute_risk_score(features: dict, current_user=Depends(get_current_user)):
    return risk_model.predict(features)


@router.get("/network")
def get_network(db: Session = Depends(get_db), current_user=Depends(get_current_user), limit: int = Query(500, le=5000)):
    rows = db.query(Relationship).limit(limit).all()
    edges = [
        {
            "source_type": r.source_type, "source_id": r.source_id,
            "target_type": r.target_type, "target_id": r.target_id,
            "relationship_type": r.relationship_type, "weight": r.weight,
        }
        for r in rows
    ]
    return network_analysis.analyze(edges)


@router.get("/network/shortest-path")
def get_shortest_path(source: str, target: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    rows = db.query(Relationship).all()
    edges = [
        {
            "source_type": r.source_type, "source_id": r.source_id,
            "target_type": r.target_type, "target_id": r.target_id,
            "relationship_type": r.relationship_type, "weight": r.weight,
        }
        for r in rows
    ]
    path = network_analysis.shortest_path(edges, source, target)
    if path is None:
        raise HTTPException(status_code=404, detail="No path found between nodes")
    return {"path": path}
class CrimeAnalysisInput(BaseModel):
    description: str


@router.post("/analyze")
def analyze_crime(data: CrimeAnalysisInput):

    text = data.description.lower()

    crime_type = "OTHER"
    risk = 30
    alert = "Low"

    if any(word in text for word in ["murder", "dead", "stab", "knife"]):
        crime_type = "HOMICIDE"
        risk = 95
        alert = "Critical"

    elif any(word in text for word in ["kidnap", "abduct"]):
        crime_type = "KIDNAPPING"
        risk = 90
        alert = "High"

    elif any(word in text for word in ["robbery", "loot", "gun"]):
        crime_type = "ROBBERY"
        risk = 80
        alert = "High"

    elif any(word in text for word in ["cyber", "otp", "phishing", "online"]):
        crime_type = "CYBERCRIME"
        risk = 70
        alert = "Medium"

    elif any(word in text for word in ["fraud", "scam"]):
        crime_type = "FRAUD"
        risk = 60
        alert = "Medium"

    elif any(word in text for word in ["theft", "stolen", "bike"]):
        crime_type = "THEFT"
        risk = 45
        alert = "Low"

    return {
        "crime_type": crime_type,
        "risk_score": risk,
        "alert": alert,
        "recommended_action": [
            "Notify nearby police stations",
            "Collect CCTV footage",
            "Deploy patrol team"
        ]
    }