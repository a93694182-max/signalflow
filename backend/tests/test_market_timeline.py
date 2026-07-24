from datetime import date, datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Evidence, Flow, FlowLink, FlowNode
from app.services.market_timeline_service import (
    get_market_timeline,
)


def create_timeline_flow(
    flow_id: int,
    title: str,
    target_asset: str,
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
        occurred_at=created_at,
        evidence_level="strong",
    )

    evidence = Evidence(
        id=flow_id,
        evidence_type="market_data",
        title=f"{title} 근거",
        source="test",
        url=f"https://example.com/{flow_id}",
        relation_score=0.9,
        impact_score=0.8,
        time_score=1.0,
        reliability_score=0.9,
    )

    node.evidences.append(evidence)
    flow.nodes.append(node)

    return flow


def test_market_timeline_returns_recent_flows_in_time_order():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    now = datetime.now(timezone.utc)

    flows = [
        create_timeline_flow(
            flow_id=1,
            title="과거 Flow",
            target_asset="^KS11",
            created_at=now - timedelta(hours=2),
        ),
        create_timeline_flow(
            flow_id=2,
            title="중간 Flow",
            target_asset="^KS11",
            created_at=now - timedelta(hours=1),
        ),
        create_timeline_flow(
            flow_id=3,
            title="최신 Flow",
            target_asset="^KS11",
            created_at=now,
        ),
    ]

    with Session(engine) as db:
        db.add_all(flows)
        db.commit()

        result = get_market_timeline(
            db=db,
            limit=2,
            target_asset="^KS11",
        )

    assert result["total"] == 3
    assert result["limit"] == 2
    assert result["target_asset"] == "^KS11"

    # 최근 2개를 시간 오름차순으로 반환
    assert [
        item["flow_id"]
        for item in result["timeline"]
    ] == [2, 3]

    assert all(
        item["target_asset"] == "^KS11"
        for item in result["timeline"]
    )

    assert result["timeline"][0]["evidence_count"] == 1
    assert len(result["timeline"][0]["evidences"]) == 1


def test_market_timeline_includes_external_causes():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    now = datetime.now(timezone.utc)

    news_flow = create_timeline_flow(
        flow_id=1,
        title="금리 인상 뉴스",
        target_asset="MARKET",
        created_at=now - timedelta(hours=1),
    )

    market_flow = create_timeline_flow(
        flow_id=2,
        title="코스피 하락",
        target_asset="^KS11",
        created_at=now,
    )

    link = FlowLink(
        source_flow=news_flow,
        target_flow=market_flow,
        relation_type="potential_cause",
        score=0.9,
        reason="금리 인상 우려가 증시에 영향을 줌",
    )

    with Session(engine) as db:
        db.add_all([
            news_flow,
            market_flow,
            link,
        ])
        db.commit()

        result = get_market_timeline(
            db=db,
            limit=20,
            target_asset="^KS11",
            include_causes=True,
        )

    assert result["total"] == 1

    item = result["timeline"][0]

    assert item["flow_id"] == 2
    assert len(item["causes"]) == 1

    cause = item["causes"][0]

    assert cause["flow_id"] == 1
    assert cause["title"] == "금리 인상 뉴스"
    assert cause["relation_type"] == "potential_cause"
    assert cause["score"] == 0.9


def test_market_timeline_can_exclude_causes():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    now = datetime.now(timezone.utc)

    news_flow = create_timeline_flow(
        flow_id=1,
        title="뉴스 Flow",
        target_asset="MARKET",
        created_at=now - timedelta(hours=1),
    )

    market_flow = create_timeline_flow(
        flow_id=2,
        title="시장 Flow",
        target_asset="^KS11",
        created_at=now,
    )

    link = FlowLink(
        source_flow=news_flow,
        target_flow=market_flow,
        relation_type="potential_cause",
        score=0.8,
        reason="테스트 원인",
    )

    with Session(engine) as db:
        db.add_all([
            news_flow,
            market_flow,
            link,
        ])
        db.commit()

        result = get_market_timeline(
            db=db,
            limit=20,
            target_asset="^KS11",
            include_causes=False,
        )

    assert result["timeline"][0]["causes"] == []


def test_market_timeline_rejects_invalid_date_range():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    with Session(engine) as db:
        with pytest.raises(HTTPException) as error:
            get_market_timeline(
                db=db,
                limit=20,
                from_date=date(2026, 7, 24),
                to_date=date(2026, 7, 23),
            )

    assert error.value.status_code == 422
    assert (
        error.value.detail
        == "from_date는 to_date보다 늦을 수 없습니다."
    )