from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EvidenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    flow_node_id: int
    evidence_type: str
    title: str
    source: str
    url: str | None
    content_summary: str | None

    relation_score: float | None
    impact_score: float | None
    time_score: float | None
    reliability_score: float | None

    published_at: datetime | None
    created_at: datetime