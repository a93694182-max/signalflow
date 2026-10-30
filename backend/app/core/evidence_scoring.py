from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from app.models.signal import Signal
from app.core.news_topic_classifier import is_relevant_news


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
        title = signal.title or signal.name or ""
        summary = signal.summary or ""

        if not is_relevant_news(title, summary):
            return 0.3

        if title and summary:
            return 0.85

        return 0.75

    return 0.5


def calculate_impact_score(signal: Signal) -> float:
    severity_score = SEVERITY_IMPACT_SCORES.get(
        signal.severity,
        0.5,
    )

    if signal.signal_type != "market_change":
        return severity_score

    if signal.change_percent is None:
        return severity_score

    change_percent = abs(signal.change_percent)

    if change_percent >= 5.0:
        return 1.0

    if change_percent >= 3.0:
        return 0.9

    if change_percent >= 1.0:
        return 0.7

    if change_percent >= 0.5:
        return 0.5

    return 0.3


def calculate_time_score(
    occurred_at: datetime,
    now: datetime | None = None,
) -> float:
    current_time = now or datetime.now(timezone.utc)

    if occurred_at.tzinfo is None:
        occurred_at = occurred_at.replace(tzinfo=timezone.utc)

    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)

    age_hours = (
        current_time - occurred_at
    ).total_seconds() / 3600

    if age_hours < 0:
        return 0.0

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
    normalized_source = " ".join(
        source.strip().lower().split()
    )

    return SOURCE_RELIABILITY_SCORES.get(
        normalized_source,
        0.6,
    )


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