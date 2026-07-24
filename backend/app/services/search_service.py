from datetime import date, datetime, time, timedelta
from typing import Literal
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models import Evidence, Flow, FlowNode


KOREA_TIMEZONE = ZoneInfo("Asia/Seoul")


def search_signalflow(
    db: Session,
    query: str,
    limit: int,
    search_type: Literal[
        "all",
        "flow",
        "evidence",
    ] = "all",
    target_asset: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
) -> dict:
    if (
        from_date is not None
        and to_date is not None
        and from_date > to_date
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="from_date는 to_date보다 늦을 수 없습니다.",
        )

    search_query = query.strip()

    if not search_query:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="검색어는 공백일 수 없습니다.",
        )

    flow_results = []
    evidence_results = []
    flow_count = 0
    evidence_count = 0

    date_conditions = []

    if from_date is not None:
        from_datetime = datetime.combine(
            from_date,
            time.min,
            tzinfo=KOREA_TIMEZONE,
        )

        date_conditions.append(
            Flow.created_at >= from_datetime
        )

    if to_date is not None:
        to_datetime = datetime.combine(
            to_date + timedelta(days=1),
            time.min,
            tzinfo=KOREA_TIMEZONE,
        )

        date_conditions.append(
            Flow.created_at < to_datetime
        )

    if search_type in {"all", "flow"}:
        flow_conditions = [
            or_(
                Flow.title.ilike(
                    f"%{search_query}%"
                ),
                Flow.summary.ilike(
                    f"%{search_query}%"
                ),
            ),
            *date_conditions,
        ]

        if target_asset is not None:
            flow_conditions.append(
                Flow.target_asset == target_asset
            )

        flow_count_stmt = (
            select(func.count())
            .select_from(Flow)
            .where(*flow_conditions)
        )

        flow_count = (
            db.scalar(flow_count_stmt) or 0
        )

        flow_stmt = (
            select(Flow)
            .where(*flow_conditions)
            .order_by(
                Flow.created_at.desc(),
                Flow.id.desc(),
            )
            .limit(limit)
        )

        flows = db.scalars(flow_stmt).all()

        flow_results = [
            {
                "flow_id": flow.id,
                "title": flow.title,
                "target_asset": flow.target_asset,
                "summary": flow.summary,
                "created_at": flow.created_at,
            }
            for flow in flows
        ]

    if search_type in {"all", "evidence"}:
        evidence_conditions = [
            or_(
                Evidence.title.ilike(
                    f"%{search_query}%"
                ),
                Evidence.content_summary.ilike(
                    f"%{search_query}%"
                ),
                Evidence.source.ilike(
                    f"%{search_query}%"
                ),
            ),
            *date_conditions,
        ]

        if target_asset is not None:
            evidence_conditions.append(
                Flow.target_asset == target_asset
            )

        evidence_count_stmt = (
            select(func.count())
            .select_from(Evidence)
            .join(FlowNode)
            .join(Flow)
            .where(*evidence_conditions)
        )

        evidence_count = (
            db.scalar(evidence_count_stmt) or 0
        )

        evidence_stmt = (
            select(Evidence)
            .join(FlowNode)
            .join(Flow)
            .where(*evidence_conditions)
            .options(
                selectinload(Evidence.node)
                .selectinload(FlowNode.flow)
            )
            .order_by(
                Evidence.created_at.desc(),
                Evidence.id.desc(),
            )
            .limit(limit)
        )

        evidences = (
            db.scalars(evidence_stmt)
            .unique()
            .all()
        )

        evidence_results = [
            {
                "evidence_id": evidence.id,
                "flow_id": evidence.node.flow.id,
                "flow_title": (
                    evidence.node.flow.title
                ),
                "target_asset": (
                    evidence.node.flow.target_asset
                ),
                "title": evidence.title,
                "source": evidence.source,
                "content_summary": (
                    evidence.content_summary
                ),
                "url": evidence.url,
                "published_at": (
                    evidence.published_at
                ),
            }
            for evidence in evidences
        ]

    return {
        "query": search_query,
        "total": flow_count + evidence_count,
        "flow_count": flow_count,
        "evidence_count": evidence_count,
        "flows": flow_results,
        "evidences": evidence_results,
    }