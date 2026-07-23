from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest
from fastapi import HTTPException

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models import (
    Evidence,
    Flow,
    FlowLink,
    FlowNode,
)
from app.services.flow_service import get_flow_feed


def create_test_flow(
    flow_id: int,
    created_at: datetime,
) -> Flow:
    return Flow(
        id=flow_id,
        title=f"Flow {flow_id}",
        target_asset="TEST",
        summary=f"Flow {flow_id} 요약",
        created_at=created_at,
        updated_at=created_at,
    )


def test_flow_feed_pagination():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    now = datetime.now(timezone.utc)

    flows = [
        create_test_flow(
            flow_id=flow_id,
            created_at=now - timedelta(
                hours=5 - flow_id,
            ),
        )
        for flow_id in range(1, 6)
    ]

    with Session(engine) as db:
        db.add_all(flows)
        db.commit()

        first_page = get_flow_feed(
            db=db,
            limit=2,
            offset=0,
        )

        second_page = get_flow_feed(
            db=db,
            limit=2,
            offset=2,
        )

        last_page = get_flow_feed(
            db=db,
            limit=2,
            offset=4,
        )

    assert first_page["total"] == 5
    assert first_page["limit"] == 2
    assert first_page["offset"] == 0
    assert [
        flow["flow_id"]
        for flow in first_page["flows"]
    ] == [5, 4]

    assert [
        flow["flow_id"]
        for flow in second_page["flows"]
    ] == [3, 2]

    assert [
        flow["flow_id"]
        for flow in last_page["flows"]
    ] == [1]



def create_filter_flow(
    flow_id: int,
    title: str,
    target_asset: str,
    created_at: datetime,
) -> Flow:
    return Flow(
        id=flow_id,
        title=title,
        target_asset=target_asset,
        summary=f"{title} 요약",
        created_at=created_at,
        updated_at=created_at,
    )


def test_flow_feed_filters_and_search():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    now = datetime.now(timezone.utc)

    flows = [
        create_filter_flow(
            flow_id=1,
            title="국내 증시 상승 흐름",
            target_asset="^KS11",
            created_at=now,
        ),
        create_filter_flow(
            flow_id=2,
            title="국내 증시 하락 흐름",
            target_asset="^KS11",
            created_at=now,
        ),
        create_filter_flow(
            flow_id=3,
            title="비트코인 상승 흐름",
            target_asset="BTC-USD",
            created_at=now,
        ),
        create_filter_flow(
            flow_id=4,
            title="금리 인상 뉴스 흐름",
            target_asset="MARKET",
            created_at=now,
        ),
    ]

    with Session(engine) as db:
        db.add_all(flows)
        db.commit()

        asset_result = get_flow_feed(
            db=db,
            limit=20,
            offset=0,
            target_asset="^KS11",
        )

        without_news_result = get_flow_feed(
            db=db,
            limit=20,
            offset=0,
            include_news=False,
        )

        search_result = get_flow_feed(
            db=db,
            limit=20,
            offset=0,
            query="상승",
        )

        combined_result = get_flow_feed(
            db=db,
            limit=20,
            offset=0,
            target_asset="^KS11",
            include_news=False,
            query="상승",
        )

    assert asset_result["total"] == 2
    assert {
        flow["target_asset"]
        for flow in asset_result["flows"]
    } == {"^KS11"}

    assert without_news_result["total"] == 3
    assert all(
        flow["target_asset"] != "MARKET"
        for flow in without_news_result["flows"]
    )

    assert search_result["total"] == 2
    assert all(
        "상승" in flow["title"]
        for flow in search_result["flows"]
    )

    assert combined_result["total"] == 1
    assert combined_result["flows"][0]["flow_id"] == 1


def test_flow_feed_date_filter():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    korea_timezone = ZoneInfo("Asia/Seoul")

    flows = [
        create_filter_flow(
            flow_id=1,
            title="7월 20일 Flow",
            target_asset="^KS11",
            created_at=datetime(
                2026, 7, 20, 12, 0,
                tzinfo=korea_timezone,
            ),
        ),
        create_filter_flow(
            flow_id=2,
            title="7월 21일 Flow",
            target_asset="KRW=X",
            created_at=datetime(
                2026, 7, 21, 23, 59,
                tzinfo=korea_timezone,
            ),
        ),
        create_filter_flow(
            flow_id=3,
            title="7월 22일 Flow",
            target_asset="BTC-USD",
            created_at=datetime(
                2026, 7, 22, 0, 0,
                tzinfo=korea_timezone,
            ),
        ),
    ]

    with Session(engine) as db:
        db.add_all(flows)
        db.commit()

        result = get_flow_feed(
            db=db,
            limit=20,
            offset=0,
            from_date=date(2026, 7, 20),
            to_date=date(2026, 7, 21),
        )

    assert result["total"] == 2
    assert {
        flow["flow_id"]
        for flow in result["flows"]
    } == {1, 2}


