from datetime import date, datetime, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Evidence, Flow, FlowNode
from app.services.search_service import search_signalflow


def create_search_flow(
    flow_id: int,
    title: str,
    target_asset: str,
    evidence_title: str,
) -> Flow:
    now = datetime.now(timezone.utc)

    flow = Flow(
        id=flow_id,
        title=title,
        target_asset=target_asset,
        summary=f"{title} 요약",
        created_at=now,
        updated_at=now,
    )

    node = FlowNode(
        id=flow_id,
        order_index=1,
        title=f"{title} 신호",
        category="market",
        occurred_at=now,
        evidence_level="strong",
    )

    evidence = Evidence(
        id=flow_id,
        evidence_type="news",
        title=evidence_title,
        source="Reuters",
        content_summary=f"{evidence_title} 내용",
        url=f"https://example.com/{flow_id}",
        published_at=now,
    )

    node.evidences.append(evidence)
    flow.nodes.append(node)

    return flow


def test_unified_search_finds_flows_and_evidences():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    flows = [
        create_search_flow(
            flow_id=1,
            title="금리 인상 전망",
            target_asset="^KS11",
            evidence_title="금리 정책 뉴스",
        ),
        create_search_flow(
            flow_id=2,
            title="비트코인 상승",
            target_asset="BTC-USD",
            evidence_title="가상자산 시장 뉴스",
        ),
    ]

    with Session(engine) as db:
        db.add_all(flows)
        db.commit()

        result = search_signalflow(
            db=db,
            query="금리",
            limit=20,
        )

    assert result["query"] == "금리"
    assert result["total"] == 2
    assert result["flow_count"] == 1
    assert result["evidence_count"] == 1

    assert result["flows"][0]["flow_id"] == 1
    assert result["evidences"][0]["flow_id"] == 1


def test_unified_search_filters_type_and_asset():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    flows = [
        create_search_flow(
            flow_id=1,
            title="시장 상승",
            target_asset="^KS11",
            evidence_title="시장 상승 근거",
        ),
        create_search_flow(
            flow_id=2,
            title="시장 상승",
            target_asset="BTC-USD",
            evidence_title="시장 상승 근거",
        ),
    ]

    with Session(engine) as db:
        db.add_all(flows)
        db.commit()

        result = search_signalflow(
            db=db,
            query="시장",
            limit=20,
            search_type="evidence",
            target_asset="^KS11",
        )

    assert result["total"] == 1
    assert result["flow_count"] == 0
    assert result["evidence_count"] == 1
    assert result["flows"] == []

    evidence = result["evidences"][0]

    assert evidence["flow_id"] == 1
    assert evidence["target_asset"] == "^KS11"


def test_unified_search_rejects_blank_query():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    with Session(engine) as db:
        with pytest.raises(HTTPException) as error:
            search_signalflow(
                db=db,
                query="   ",
                limit=20,
            )

    assert error.value.status_code == 422
    assert (
        error.value.detail
        == "검색어는 공백일 수 없습니다."
    )


def test_unified_search_rejects_invalid_date_range():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    with Session(engine) as db:
        with pytest.raises(HTTPException) as error:
            search_signalflow(
                db=db,
                query="시장",
                limit=20,
                from_date=date(2026, 7, 24),
                to_date=date(2026, 7, 23),
            )

    assert error.value.status_code == 422
    assert (
        error.value.detail
        == "from_date는 to_date보다 늦을 수 없습니다."
    )