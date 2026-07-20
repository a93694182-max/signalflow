from datetime import datetime, timedelta, timezone

from app.core.evidence_scoring import calculate_evidence_scores
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