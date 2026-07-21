from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    flow_id: int
    question: str = Field(
        min_length=1,
        max_length=500,
    )


class AskResponse(BaseModel):
    flow_id: int
    question: str
    answer: str
    confidence_score: float
    confidence_level: str
    primary_cause: str | None
    flow_path: list[str]
    evidence_count: int
    answer_source: str
    why_trail: list[str]