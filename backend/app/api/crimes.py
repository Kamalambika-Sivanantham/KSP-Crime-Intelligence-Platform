import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.crime import Crime, CrimeStatus, CrimeCategory, CrimeTimeline
from app.models.user import User, RoleEnum
from app.schemas.crime import CrimeCreate, CrimeUpdate, CrimeOut, CrimeListResponse
from app.api.deps import get_current_user, require_roles
from app.ml.risk_score import risk_model

router = APIRouter(prefix="/crimes", tags=["Crimes"])

WRITE_ROLES = (RoleEnum.SUPER_ADMIN, RoleEnum.SCRB_OFFICER, RoleEnum.DISTRICT_SP,
               RoleEnum.POLICE_INSPECTOR, RoleEnum.INVESTIGATION_OFFICER)


@router.get("", response_model=CrimeListResponse)
def list_crimes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    district_id: uuid.UUID | None = None,
    category: CrimeCategory | None = None,
    status: CrimeStatus | None = None,
):
    q = db.query(Crime)
    if district_id:
        q = q.filter(Crime.district_id == district_id)
    if category:
        q = q.filter(Crime.category == category)
    if status:
        q = q.filter(Crime.status == status)
    total = q.count()
    items = q.order_by(Crime.reported_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return CrimeListResponse(total=total, page=page, page_size=page_size, items=items)


@router.get("/{crime_id}", response_model=CrimeOut)
def get_crime(crime_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    crime = db.query(Crime).filter(Crime.id == crime_id).first()
    if not crime:
        raise HTTPException(status_code=404, detail="Crime not found")
    return crime


@router.post("", response_model=CrimeOut, dependencies=[Depends(require_roles(*WRITE_ROLES))])
def create_crime(payload: CrimeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if db.query(Crime).filter(Crime.fir_number == payload.fir_number).first():
        raise HTTPException(status_code=400, detail="FIR number already exists")
    crime_count = db.query(Crime).count()

    violent_categories = [
        CrimeCategory.HOMICIDE,
        CrimeCategory.ASSAULT,
        CrimeCategory.KIDNAPPING,
    ]

    features = {
        "crimes_last_30d": crime_count + 1,
        "crimes_last_90d": (crime_count * 2) + 5,

        "violent_crime_ratio": 1.0 if payload.category in violent_categories else 0.2,

        "repeat_offender_count": len(payload.description or "") % 10,

        "population_density": int(abs(payload.lat * 10)) % 100,

        "avg_response_time_min": int(abs(payload.lng)) % 30,
    }

    prediction = risk_model.predict(features)

    crime = Crime(
    **payload.model_dump(),
    created_by=current_user.id,
    risk_score=prediction["risk_score"]
    )
    db.add(crime)
    db.commit()
    db.refresh(crime)
    db.add(CrimeTimeline(crime_id=crime.id, event="Crime reported", actor_id=current_user.id))
    db.commit()
    return crime


@router.put("/{crime_id}", response_model=CrimeOut, dependencies=[Depends(require_roles(*WRITE_ROLES))])
def update_crime(crime_id: uuid.UUID, payload: CrimeUpdate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    crime = db.query(Crime).filter(Crime.id == crime_id).first()
    if not crime:
        raise HTTPException(status_code=404, detail="Crime not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(crime, field, value)
    db.add(CrimeTimeline(crime_id=crime.id, event=f"Crime updated: {list(payload.model_dump(exclude_unset=True).keys())}",
                          actor_id=current_user.id))
    db.commit()
    db.refresh(crime)
    return crime


@router.delete("/{crime_id}", dependencies=[Depends(require_roles(RoleEnum.SUPER_ADMIN, RoleEnum.SCRB_OFFICER))])
def delete_crime(crime_id: uuid.UUID, db: Session = Depends(get_db)):
    crime = db.query(Crime).filter(Crime.id == crime_id).first()
    if not crime:
        raise HTTPException(status_code=404, detail="Crime not found")
    db.delete(crime)
    db.commit()
    return {"detail": "Crime deleted"}
