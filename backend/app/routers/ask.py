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
    answer = generate_flow_answer(
        db=db,
        flow_id=request.flow_id,
        question=request.question,
    )

    return AskResponse(
        flow_id=request.flow_id,
        question=request.question,
        answer=answer,
    )