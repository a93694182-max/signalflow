from datetime import datetime, timezone

from app.core.flow_discovery import discover_flows
from app.models.signal import Signal
from app.services.signal_filter_service import filter_signals


def make_news_signal(title: str) -> Signal:
    return Signal(
        source="Reuters",
        signal_type="news",
        category="monetary_policy",
        symbol="MARKET",
        name=title,
        value=None,
        previous_value=None,
        change=None,
        change_percent=None,
        direction=None,
        severity="info",
        occurred_at=datetime(
            2026, 10, 28, tzinfo=timezone.utc
        ),
        title=title,
        summary="Federal Reserve monetary policy update",
        url="https://example.com/news/fed",
    )


def test_news_flow_creation():
    signals = [
        make_news_signal("Fed signals interest rate cut"),
    ]

    filtered_signals = filter_signals(signals)
    flows = discover_flows(filtered_signals)

    assert len(flows) == 1
    assert flows[0].title == "통화정책 뉴스 흐름"
    assert len(flows[0].nodes) == 1
    assert len(flows[0].nodes[0].evidences) == 1


def test_news_flow_empty_signals():
    signals = filter_signals([])

    assert signals == []