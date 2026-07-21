from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session, selectinload
from dataclasses import dataclass


from app.core.flow_discovery import discover_flow, discover_flows
from app.core.flow_ranking import rank_flows
from app.core.flow_timeline import build_flow_timeline
from app.core.why_analysis import (
    WhyAnalysisResult,
    analyze_flow,
)
from app.models import Flow, FlowNode
from app.models.signal import Signal
from app.services.flow_link_service import get_why_trail



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


@dataclass(frozen=True, slots=True)
class CrossFlowWhyAnalysisResult:
    analysis: WhyAnalysisResult
    summary: str
    external_causes: list[dict]




def get_flow_why_analysis(
    db: Session,
    flow_id: int,
) -> CrossFlowWhyAnalysisResult:
    flow = get_flow_trace(
        db=db,
        flow_id=flow_id,
    )

    analysis = analyze_flow(flow)

    trail_result = get_why_trail(
        db=db,
        flow_id=flow_id,
    )

    external_causes = (
        trail_result["trail"][:3]
    )

    if external_causes:
        cause_titles = ", ".join(
            f"'{cause['source_title']}'"
            for cause in external_causes
        )

        summary = (
            f"{flow.title}과 연결된 외부 원인 후보는 "
            f"{cause_titles}입니다."
        )

        if analysis.primary_cause is not None:
            summary += (
                f" 내부 신호 중에서는 "
                f"'{analysis.primary_cause.title}'가 "
                f"가장 강하게 나타났습니다."
            )

    else:
        summary = analysis.summary

    return CrossFlowWhyAnalysisResult(
        analysis=analysis,
        summary=summary,
        external_causes=external_causes,
    )

def get_flow_timeline(
    db: Session,
    flow_id: int,
):
    flow = get_flow_trace(
        db=db,
        flow_id=flow_id,
    )

    return build_flow_timeline(flow)