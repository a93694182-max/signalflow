from datetime import date

from pydantic import BaseModel, Field


class EconomicObservation(BaseModel):
    date: date
    value: float


class EconomicSeriesResponse(BaseModel):
    series_id: str
    name: str
    unit: str
    observations: list[EconomicObservation] = Field(default_factory=list)