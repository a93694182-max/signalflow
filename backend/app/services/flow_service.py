from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Flow


def get_flow_trace(db: Session, flow_id: int) -> Flow:
    stmt = (
        select(Flow)
        .options(selectinload(Flow.nodes))
        .where(Flow.id == flow_id)
    )

    flow = db.scalar(stmt)

    if flow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flow {flow_id}를 찾을 수 없습니다.",
        )

    return flow