def test_flow_feed_rejects_invalid_date_range():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    with Session(engine) as db:
        with pytest.raises(HTTPException) as error:
            get_flow_feed(
                db=db,
                limit=20,
                offset=0,
                from_date=date(2026, 7, 22),
                to_date=date(2026, 7, 21),
            )

    assert error.value.status_code == 422
    assert (
        error.value.detail
        == "from_date는 to_date보다 늦을 수 없습니다."
    )



def create_scored_flow(
    flow_id: int,
    title: str,
    score: float,
    created_at: datetime,
) -> Flow:
    flow = Flow(
        id=flow_id,
        title=title,
        target_asset="^KS11",
        summary=f"{title} 요약",
        created_at=created_at,
        updated_at=created_at,
    )

    node = FlowNode(
        id=flow_id,
        order_index=1,
        title=f"{title} 신호",
        category="domestic_stock",
        evidence_level="strong",
    )

    evidence = Evidence(
        id=flow_id,
        evidence_type="market_data",
        title=f"{title} 근거",
        source="test",
        relation_score=score,
        impact_score=score,
        time_score=score,
        reliability_score=score,
    )

    node.evidences.append(evidence)
    flow.nodes.append(node)

    return flow


def test_flow_feed_sorting():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    now = datetime.now(timezone.utc)

    older_high_score_flow = create_scored_flow(
        flow_id=1,
        title="과거 고득점 Flow",
        score=1.0,
        created_at=now - timedelta(days=1),
    )

    newer_low_score_flow = create_scored_flow(
        flow_id=2,
        title="최신 저득점 Flow",
        score=0.4,
        created_at=now,
    )

    with Session(engine) as db:
        db.add_all([
            older_high_score_flow,
            newer_low_score_flow,
        ])
        db.commit()

        latest_result = get_flow_feed(
            db=db,
            limit=20,
            offset=0,
            sort_by="latest",
        )

        score_result = get_flow_feed(
            db=db,
            limit=20,
            offset=0,
            sort_by="score",
        )

    assert [
        flow["flow_id"]
        for flow in latest_result["flows"]
    ] == [2, 1]

    assert [
        flow["flow_id"]
        for flow in score_result["flows"]
    ] == [1, 2]

    assert (
        score_result["flows"][0]["score"]
        > score_result["flows"][1]["score"]
    )


def test_flow_feed_rejects_invalid_sort():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    with Session(engine) as db:
        with pytest.raises(HTTPException) as error:
            get_flow_feed(
                db=db,
                limit=20,
                offset=0,
                sort_by="wrong",
            )

    assert error.value.status_code == 422
    assert (
        error.value.detail
        == "sort는 latest 또는 score만 사용할 수 있습니다."
    )




def test_flow_feed_summary_counts():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    now = datetime.now(timezone.utc)

    news_flow = create_scored_flow(
        flow_id=1,
        title="금리 인상 뉴스 흐름",
        score=0.9,
        created_at=now,
    )
    news_flow.target_asset = "MARKET"

    market_flow = create_scored_flow(
        flow_id=2,
        title="국내 증시 하락 흐름",
        score=0.8,
        created_at=now,
    )

    flow_link = FlowLink(
        source_flow=news_flow,
        target_flow=market_flow,
        relation_type="potential_cause",
        score=0.9,
        reason="테스트 연결",
    )

    with Session(engine) as db:
        db.add_all([
            news_flow,
            market_flow,
            flow_link,
        ])
        db.commit()

        result = get_flow_feed(
            db=db,
            limit=20,
            offset=0,
            sort_by="latest",
        )

    items_by_id = {
        flow["flow_id"]: flow
        for flow in result["flows"]
    }

    assert items_by_id[1]["evidence_count"] == 1
    assert items_by_id[2]["evidence_count"] == 1

    assert items_by_id[1]["link_count"] == 1
    assert items_by_id[2]["link_count"] == 1