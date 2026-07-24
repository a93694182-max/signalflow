from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.core.flow_ranking import rank_flows
from app.models import Flow, FlowLink, FlowNode


KOREA_TIMEZONE = ZoneInfo("Asia/Seoul")


def get_market_timeline(
    db: Session,
    limit: int,
    target_asset: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    include_causes: bool = True,
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

    conditions = []

    if target_asset is not None:
        conditions.append(
            Flow.target_asset == target_asset
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

    stmt = (
        select(Flow)
        .where(*conditions)
        .options(
            selectinload(Flow.nodes)
            .selectinload(FlowNode.evidences),
            selectinload(Flow.incoming_links)
            .selectinload(FlowLink.source_flow),
        )
        .order_by(
            Flow.created_at.desc(),
            Flow.id.desc(),
        )
        .limit(limit)
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

    timeline = []

    # 최근 Flow를 조회한 뒤 시간 오름차순으로 반환
    for flow in reversed(flows):
        ranking = ranking_by_flow_id[flow.id]

        evidences = [
            evidence
            for node in flow.nodes
            for evidence in node.evidences
        ]

        evidence_summaries = [
            {
                "evidence_id": evidence.id,
                "title": evidence.title,
                "source": evidence.source,
                "url": evidence.url,
            }
            for evidence in evidences[:3]
        ]

        causes = []

        if include_causes:
            sorted_links = sorted(
                flow.incoming_links,
                key=lambda link: link.score,
                reverse=True,
            )

            causes = [
                {
                    "flow_id": link.source_flow.id,
                    "title": link.source_flow.title,
                    "target_asset": (
                        link.source_flow.target_asset
                    ),
                    "relation_type": link.relation_type,
                    "score": link.score,
                    "reason": link.reason,
                }
                for link in sorted_links[:3]
            ]

        timeline.append(
            {
                "flow_id": flow.id,
                "title": flow.title,
                "target_asset": flow.target_asset,
                "summary": flow.summary,
                "score": ranking.score,
                "event_at": flow.created_at,
                "evidence_count": len(evidences),
                "evidences": evidence_summaries,
                "causes": causes,
            }
        )

    return {
        "total": total,
        "limit": limit,
        "target_asset": target_asset,
        "timeline": timeline,
    }