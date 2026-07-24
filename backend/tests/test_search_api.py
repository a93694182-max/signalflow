from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Evidence, Flow, FlowNode


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


def test_unified_search_api_response(api_client):
    client, test_session = api_client

    now = datetime.now(timezone.utc)

    flow = Flow(
        id=1,
        title="KOSPI 피 상승 흐름",
        target_asset="^KS11",
        summary="KOSPI 상승",
        created_at=now,
        updated_at=now,
    )

    node = FlowNode(
        id=1,
        order_index=1,
        title="코스피 상승",
        category="domestic_stock",
        occurred_at=now,
        evidence_level="strong",
    )

    evidence = Evidence(
        id=1,
        evidence_type="market_data",
        title="KOSPI 실시간 데이터",
        source="yahoo_finance",
        content_summary="KOSPI 상승 데이터",
        published_at=now,
    )

    node.evidences.append(evidence)
    flow.nodes.append(node)

    with test_session() as db:
        db.add(flow)
        db.commit()

    response = client.get(
        "/api/search",
        params={
            "q": "KOSPI",
            "type": "all",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["query"] == "KOSPI"
    assert body["total"] == 2
    assert body["flow_count"] == 1
    assert body["evidence_count"] == 1
    assert body["flows"][0]["flow_id"] == 1
    assert body["evidences"][0]["flow_id"] == 1


def test_unified_search_api_validation(api_client):
    client, _ = api_client

    missing_query = client.get(
        "/api/search",
    )

    invalid_type = client.get(
        "/api/search",
        params={
            "q": "시장",
            "type": "wrong",
        },
    )

    blank_query = client.get(
        "/api/search",
        params={
            "q": "   ",
        },
    )

    invalid_dates = client.get(
        "/api/search",
        params={
            "q": "시장",
            "from_date": "2026-07-24",
            "to_date": "2026-07-23",
        },
    )

    assert missing_query.status_code == 422
    assert invalid_type.status_code == 422
    assert blank_query.status_code == 422
    assert invalid_dates.status_code == 422