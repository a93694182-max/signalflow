from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.flow import FlowTraceResponse
from app.services.flow_service import (
    get_flow_trace,
    get_ranked_flows,
)

router = APIRouter(
    prefix="/api/flows",
    tags=["Flows"],
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
            "evidence_count": result.evidence_count,
        }
        for index, result in enumerate(
            ranking,
            start=1,
        )
    ]
