from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Evidence


def get_evidence(db: Session, evidence_id: int) -> Evidence:
    stmt = select(Evidence).where(Evidence.id == evidence_id)

    evidence = db.scalar(stmt)

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence {evidence_id}를 찾을 수 없습니다.",
        )

    return evidence