from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Signal:
    source: str
    signal_type: str
    category: str

    symbol: str
    name: str

    value: float | None
    previous_value: float | None

    change: float | None
    change_percent: float | None

    direction: str | None
    severity: str

    occurred_at: datetime

    title: str | None = None
    summary: str | None = None
    url: str | None = None
    metadata: dict[str, Any] | None = None