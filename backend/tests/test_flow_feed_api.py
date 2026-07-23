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


def test_flow_feed_api_response(api_client):
    client, test_session = api_client

    now = datetime.now(timezone.utc)

    with test_session() as db:
        db.add_all([
            Flow(
                id=1,
                title="국내 증시 상승 흐름",
                target_asset="^KS11",
                summary="국내 증시 상승",
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
        "/api/flows",
        params={
            "limit": 1,
            "offset": 0,
            "sort": "latest",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["total"] == 2
    assert body["limit"] == 1
    assert body["offset"] == 0
    assert len(body["flows"]) == 1

    flow = body["flows"][0]

    assert flow["flow_id"] == 2
    assert flow["score"] == 0.0
    assert flow["evidence_count"] == 0
    assert flow["link_count"] == 0


def test_flow_feed_api_empty_response(
    api_client,
):
    client, _ = api_client

    response = client.get("/api/flows")

    assert response.status_code == 200
    assert response.json() == {
        "total": 0,
        "limit": 20,
        "offset": 0,
        "flows": [],
    }


def test_flow_feed_api_validation(api_client):
    client, _ = api_client

    invalid_limit = client.get(
        "/api/flows",
        params={"limit": 0},
    )
    invalid_sort = client.get(
        "/api/flows",
        params={"sort": "wrong"},
    )
    invalid_dates = client.get(
        "/api/flows",
        params={
            "from_date": "2026-07-22",
            "to_date": "2026-07-21",
        },
    )

    assert invalid_limit.status_code == 422
    assert invalid_sort.status_code == 422
    assert invalid_dates.status_code == 422

    assert invalid_dates.json() == {
        "detail": (
            "from_date는 to_date보다 "
            "늦을 수 없습니다."
        )
    }