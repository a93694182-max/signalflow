from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status
from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session, selectinload
from typing import Literal

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



KOREA_TIMEZONE = ZoneInfo("Asia/Seoul")




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

def get_ranked_flows(
    db: Session,
    created_after: datetime | None = None,
):
    stmt = select(Flow).options(
        selectinload(Flow.nodes)
        .selectinload(FlowNode.evidences)
    )

    # 최신성 기준 적용
    if created_after is not None:
        stmt = stmt.where(
            Flow.created_at >= created_after
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


def get_flow_feed(
    db: Session,
    limit: int,
    offset: int,
    target_asset: str | None = None,
    include_news: bool = True,
    query: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    sort_by: Literal["latest", "score"] = "latest",
) -> dict:
    conditions = []

    if (
        from_date is not None
        and to_date is not None
        and from_date > to_date
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="from_date는 to_date보다 늦을 수 없습니다.",
        )
    
    if sort_by not in {"latest", "score"}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="sort는 latest 또는 score만 사용할 수 있습니다.",
        )


    if target_asset is not None:
        conditions.append(
            Flow.target_asset == target_asset
        )

    if not include_news:
        conditions.append(
            Flow.target_asset != "MARKET"
        )

    if query is not None:
        search_query = query.strip()

        if search_query:
            conditions.append(
                Flow.title.ilike(
                    f"%{search_query}%"
                )
            )


    if from_date is not None:
        from_datetime = datetime.combine(
            from_date,
            time.min,
            tzinfo=KOREA_TIMEZONE,
        )

        conditions.append(
            Flow.created_at >= from_datetime
        )

    if to_date is not None:
        # 종료일 전체 포함
        to_datetime = datetime.combine(
            to_date + timedelta(days=1),
            time.min,
            tzinfo=KOREA_TIMEZONE,
        )

        conditions.append(
            Flow.created_at < to_datetime
        )

    count_stmt = (
        select(func.count())
        .select_from(Flow)
        .where(*conditions)
    )

    total = db.scalar(count_stmt) or 0

    base_stmt = (
        select(Flow)
        .where(*conditions)
        .options(
            selectinload(Flow.nodes)
            .selectinload(FlowNode.evidences)
        )
    )

    if sort_by == "score":
        # 기존 Flow Ranking 기준 재사용
        matching_flows = (
            db.scalars(base_stmt)
            .unique()
            .all()
        )

        ranked_results = rank_flows(
            matching_flows
        )

        page_results = ranked_results[
            offset:offset + limit
        ]

        flow_items = [
            {
                "flow_id": result.flow.id,
                "title": result.flow.title,
                "target_asset": (
                    result.flow.target_asset
                ),
                "summary": result.flow.summary,
                "score": result.score,
                "created_at": (
                    result.flow.created_at
                ),
                "updated_at": (
                    result.flow.updated_at
                ),
            }
            for result in page_results
        ]

    else:
        stmt = (
            base_stmt
            .order_by(
                Flow.created_at.desc(),
                Flow.id.desc(),
            )
            .limit(limit)
            .offset(offset)
        )

        flows = (
            db.scalars(stmt)
            .unique()
            .all()
        )

        ranking_by_flow_id = {
            result.flow.id: result
            for result in rank_flows(flows)
        }

        flow_items = [
            {
                "flow_id": flow.id,
                "title": flow.title,
                "target_asset": flow.target_asset,
                "summary": flow.summary,
                "score": (
                    ranking_by_flow_id[flow.id].score
                ),
                "created_at": flow.created_at,
                "updated_at": flow.updated_at,
            }
            for flow in flows
        ]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "flows": flow_items,
    }