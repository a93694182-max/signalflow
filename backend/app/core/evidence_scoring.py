from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.models.signal import Signal


SOURCE_RELIABILITY_SCORES = {
    # 공식 경제 데이터
    "fred": 1.0,

    # 시장 데이터
    "yahoo_finance": 0.9,

    # 주요 언론
    "reuters": 0.95,
    "bloomberg": 0.95,
    "associated press": 0.93,
    "ap": 0.93,
    "cnbc": 0.9,
    "financial times": 0.94,
    "the wall street journal": 0.94,
    "wall street journal": 0.94,
}

SEVERITY_IMPACT_SCORES = {
    "info": 0.5,
    "low": 0.4,
    "medium": 0.7,
    "high": 1.0,
}


@dataclass(frozen=True, slots=True)
class EvidenceScores:
    relation_score: float
    impact_score: float
    time_score: float
    reliability_score: float

    @property
    def total_score(self) -> float:
        score = (
            self.relation_score * 0.3
            + self.impact_score * 0.2
            + self.time_score * 0.2
            + self.reliability_score * 0.3
        )

        return round(score, 3)


def calculate_relation_score(signal: Signal) -> float:
    if signal.signal_type in {
        "market_change",
        "economic_change",
    }:
        return 1.0

    if signal.signal_type == "news":
        if signal.summary and signal.title:
            return 0.85

        if signal.title or signal.name:
            return 0.75

    return 0.5


def calculate_impact_score(signal: Signal) -> float:
    return SEVERITY_IMPACT_SCORES.get(
        signal.severity,
        0.5,
    )


def calculate_time_score(
    occurred_at: datetime,
    now: datetime | None = None,
) -> float:
    current_time = now or datetime.now(timezone.utc)

    if occurred_at.tzinfo is None:
        occurred_at = occurred_at.replace(tzinfo=timezone.utc)

    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)

    age_hours = max(
        0.0,
        (current_time - occurred_at).total_seconds() / 3600,
    )

    if age_hours <= 6:
        return 1.0

    if age_hours <= 24:
        return 0.9

    if age_hours <= 72:
        return 0.75

    if age_hours <= 168:
        return 0.6

    if age_hours <= 720:
        return 0.4

    return 0.2


def calculate_reliability_score(source: str) -> float:
    normalized_source = source.strip().lower()

    if normalized_source in SOURCE_RELIABILITY_SCORES:
        return SOURCE_RELIABILITY_SCORES[normalized_source]

    for known_source, score in SOURCE_RELIABILITY_SCORES.items():
        if known_source in normalized_source:
            return score

    return 0.6


def calculate_evidence_scores(
    signal: Signal,
    now: datetime | None = None,
) -> EvidenceScores:
    return EvidenceScores(
        relation_score=calculate_relation_score(signal),
        impact_score=calculate_impact_score(signal),
        time_score=calculate_time_score(
            occurred_at=signal.occurred_at,
            now=now,
        ),
        reliability_score=calculate_reliability_score(
            signal.source,
        ),
    )