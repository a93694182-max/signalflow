from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.services.flow_service import (
    get_flow_why_analysis,
    get_ranked_flows,
)


BRIEFING_FLOW_WINDOW_HOURS = 24
BRIEFING_TOP_FLOW_LIMIT = 3


def get_daily_briefing(db: Session) -> dict:
    now = datetime.now(timezone.utc)
    created_after = now - timedelta(
        hours=BRIEFING_FLOW_WINDOW_HOURS
    )

    ranked_flows = [
        result
        for result in get_ranked_flows(
            db,
            created_after=created_after,
        )
        if result.flow.target_asset != "MARKET"
    ]

    if not ranked_flows:
        return {
            "date": now.date(),
            "headline": "오늘 생성된 주요 시장 흐름이 없습니다.",
            "summary": "분석할 수 있는 최근 시장 Flow가 없습니다.",
            "top_flows": [],
            "key_causes": [],
        }

    top_results = ranked_flows[:BRIEFING_TOP_FLOW_LIMIT]
    primary_result = top_results[0]

    why_result = get_flow_why_analysis(
        db=db,
        flow_id=primary_result.flow.id,
    )

    key_causes = [
        cause["source_title"]
        for cause in why_result.external_causes
    ]

    if (
        not key_causes
        and why_result.analysis.primary_cause is not None
    ):
        key_causes.append(
            why_result.analysis.primary_cause.title
        )

    top_flows = [
        {
            "flow_id": result.flow.id,
            "title": result.flow.title,
            "target_asset": result.flow.target_asset,
            "score": result.score,
            "created_at": result.flow.created_at,
        }
        for result in top_results
    ]

    return {
        "date": now.date(),
        "headline": primary_result.flow.title,
        "summary": why_result.summary,
        "top_flows": top_flows,
        "key_causes": key_causes,
    }