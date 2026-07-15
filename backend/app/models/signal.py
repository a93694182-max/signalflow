from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Signal:
    source: str
    signal_type: str
    category: str

    symbol: str
    name: str

    value: float
    previous_value: float

    change: float
    change_percent: float

    direction: str
    severity: str

    occurred_at: datetime