from datetime import datetime, timedelta, timezone
from app.core.evidence_scoring import (
    calculate_evidence_scores,
    calculate_impact_score,
    calculate_relation_score,
    calculate_reliability_score,
    calculate_time_score,
)
from app.models.signal import Signal


now = datetime.now(timezone.utc)


def make_news_signal(
    source: str,
    hours_ago: int,
) -> Signal:
    return Signal(
        source=source,
        signal_type="news",
        category="general",
        symbol="MARKET",
        name="Oil prices rise after supply concerns",
        value=None,
        previous_value=None,
        change=None,
        change_percent=None,
        direction=None,
        severity="info",
        occurred_at=now - timedelta(hours=hours_ago),
        title="Oil prices rise after supply concerns",
        summary="Oil prices increased due to supply concerns.",
        url="https://example.com/news",
    )


signals = [
    make_news_signal("Reuters", 2),
    make_news_signal("CNBC", 30),
    make_news_signal("Unknown Blog", 200),
]

for signal in signals:
    scores = calculate_evidence_scores(
        signal,
        now=now,
    )

    print("=" * 60)
    print(f"source: {signal.source}")
    print(f"relation: {scores.relation_score}")
    print(f"impact: {scores.impact_score}")
    print(f"time: {scores.time_score}")
    print(f"reliability: {scores.reliability_score}")
    print(f"total: {scores.total_score}")

def test_known_source_reliability():
    assert calculate_reliability_score("Reuters") == 0.95
    assert calculate_reliability_score("REUTERS") == 0.95
    assert calculate_reliability_score("  Reuters  ") == 0.95


def test_unknown_source_reliability():
    assert calculate_reliability_score("Unknown Blog") == 0.6


def test_partial_source_name_is_not_trusted():
    assert calculate_reliability_score("fake_reuters_news") == 0.6

def test_future_evidence_time_score():
    now = datetime.now(timezone.utc)

    future_time = now + timedelta(hours=2)

    score = calculate_time_score(
        occurred_at=future_time,
        now=now,
    )

    assert score == 0.0


def test_recent_evidence_time_score():
    now = datetime.now(timezone.utc)

    recent_time = now - timedelta(hours=2)

    score = calculate_time_score(
        occurred_at=recent_time,
        now=now,
    )

    assert score == 1.0

def test_relevant_news_relation_score():
    signal = make_news_signal(
        source="Reuters",
        hours_ago=2,
    )

    assert calculate_relation_score(signal) == 0.85


def test_irrelevant_news_relation_score():
    signal = make_news_signal(
        source="Reuters",
        hours_ago=2,
    )

    signal.title = "Football team wins championship"
    signal.summary = "The team celebrated its victory."

    assert calculate_relation_score(signal) == 0.3


def test_market_impact_score():
    signal = make_news_signal(
        source="Yahoo Finance",
        hours_ago=2,
    )

    signal.signal_type = "market_change"
    signal.change_percent = 5.0

    assert calculate_impact_score(signal) == 1.0

    signal.change_percent = 1.5

    assert calculate_impact_score(signal) == 0.7

    signal.change_percent = -0.6

    assert calculate_impact_score(signal) == 0.5


def test_news_impact_score():
    signal = make_news_signal(
        source="Reuters",
        hours_ago=2,
    )

    signal.severity = "high"

    assert calculate_impact_score(signal) == 1.0