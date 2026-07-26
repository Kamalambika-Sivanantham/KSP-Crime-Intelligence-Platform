import sys
import os
import pytest
from sqlalchemy.orm import Session

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.core.database import Base, engine, SessionLocal
import app.models  # noqa: F401


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
