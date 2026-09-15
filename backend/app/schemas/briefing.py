from datetime import date, datetime

from pydantic import BaseModel


class BriefingFlowItem(BaseModel):
    flow_id: int
    title: str
    target_asset: str
    score: float
    created_at: datetime


class DailyBriefingResponse(BaseModel):
    date: date
    headline: str
    summary: str
    top_flows: list[BriefingFlowItem]
    key_causes: list[str]