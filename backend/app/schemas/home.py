from datetime import datetime

from pydantic import BaseModel


class HomeTopWhyResponse(BaseModel):
    flow_id: int
    title: str
    target_asset: str
    score: float
    created_at: datetime


class HomeBiggestWhyResponse(HomeTopWhyResponse):
    summary: str
    confidence_score: float
    confidence_level: str
    external_cause_count: int


class HomeResponse(BaseModel):
    biggest_why: HomeBiggestWhyResponse | None
    top_whys: list[HomeTopWhyResponse]