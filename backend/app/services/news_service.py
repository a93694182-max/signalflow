from datetime import datetime, timezone
from typing import Any

import requests

from app.config import FINNHUB_API_KEY
from app.core.news_topic_classifier import (
    classify_news_topic,
    is_relevant_news,
)
from app.models.signal import Signal


FINNHUB_BASE_URL = "https://finnhub.io/api/v1"


def get_market_news(
    category: str = "general",
    limit: int = 20,
) -> list[dict[str, Any]]:
    if not FINNHUB_API_KEY:
        raise RuntimeError("FINNHUB_API_KEY 환경변수가 설정되지 않았습니다.")

    response = requests.get(
        f"{FINNHUB_BASE_URL}/news",
        params={
            "category": category,
            "token": FINNHUB_API_KEY,
        },
        timeout=10,
    )

    response.raise_for_status()

    news_items = response.json()

    if not isinstance(news_items, list):
        raise RuntimeError("Finnhub 뉴스 응답 형식이 올바르지 않습니다.")

    return news_items[:limit]


def generate_news_signals(
    category: str = "general",
    limit: int = 20,
) -> list[Signal]:
    news_items = get_market_news(
        category=category,
        limit=limit,
    )

    signals: list[Signal] = []

    for item in news_items:
        headline = item.get("headline")

        if not headline:
            continue

        summary = item.get("summary")

        if not is_relevant_news(
            title=headline,
            summary=summary,
        ):
            continue

        published_timestamp = item.get("datetime")

        if published_timestamp:
            occurred_at = datetime.fromtimestamp(
                published_timestamp,
                tz=timezone.utc,
            )
        else:
            occurred_at = datetime.now(timezone.utc)

        summary = item.get("summary")

        topic = classify_news_topic(
            title=headline,
            summary=summary,
        )

        signal = Signal(
            source=item.get("source") or "Finnhub",
            signal_type="news",
            category=topic,
            symbol=item.get("related") or "MARKET",
            name=headline,
            value=None,
            previous_value=None,
            change=None,
            change_percent=None,
            direction=None,
            severity="info",
            occurred_at=occurred_at,
            title=headline,
            summary=summary,
            url=item.get("url"),
            metadata={
                "news_id": item.get("id"),
                "image": item.get("image"),
                "related": item.get("related"),
                "finnhub_category": item.get("category"),
                "topic": topic,
            },
        )

        signals.append(signal)

    return signals