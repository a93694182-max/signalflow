from datetime import datetime, timezone

from app.models.signal import Signal
from app.services.signal_filter_service import filter_signals


def make_news(
    title: str,
    news_id: int | None = None,
    url: str | None = None,
) -> Signal:
    return Signal(
        source="Reuters",
        signal_type="news",
        category="general",
        symbol="MARKET",
        name=title,
        value=None,
        previous_value=None,
        change=None,
        change_percent=None,
        direction=None,
        severity="info",
        occurred_at=datetime(2026, 10, 28, tzinfo=timezone.utc),
        title=title,
        url=url,
        metadata={"news_id": news_id},
    )


def test_duplicate_news_id():
    signals = [
        make_news("Fed cuts rates", news_id=100),
        make_news("Federal Reserve lowers rates", news_id=100),
    ]

    assert len(filter_signals(signals)) == 1


def test_duplicate_news_url():
    signals = [
        make_news(
            "Oil prices rise",
            url="https://example.com/news/1",
        ),
        make_news(
            "Oil market gains",
            url="https://example.com/news/1",
        ),
    ]

    assert len(filter_signals(signals)) == 1


def test_duplicate_news_title():
    signals = [
        make_news("Oil Prices Rise"),
        make_news("  oil   prices   rise  "),
    ]

    assert len(filter_signals(signals)) == 1


def test_different_news_are_preserved():
    signals = [
        make_news("Fed cuts rates", news_id=100),
        make_news("Oil prices rise", news_id=200),
    ]

    assert len(filter_signals(signals)) == 2