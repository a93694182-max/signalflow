import logging

import requests
from fastapi import HTTPException

from app.models.signal import Signal
from app.services.economic_service import FRED_SERIES
from app.services.market_service import SYMBOL_NAMES
from app.services.news_service import generate_news_signals
from app.services.signal_service import (
    generate_economic_signal,
    generate_market_signal,
)


logger = logging.getLogger(__name__)


def collect_market_signals() -> list[Signal]:
    signals: list[Signal] = []

    for symbol in SYMBOL_NAMES:
        try:
            signal = generate_market_signal(symbol)
            signals.append(signal)
        except (HTTPException, ValueError) as exc:
            logger.warning(
                "시장 Signal 수집 실패: symbol=%s, error=%s",
                symbol,
                exc,
            )

    return signals


def collect_economic_signals() -> list[Signal]:
    signals: list[Signal] = []

    for series_id in FRED_SERIES:
        try:
            signal = generate_economic_signal(series_id)
            signals.append(signal)
        except (HTTPException, ValueError) as exc:
            logger.warning(
                "경제 Signal 수집 실패: series_id=%s, error=%s",
                series_id,
                exc,
            )

    return signals


def collect_news_signals() -> list[Signal]:
    try:
        return generate_news_signals(
            category="general",
            limit=20,
        )
    except (requests.RequestException, RuntimeError, ValueError) as exc:
        logger.warning(
            "뉴스 Signal 수집 실패: error=%s",
            exc,
        )

        return []


def collect_all_signals() -> list[Signal]:
    market_signals = collect_market_signals()
    economic_signals = collect_economic_signals()
    news_signals = collect_news_signals()

    return market_signals + economic_signals + news_signals