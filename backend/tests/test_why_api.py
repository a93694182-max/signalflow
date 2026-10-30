import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import patch
from app.database import Base, get_db
from app.main import app
from app.models import Evidence, Flow, FlowNode


@pytest.fixture
def api_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    test_session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)

    def override_get_db():
        with test_session() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    yield client, test_session

    client.close()

    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)
    engine.dispose()


def test_why_api_explanation_response(api_client):
    client, test_session = api_client

    flow = Flow(
        id=1,
        title="국내 증시 하락 흐름",
        target_asset="^KS11",
        summary="국내 증시 하락",
    )

    node = FlowNode(
        id=1,
        order_index=1,
        title="금리 상승",
        category="market",
        evidence_level="strong",
    )

    evidence = Evidence(
        id=1,
        evidence_type="news",
        title="금리 상승 뉴스",
        source="Reuters",
        relation_score=0.9,
        impact_score=0.8,
        time_score=1.0,
        reliability_score=0.95,
    )

    node.evidences.append(evidence)
    flow.nodes.append(node)

    with test_session() as db:
        db.add(flow)
        db.commit()

    response = client.get("/api/flows/1/why")

    assert response.status_code == 200

    body = response.json()

    assert body["flow_id"] == 1
    assert body["primary_cause"]["node_id"] == 1

    assert len(body["evidence_breakdowns"]) == 1

    breakdown = body["evidence_breakdowns"][0]

    assert breakdown["evidence_id"] == 1
    assert breakdown["title"] == "금리 상승 뉴스"
    assert breakdown["scores"]["relation"] == 0.9
    assert breakdown["weights"]["relation"] == 0.3
    assert breakdown["total_score"] == 0.915

    confidence = body["confidence_breakdown"]

    assert confidence["evidence_count"] == 1
    assert confidence["confidence_cap"] == 0.59
    assert confidence["confidence_score"] == body["confidence_score"]
    assert confidence["confidence_level"] == body["confidence_level"]

    ranking = body["cause_ranking"]

    assert len(ranking) == 1
    assert ranking[0]["rank"] == 1
    assert ranking[0]["node_id"] == 1
    assert ranking[0]["evidence_count"] == 1


def test_why_api_empty_evidence(api_client):
    client, test_session = api_client

    flow = Flow(
        id=2,
        title="근거 없는 흐름",
        target_asset="^KS11",
        summary="근거 없음",
    )

    with test_session() as db:
        db.add(flow)
        db.commit()

    response = client.get("/api/flows/2/why")

    assert response.status_code == 200

    body = response.json()

    assert body["primary_cause"] is None
    assert body["evidence_breakdowns"] == []
    assert body["confidence_breakdown"]["evidence_count"] == 0
    assert body["confidence_breakdown"]["confidence_score"] == 0.0
    assert body["cause_ranking"] == []