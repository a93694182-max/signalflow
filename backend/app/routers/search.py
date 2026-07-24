from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.search import UnifiedSearchResponse
from app.services.search_service import (
    search_signalflow,
)


router = APIRouter(
    prefix="/api/search",
    tags=["Search"],
)


@router.get(
    "",
    response_model=UnifiedSearchResponse,
)
def read_unified_search(
    query: str = Query(
        min_length=1,
        max_length=100,
        alias="q",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search_type: Literal[
        "all",
        "flow",
        "evidence",
    ] = Query(
        default="all",
        alias="type",
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
    db: Session = Depends(get_db),
):
    return search_signalflow(
        db=db,
        query=query,
        limit=limit,
        search_type=search_type,
        target_asset=target_asset,
        from_date=from_date,
        to_date=to_date,
    )