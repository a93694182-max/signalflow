from datetime import datetime

from pydantic import BaseModel, Field


class TimelineEventResponse(BaseModel):
    node_id: int
    order_index: int
    title: str
    category: str
    description: str | None
    occurred_at: datetime | None
    evidence_level: str
    evidence_count: int


class FlowTimelineResponse(BaseModel):
    flow_id: int
    title: str
    target_asset: str
    event_count: int
    timeline: list[TimelineEventResponse] = Field(
        default_factory=list,
    )