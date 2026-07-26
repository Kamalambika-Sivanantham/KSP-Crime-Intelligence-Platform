"""
Seed script for the KSP Crime Intelligence & Analytics Platform.
Run inside the backend container: python scripts/seed.py
Creates: districts, police stations, an admin user + one per role,
sample crimes across Bengaluru/Mysuru/Mangaluru, and a few network edges.
"""
import sys
import os
import random
import datetime
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.user import User, RoleEnum
from app.models.geography import District, PoliceStation
from app.models.crime import Crime, CrimeCategory, CrimeStatus, Relationship

DISTRICTS = [
    {"name": "Bengaluru Urban", "code": "BLR", "population": 9621551, "literacy_rate": 87.7,
     "centroid_lat": 12.9716, "centroid_lng": 77.5946},
    {"name": "Mysuru", "code": "MYS", "population": 3001127, "literacy_rate": 72.6,
     "centroid_lat": 12.2958, "centroid_lng": 76.6394},
    {"name": "Mangaluru (Dakshina Kannada)", "code": "DK", "population": 2089649, "literacy_rate": 88.6,
     "centroid_lat": 12.9141, "centroid_lng": 74.8560},
    {"name": "Belagavi", "code": "BGM", "population": 4779661, "literacy_rate": 73.9,
     "centroid_lat": 15.8497, "centroid_lng": 74.4977},
    {"name": "Kalaburagi", "code": "KLB", "population": 2566326, "literacy_rate": 68.8,
     "centroid_lat": 17.3297, "centroid_lng": 76.8343},
]

CATEGORIES = list(CrimeCategory)
STATUSES = list(CrimeStatus)


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(District).count() > 0:
            print("Database already seeded. Skipping.")
            return

        district_objs = []
        for d in DISTRICTS:
            obj = District(**d)
            db.add(obj)
            district_objs.append(obj)
        db.commit()

        station_objs = []
        for d in district_objs:
            for i in range(1, 4):
                station = PoliceStation(
                    name=f"{d.name} PS-{i}",
                    code=f"{d.code}-PS{i}",
                    district_id=d.id,
                    lat=d.centroid_lat + random.uniform(-0.05, 0.05),
                    lng=d.centroid_lng + random.uniform(-0.05, 0.05),
                    address=f"{d.name} Police Station {i}",
                )
                db.add(station)
                station_objs.append(station)
        db.commit()

        roles = [
            ("SA001", "Super Administrator", "admin@ksp.gov.in", RoleEnum.SUPER_ADMIN),
            ("SCRB001", "SCRB Officer", "scrb@ksp.gov.in", RoleEnum.SCRB_OFFICER),
            ("SP001", "District SP Bengaluru", "sp.blr@ksp.gov.in", RoleEnum.DISTRICT_SP),
            ("PI001", "Inspector Ravi Kumar", "pi.ravi@ksp.gov.in", RoleEnum.POLICE_INSPECTOR),
            ("CA001", "Crime Analyst", "analyst@ksp.gov.in", RoleEnum.CRIME_ANALYST),
            ("IO001", "Investigation Officer", "io@ksp.gov.in", RoleEnum.INVESTIGATION_OFFICER),
            ("RO001", "Read Only Officer", "readonly@ksp.gov.in", RoleEnum.READ_ONLY_OFFICER),
        ]
        for badge, name, email, role in roles:
            db.add(User(
                badge_number=badge, full_name=name, email=email,
                hashed_password=hash_password("Passw0rd!123"),
                role=role, district_id=district_objs[0].id,
            ))
        db.commit()

        crimes = []
        for i in range(300):
            district = random.choice(district_objs)
            stations = [s for s in station_objs if s.district_id == district.id]
            station = random.choice(stations)
            days_ago = random.randint(0, 180)
            crime = Crime(
                fir_number=f"FIR/{district.code}/{2026}/{1000+i}",
                category=random.choice(CATEGORIES),
                status=random.choice(STATUSES),
                description="Sample seeded incident for demo/testing purposes.",
                modus_operandi=random.choice(["Break-in via rear window", "Snatching on two-wheeler",
                                               "Online phishing link", "Armed confrontation", "Unknown"]),
                lat=station.lat + random.uniform(-0.03, 0.03),
                lng=station.lng + random.uniform(-0.03, 0.03),
                address=f"Near {station.name}",
                district_id=district.id,
                police_station_id=station.id,
                reported_at=datetime.datetime.utcnow() - datetime.timedelta(days=days_ago, hours=random.randint(0, 23)),
                risk_score=round(random.uniform(10, 95), 2),
            )
            db.add(crime)
            crimes.append(crime)
        db.commit()

        # Sample network edges for the graph module
        suspect_ids = [f"S{i}" for i in range(1, 15)]
        phone_ids = [f"P{i}" for i in range(1, 10)]
        for _ in range(40):
            db.add(Relationship(
                source_type="suspect", source_id=random.choice(suspect_ids),
                target_type=random.choice(["suspect", "phone", "vehicle"]),
                target_id=random.choice(suspect_ids + phone_ids),
                relationship_type=random.choice(["call", "financial", "travel", "social"]),
                weight=round(random.uniform(0.5, 3.0), 2),
            ))
        db.commit()

        print(f"Seeded {len(district_objs)} districts, {len(station_objs)} stations, "
              f"{len(roles)} users, {len(crimes)} crimes.")
        print("All seeded users share password: Passw0rd!123")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
