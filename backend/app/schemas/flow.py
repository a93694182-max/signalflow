from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.evidence import EvidenceResponse



class FlowNodeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_index: int
    title: str
    category: str
    description: str | None
    occurred_at: datetime | None
    evidence_level: str
    
    evidences: list[EvidenceResponse] = Field(default_factory=list)


class FlowTraceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    target_asset: str
    summary: str | None
    updated_at: datetime
    nodes: list[FlowNodeResponse]