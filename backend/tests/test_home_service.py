from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Evidence, Flow, FlowNode
from app.services.home_service import get_home_data


def create_test_flow(
    flow_id: int,
    title: str,
    target_asset: str,
    evidence_score: float,
    created_at: datetime,
) -> Flow:
    flow = Flow(
        id=flow_id,
        title=title,
        target_asset=target_asset,
        summary=f"{title} 요약",
        created_at=created_at,
        updated_at=created_at,
    )

    node = FlowNode(
        id=flow_id,
        order_index=1,
        title=f"{title} 신호",
        category="market",
        description=f"{title} 설명",
        evidence_level="strong",
    )

    evidence = Evidence(
        id=flow_id,
        evidence_type="market_data",
        title=f"{title} 근거",
        source="test",
        relation_score=evidence_score,
        impact_score=evidence_score,
        time_score=evidence_score,
        reliability_score=evidence_score,
    )

    node.evidences.append(evidence)
    flow.nodes.append(node)

    return flow


def test_home_selects_recent_market_flows():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    now = datetime.now(timezone.utc)

    # 뉴스는 점수가 높아도 시장 움직임의 외부 원인 후보이므로 홈에서 제외
    news_flow = create_test_flow(
        flow_id=1,
        title="금리 인상 뉴스 흐름",
        target_asset="MARKET",
        evidence_score=1.0,
        created_at=now,
    )

    # 오래된 Flow가 최신 Flow보다 점수가 높아도 현재 홈에는 노출 x 
    old_market_flow = create_test_flow(
        flow_id=2,
        title="과거 금 가격 상승 흐름",
        target_asset="GC=F",
        evidence_score=1.0,
        created_at=now - timedelta(days=2),
    )

    kospi_flow = create_test_flow(
        flow_id=3,
        title="국내 증시 하락 흐름",
        target_asset="^KS11",
        evidence_score=0.9,
        created_at=now,
    )

    exchange_flow = create_test_flow(
        flow_id=4,
        title="원달러 환율 상승 흐름",
        target_asset="KRW=X",
        evidence_score=0.8,
        created_at=now,
    )

    with Session(engine) as db:
        db.add_all([
            news_flow,
            old_market_flow,
            kospi_flow,
            exchange_flow,
        ])
        db.commit()

        result = get_home_data(db)

    assert result["biggest_why"] is not None
    assert result["biggest_why"]["flow_id"] == 3
    assert result["biggest_why"]["target_asset"] == "^KS11"

    assert len(result["top_whys"]) == 1
    assert result["top_whys"][0]["flow_id"] == 4

    selected_flow_ids = {
        result["biggest_why"]["flow_id"],
        *[
            flow["flow_id"]
            for flow in result["top_whys"]
        ],
    }

    assert 1 not in selected_flow_ids
    assert 2 not in selected_flow_ids

def test_home_returns_empty_response_without_recent_flows():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    old_flow = create_test_flow(
        flow_id=1,
        title="과거 국내 증시 흐름",
        target_asset="^KS11",
        evidence_score=1.0,
        created_at=(
            datetime.now(timezone.utc)
            - timedelta(days=2)
        ),
    )

    with Session(engine) as db:
        db.add(old_flow)
        db.commit()

        result = get_home_data(db)

    assert result == {
        "biggest_why": None,
        "top_whys": [],
    }