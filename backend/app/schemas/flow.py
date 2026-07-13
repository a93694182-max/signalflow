from datetime import datetime

from pydantic import BaseModel


class FlowNodeResponse(BaseModel):
    id: int
    order_index: int
    title: str
    category: str
    description: str
    occurred_at: datetime
    evidence_level: str


class FlowTraceResponse(BaseModel):
    id: int
    title: str
    target_asset: str
    summary: str
    updated_at: datetime
    nodes: list[FlowNodeResponse]