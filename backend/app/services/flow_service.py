from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session, selectinload

from app.core.flow_discovery import discover_flow
from app.core.flow_ranking import rank_flows
from app.models import Flow, FlowNode
from app.models.signal import Signal


def get_flow_trace(db: Session, flow_id: int) -> Flow:
    stmt = (
        select(Flow)
        .where(Flow.id == flow_id)
        .options(
            selectinload(Flow.nodes)
            .selectinload(FlowNode.evidences)
        )
    )

    flow = db.scalar(stmt)

    if flow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flow {flow_id}를 찾을 수 없습니다.",
        )

    return flow


def create_flow_from_signals(
    db: Session,
    signals: list[Signal],
) -> Flow:
    flow = discover_flow(signals)

    try:
        db.add(flow)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return get_flow_trace(db, flow.id)



def create_flows_from_signals(
    db: Session,
    signals: list[Signal],
) -> list[Flow]:
    discovered_flows = discover_flows(signals)

    saved_flows: list[Flow] = []

    try:
        for flow in discovered_flows:
            duplicate = find_duplicate_flow(db, flow)

            if duplicate is not None:
                saved_flows.append(duplicate)
                continue

            db.add(flow)
            db.flush()
            saved_flows.append(flow)

        db.commit()

        flow_ids = [flow.id for flow in saved_flows]

    except Exception:
        db.rollback()
        raise

    return [
        get_flow_trace(db, flow_id)
        for flow_id in flow_ids
    ]


def find_duplicate_flow(
    db: Session,
    flow: Flow,
) -> Flow | None:
    occurred_at = (
        flow.nodes[0].occurred_at
        if flow.nodes
        else None
    )

    stmt = (
        select(Flow)
        .join(Flow.nodes)
        .where(
            and_(
                Flow.title == flow.title,
                Flow.target_asset == flow.target_asset,
                FlowNode.occurred_at == occurred_at,
            )
        )
        .options(
            selectinload(Flow.nodes)
            .selectinload(FlowNode.evidences)
        )
    )

    return db.scalar(stmt)

def get_ranked_flows(db: Session):
    stmt = (
        select(Flow)
        .options(
            selectinload(Flow.nodes)
            .selectinload(FlowNode.evidences)
        )
    )

    flows = db.scalars(stmt).unique().all()

    return rank_flows(flows)