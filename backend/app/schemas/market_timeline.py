from datetime import datetime

from pydantic import BaseModel, Field


class MarketTimelineEvidenceResponse(BaseModel):
    evidence_id: int
    title: str
    source: str
    url: str | None


class MarketTimelineCauseResponse(BaseModel):
    flow_id: int
    title: str
    target_asset: str
    relation_type: str
    score: float
    reason: str


class MarketTimelineItemResponse(BaseModel):
    flow_id: int
    title: str
    target_asset: str
    summary: str | None
    score: float
    event_at: datetime
    evidence_count: int

    evidences: list[MarketTimelineEvidenceResponse] = Field(
        default_factory=list,
    )
    causes: list[MarketTimelineCauseResponse] = Field(
        default_factory=list,
    )


class MarketTimelineResponse(BaseModel):
    total: int
    limit: int
    target_asset: str | None
    timeline: list[MarketTimelineItemResponse] = Field(
        default_factory=list,
    )