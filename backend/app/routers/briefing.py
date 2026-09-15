from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.briefing import DailyBriefingResponse
from app.services.briefing_service import get_daily_briefing


router = APIRouter(
    prefix="/api/briefing",
    tags=["briefing"],
)


@router.get(
    "/daily",
    response_model=DailyBriefingResponse,
)
def read_daily_briefing(
    db: Session = Depends(get_db),
):
    return get_daily_briefing(db)