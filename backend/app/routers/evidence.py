from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.evidence import EvidenceResponse
from app.services.evidence_service import get_evidence


router = APIRouter(
    prefix="/api/evidence",
    tags=["Evidence"],
)


@router.get(
    "/{evidence_id}",
    response_model=EvidenceResponse,
)
def read_evidence(
    evidence_id: int,
    db: Session = Depends(get_db),
):
    return get_evidence(db, evidence_id)