from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    flow_id: int
    question: str = Field(min_length=1, max_length=500)


class AskResponse(BaseModel):
    flow_id: int
    question: str
    answer: str