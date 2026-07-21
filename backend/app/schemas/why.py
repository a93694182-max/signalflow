from pydantic import BaseModel, ConfigDict, Field

from app.schemas.trail import WhyTrailStepResponse


class WhyCauseResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    node_id: int
    title: str
    category: str
    description: str | None
    score: float
    evidence_count: int


class WhyAnalysisResponse(BaseModel):
    flow_id: int
    title: str
    target_asset: str
    summary: str
    confidence_score: float
    confidence_level: str

    primary_cause: WhyCauseResponse | None

    causes: list[WhyCauseResponse] = Field(
        default_factory=list,
    )

    external_causes: list[
        WhyTrailStepResponse
    ] = Field(
        default_factory=list,
    )