from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Flow


@pytest.fixture
def api_client():
    engine = create_engine(
        "sqlite://",
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )

    test_session = sessionmaker(
        bind=engine,
    )

    Base.metadata.create_all(engine)

    def override_get_db():
        with test_session() as db:
            yield db

    app.dependency_overrides[get_db] = (
        override_get_db
    )

    client = TestClient(app)

    yield client, test_session

    client.close()
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)
    engine.dispose()


def test_market_timeline_api_response(api_client):
    client, test_session = api_client

    now = datetime.now(timezone.utc)

    with test_session() as db:
        db.add_all([
            Flow(
                id=1,
                title="코스피 상승 흐름",
                target_asset="^KS11",
                summary="코스피 상승",
                created_at=now,
                updated_at=now,
            ),
            Flow(
                id=2,
                title="비트코인 상승 흐름",
                target_asset="BTC-USD",
                summary="비트코인 상승",
                created_at=now,
                updated_at=now,
            ),
        ])
        db.commit()

    response = client.get(
        "/api/timeline",
        params={
            "target_asset": "^KS11",
            "limit": 20,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["total"] == 1
    assert body["limit"] == 20
    assert body["target_asset"] == "^KS11"
    assert len(body["timeline"]) == 1

    item = body["timeline"][0]

    assert item["flow_id"] == 1
    assert item["target_asset"] == "^KS11"
    assert item["evidence_count"] == 0
    assert item["evidences"] == []
    assert item["causes"] == []


def test_market_timeline_api_validation(api_client):
    client, _ = api_client

    invalid_limit = client.get(
        "/api/timeline",
        params={"limit": 0},
    )

    invalid_dates = client.get(
        "/api/timeline",
        params={
            "from_date": "2026-07-24",
            "to_date": "2026-07-23",
        },
    )

    assert invalid_limit.status_code == 422
    assert invalid_dates.status_code == 422

    assert invalid_dates.json() == {
        "detail": (
            "from_date는 to_date보다 "
            "늦을 수 없습니다."
        )
    }