from datetime import datetime

from pydantic import BaseModel,  Field


class MarketPriceResponse(BaseModel):
    symbol: str
    name: str
    price: float
    previous_close: float
    change: float
    change_percent: float
    currency: str | None
    market_time: datetime | None

class MarketDashboardResponse(BaseModel):
    markets: list[MarketPriceResponse] = Field(default_factory=list)


class MarketHistoryPoint(BaseModel):
    time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class MarketHistoryResponse(BaseModel):
    symbol: str
    name: str
    period: str
    interval: str
    points: list[MarketHistoryPoint] = Field(default_factory=list)