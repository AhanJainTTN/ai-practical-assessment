from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.comments.models import Comment  # noqa: F401 — register SQLAlchemy mapper
from app.core.database import Base, get_db
from app.tickets.models import Ticket  # noqa: F401 — register SQLAlchemy mapper
from app.users.models import User  # noqa: F401 — register SQLAlchemy mapper
from main import create_app

TEST_DATABASE_URL = "sqlite://"


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    app = create_app()

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def seed_users(db_session: Session) -> dict[str, User]:
    requester = User(name="Alice", email="alice@example.com", role="requester")
    agent = User(name="Bob", email="bob@example.com", role="agent")
    db_session.add_all([requester, agent])
    db_session.commit()
    db_session.refresh(requester)
    db_session.refresh(agent)
    return {"requester": requester, "agent": agent}
