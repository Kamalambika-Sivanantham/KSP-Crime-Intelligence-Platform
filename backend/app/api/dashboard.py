import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.crime import Crime, CrimeStatus, CrimeCategory
from app.api.deps import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    today = datetime.date.today()
    total = db.query(func.count(Crime.id)).scalar()
    today_count = db.query(func.count(Crime.id)).filter(func.date(Crime.reported_at) == today).scalar()
    under_investigation = db.query(func.count(Crime.id)).filter(Crime.status == CrimeStatus.UNDER_INVESTIGATION).scalar()
    closed = db.query(func.count(Crime.id)).filter(Crime.status == CrimeStatus.CLOSED).scalar()

    by_category = (
        db.query(Crime.category, func.count(Crime.id))
        .group_by(Crime.category).all()
    )
    by_status = (
        db.query(Crime.status, func.count(Crime.id))
        .group_by(Crime.status).all()
    )
    by_district = (
        db.query(Crime.district_id, func.count(Crime.id))
        .group_by(Crime.district_id).order_by(func.count(Crime.id).desc()).limit(10).all()
    )

    thirty_days_ago = today - datetime.timedelta(days=30)
    trend = (
        db.query(func.date(Crime.reported_at).label("day"), func.count(Crime.id))
        .filter(func.date(Crime.reported_at) >= thirty_days_ago)
        .group_by("day").order_by("day").all()
    )

    return {
        "total_crimes": total,
        "todays_incidents": today_count,
        "under_investigation": under_investigation,
        "closed": closed,
        "by_category": [{"category": c.value, "count": n} for c, n in by_category],
        "by_status": [{"status": s.value, "count": n} for s, n in by_status],
        "top_districts": [{"district_id": str(d), "count": n} for d, n in by_district],
        "trend_30_days": [{"date": str(d), "count": n} for d, n in trend],
    }
