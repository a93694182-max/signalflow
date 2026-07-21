from pydantic import BaseModel, Field


class WhyTrailStepResponse(BaseModel):
    source_flow_id: int
    source_title: str
    target_flow_id: int
    target_title: str
    relation_type: str
    score: float
    reason: str


class WhyTrailResponse(BaseModel):
    flow_id: int
    title: str
    trail_count: int
    trail: list[WhyTrailStepResponse] = Field(
        default_factory=list,
    )