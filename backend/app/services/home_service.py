from sqlalchemy.orm import Session

from app.services.flow_service import (
    get_flow_why_analysis,
    get_ranked_flows,
)

from datetime import datetime, timedelta, timezone


HOME_FLOW_WINDOW_HOURS = 24

def get_home_data(db: Session) -> dict:
    created_after = (
        datetime.now(timezone.utc)
        - timedelta(hours=HOME_FLOW_WINDOW_HOURS)
    )

    # 홈은 현재 상황을 보여주므로 최근 24시간 내 생성된 Flow만 사용
    ranked_flows = [
        result
        for result in get_ranked_flows(
            db,
            created_after=created_after,
        )
        # 뉴스는 분석 대상이 아니라 시장 움직임의 외부 원인 후보로 사용
        if result.flow.target_asset != "MARKET"
    ]

    if not ranked_flows:
        return {
            "biggest_why": None,
            "top_whys": [],
        }

    biggest_result = ranked_flows[0]
    biggest_flow = biggest_result.flow

    why_result = get_flow_why_analysis(
        db=db,
        flow_id=biggest_flow.id,
    )

    biggest_why = {
        "flow_id": biggest_flow.id,
        "title": biggest_flow.title,
        "target_asset": biggest_flow.target_asset,
        "summary": why_result.summary,
        "score": biggest_result.score,
        "confidence_score": (
            why_result.analysis.confidence_score
        ),
        "confidence_level": (
            why_result.analysis.confidence_level
        ),
        "external_cause_count": len(
            why_result.external_causes
        ),
        "created_at": biggest_flow.created_at,
    }

    top_whys = [
        {
            "flow_id": result.flow.id,
            "title": result.flow.title,
            "target_asset": result.flow.target_asset,
            "score": result.score,
            "created_at": result.flow.created_at,
        }
        for result in ranked_flows[1:4]
    ]

    return {
        "biggest_why": biggest_why,
        "top_whys": top_whys,
    }