from datetime import datetime

from pydantic import BaseModel, Field


class FlowSearchItemResponse(BaseModel):
    flow_id: int
    title: str
    target_asset: str
    summary: str | None
    created_at: datetime


class EvidenceSearchItemResponse(BaseModel):
    evidence_id: int
    flow_id: int
    flow_title: str
    target_asset: str
    title: str
    source: str
    content_summary: str | None
    url: str | None
    published_at: datetime | None


class UnifiedSearchResponse(BaseModel):
    query: str
    total: int
    flow_count: int
    evidence_count: int
    flows: list[FlowSearchItemResponse] = Field(
        default_factory=list,
    )
    evidences: list[EvidenceSearchItemResponse] = Field(
        default_factory=list,
    )