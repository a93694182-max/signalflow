from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Literal


from app.database import get_db
from app.schemas.flow import (
    FlowFeedResponse,
    FlowTraceResponse,
)
from app.schemas.why import WhyAnalysisResponse
from app.schemas.timeline import FlowTimelineResponse
from app.services.flow_service import (
    get_flow_feed,
    get_flow_trace,
    get_flow_why_analysis,
    get_ranked_flows,
    get_flow_timeline,
)
from app.schemas.trail import WhyTrailResponse
from app.services.flow_link_service import get_why_trail



router = APIRouter(
    prefix="/api/flows",
    tags=["Flows"],
)


@router.get(
    "",
    response_model=FlowFeedResponse,
)
def read_flow_feed(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    target_asset: str | None = Query(
        default=None,
        max_length=50,
    ),
    include_news: bool = Query(
        default=True,
    ),
    query: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    from_date: date | None = Query(
        default=None,
    ),
    to_date: date | None = Query(
        default=None,
    ),
    sort_by: Literal["latest", "score"] = Query(
        default="latest",
        alias="sort",
    ),
    db: Session = Depends(get_db),

    
):
    return get_flow_feed(
        db=db,
        limit=limit,
        offset=offset,
        target_asset=target_asset,
        include_news=include_news,
        query=query,
        from_date=from_date,
        to_date=to_date,
        sort_by=sort_by,
    )


@router.get(
    "/{flow_id}/trace",
    response_model=FlowTraceResponse,
)
def read_flow_trace(
    flow_id: int,
    db: Session = Depends(get_db),
):
    return get_flow_trace(db, flow_id)



@router.get("/ranking")
def read_flow_ranking(
    db: Session = Depends(get_db),
):
    ranking = get_ranked_flows(db)

    return [
        {
            "rank": index,
            "flow_id": result.flow.id,
            "title": result.flow.title,
            "target_asset": result.flow.target_asset,
            "score": result.score,
            "quality_score": result.quality_score,
            "coverage_score": result.coverage_score,
            "evidence_count": result.evidence_count,
        }
        for index, result in enumerate(
            ranking,
            start=1,
        )
    ]



@router.get(
    "/{flow_id}/why",
    response_model=WhyAnalysisResponse,
)
def read_flow_why_analysis(
    flow_id: int,
    db: Session = Depends(get_db),
):
    result = get_flow_why_analysis(
        db=db,
        flow_id=flow_id,
    )

    analysis = result.analysis

    return {
        "flow_id": analysis.flow.id,
        "title": analysis.flow.title,
        "target_asset": (
            analysis.flow.target_asset
        ),
        "summary": result.summary,
        "confidence_score": (
            analysis.confidence_score
        ),
        "confidence_level": (
            analysis.confidence_level
        ),
        "primary_cause": (
            analysis.primary_cause
        ),
        "causes": analysis.causes,
        "external_causes": (
            result.external_causes
        ),
    }



@router.get(
    "/{flow_id}/timeline",
    response_model=FlowTimelineResponse,
)
def read_flow_timeline(
    flow_id: int,
    db: Session = Depends(get_db),
):
    result = get_flow_timeline(
        db=db,
        flow_id=flow_id,
    )

    return {
        "flow_id": result.flow.id,
        "title": result.flow.title,
        "target_asset": result.flow.target_asset,
        "event_count": len(result.events),
        "timeline": result.events,
    }


@router.get(
    "/{flow_id}/trail",
    response_model=WhyTrailResponse,
)
def read_why_trail(
    flow_id: int,
    db: Session = Depends(get_db),
):
    return get_why_trail(
        db=db,
        flow_id=flow_id,
    )