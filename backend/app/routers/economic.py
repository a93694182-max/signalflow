from fastapi import APIRouter, Query

from app.schemas.economic import EconomicSeriesResponse
from app.services.economic_service import get_fred_series


router = APIRouter(
    prefix="/api/economic",
    tags=["Economic"],
)


@router.get(
    "/fred/{series_id}",
    response_model=EconomicSeriesResponse,
)
def read_fred_series(
    series_id: str,
    limit: int = Query(default=24, ge=1, le=100),
):
    return get_fred_series(
        series_id=series_id,
        limit=limit,
    )