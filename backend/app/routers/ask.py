from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ask import AskRequest, AskResponse
from app.services.ai_service import generate_flow_answer


router = APIRouter(
    prefix="/api/ask",
    tags=["Ask"],
)


@router.post(
    "",
    response_model=AskResponse,
)
def ask_question(
    request: AskRequest,
    db: Session = Depends(get_db),
):
    result = generate_flow_answer(
        db=db,
        flow_id=request.flow_id,
        question=request.question,
    )

    return AskResponse(
        flow_id=request.flow_id,
        question=request.question,
        answer=result.answer,
        confidence_score=result.confidence_score,
        confidence_level=result.confidence_level,
        primary_cause=result.primary_cause,
        flow_path=result.flow_path,
        evidence_count=result.evidence_count,
        answer_source=result.answer_source,
        why_trail=result.why_trail,
    )