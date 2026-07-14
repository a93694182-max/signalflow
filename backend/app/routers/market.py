from fastapi import APIRouter, Query

from app.schemas.market import (
    MarketDashboardResponse,
    MarketHistoryResponse,
    MarketPriceResponse,
)

from app.services.market_service import (
    get_market_dashboard,
    get_market_history,
    get_market_price,
)

router = APIRouter(
    prefix="/api/market",
    tags=["Market"],
)


@router.get(
    "/dashboard",
    response_model=MarketDashboardResponse,
)
def read_market_dashboard():
    return get_market_dashboard()


@router.get(
    "/history/{symbol}",
    response_model=MarketHistoryResponse,
)
def read_market_history(
    symbol: str,
    period: str = Query(default="1mo"),
    interval: str = Query(default="1d"),
):
    return get_market_history(
        symbol=symbol,
        period=period,
        interval=interval,
    )



@router.get(
    "/price/{symbol}",
    response_model=MarketPriceResponse,
)
def read_market_price(symbol: str):
    return get_market_price(symbol)