from datetime import datetime, timezone

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Flow
from app.services.flow_service import create_flows_from_signals


def test_duplicate_flow_is_not_returned(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    occurred_at = datetime(
        2026, 10, 28, 12, 0, tzinfo=timezone.utc
    )

   

    def fake_discover_flows(signals):
        from app.models import FlowNode

        flow = Flow(
            title="시장 상승 흐름",
            target_asset="TEST",
            summary="테스트",
        )

        flow.nodes.append(
            FlowNode(
                order_index=1,
                title="테스트 신호",
                category="market",
                description="테스트",
                occurred_at=occurred_at,
                evidence_level="moderate",
            )
        )

        return [flow]

    monkeypatch.setattr(
        "app.services.flow_service.discover_flows",
        fake_discover_flows,
    )

    with Session(engine) as db:
        first_result = create_flows_from_signals(
            db=db,
            signals=[],
        )

        second_result = create_flows_from_signals(
            db=db,
            signals=[],
        )

        flow_count = db.scalar(
            select(func.count()).select_from(Flow)
        )

    assert len(first_result) == 1
    assert len(second_result) == 0
    assert flow_count == 1


def test_same_timestamp_different_node_is_not_duplicate(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    occurred_at = datetime(
        2026, 10, 28, 12, 0, tzinfo=timezone.utc
    )

    node_titles = iter([
        "코스피 1% 상승",
        "코스피 2% 상승",
    ])

    def fake_discover_flows(signals):
        from app.models import FlowNode

        flow = Flow(
            title="국내 증시 상승 흐름",
            target_asset="^KS11",
            summary="테스트",
        )

        flow.nodes.append(
            FlowNode(
                order_index=1,
                title=next(node_titles),
                category="domestic_stock",
                description="테스트",
                occurred_at=occurred_at,
                evidence_level="moderate",
            )
        )

        return [flow]

    monkeypatch.setattr(
        "app.services.flow_service.discover_flows",
        fake_discover_flows,
    )

    with Session(engine) as db:
        first_result = create_flows_from_signals(db, [])
        second_result = create_flows_from_signals(db, [])

        flow_count = db.scalar(
            select(func.count()).select_from(Flow)
        )

    assert len(first_result) == 1
    assert len(second_result) == 1
    assert flow_count == 2