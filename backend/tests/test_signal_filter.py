from datetime import datetime, timezone

from app.models.signal import Signal
from app.services.signal_filter_service import is_meaningful_signal


news_signal = Signal(
    source="Reuters",
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
    occurred_at=datetime.now(timezone.utc),
    title="Oil prices rise after supply concerns",
)


market_signal = Signal(
    source="Yahoo Finance",
    signal_type="market_change",
    category="market",
    symbol="AAPL",
    name="Apple",
    value=210.0,
    previous_value=208.0,
    change=2.0,
    change_percent=0.96,
    direction="up",
    severity="medium",
    occurred_at=datetime.now(timezone.utc),
)


small_market_signal = Signal(
    source="Yahoo Finance",
    signal_type="market_change",
    category="market",
    symbol="MSFT",
    name="Microsoft",
    value=500.0,
    previous_value=499.0,
    change=1.0,
    change_percent=0.2,
    direction="up",
    severity="low",
    occurred_at=datetime.now(timezone.utc),
)


print("뉴스 통과:", is_meaningful_signal(news_signal))
print("시장 Signal 통과:", is_meaningful_signal(market_signal))
print("작은 시장 Signal 통과:", is_meaningful_signal(small_market_signal))