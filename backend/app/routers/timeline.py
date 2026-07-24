from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.market_timeline import (
    MarketTimelineResponse,
)
from app.services.market_timeline_service import (
    get_market_timeline,
)


router = APIRouter(
    prefix="/api/timeline",
    tags=["Timeline"],
)


@router.get(
    "",
    response_model=MarketTimelineResponse,
)
def read_market_timeline(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    target_asset: str | None = Query(
        default=None,
        max_length=50,
    ),
    from_date: date | None = Query(
        default=None,
    ),
    to_date: date | None = Query(
        default=None,
    ),
    include_causes: bool = Query(
        default=True,
    ),
    db: Session = Depends(get_db),
):
    return get_market_timeline(
        db=db,
        limit=limit,
        target_asset=target_asset,
        from_date=from_date,
        to_date=to_date,
        include_causes=include_causes,
    )