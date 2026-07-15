from datetime import datetime, timezone

from app.models.signal import Signal
from app.services.economic_service import get_fred_series
from app.services.market_service import get_market_price

MARKET_CATEGORIES = {
    "^KS11": "domestic_stock",
    "^KQ11": "domestic_stock",
    "KRW=X": "currency",
    "BTC-USD": "crypto",
    "GC=F": "commodity",
    "CL=F": "commodity",
}

MARKET_THRESHOLDS = {
    "low": 0.5,
    "medium": 1.0,
    "high": 2.0,
}

ECONOMIC_THRESHOLDS = {
    "low": 0.1,
    "medium": 0.5,
    "high": 1.0,
}


def determine_direction(change: float) -> str:
    if change > 0:
        return "up"

    if change < 0:
        return "down"

    return "flat"


def determine_severity(
    change_percent: float,
    thresholds: dict[str, float],
) -> str:
    absolute_change = abs(change_percent)

    if absolute_change >= thresholds["high"]:
        return "high"

    if absolute_change >= thresholds["medium"]:
        return "medium"

    return "low"


def generate_market_signal(symbol: str) -> Signal:
    market = get_market_price(symbol)

    change = float(market["change"])
    change_percent = float(market["change_percent"])

    return Signal(
        source="yahoo_finance",
        signal_type="market_change",
        category=MARKET_CATEGORIES.get(
            market["symbol"],
            "market",
        ),
        symbol=market["symbol"],
        name=market["name"],
        value=float(market["price"]),
        previous_value=float(market["previous_close"]),
        change=change,
        change_percent=change_percent,
        direction=determine_direction(change),
        severity=determine_severity(
            change_percent,
            MARKET_THRESHOLDS,
            
        ),
        
        occurred_at=market["market_time"],
    )


def generate_economic_signal(series_id: str) -> Signal:
    series = get_fred_series(
        series_id=series_id,
        limit=2,
    )
    category="economic",
    observations = series["observations"]

    if len(observations) < 2:
        raise ValueError(
            f"{series_id}는 변화율 계산에 필요한 데이터가 부족합니다."
        )

    previous_observation = observations[-2]
    current_observation = observations[-1]

    previous_value = float(previous_observation["value"])
    value = float(current_observation["value"])

    change = value - previous_value
    change_percent = (
        change / previous_value * 100
        if previous_value != 0
        else 0.0
    )

    return Signal(
        source="fred",
        signal_type="economic_change",
        category="economic",
        symbol=series["series_id"],
        name=series["name"],
        value=round(value, 4),
        previous_value=round(previous_value, 4),
        change=round(change, 4),
        change_percent=round(change_percent, 2),
        direction=determine_direction(change),
        severity=determine_severity(
            change_percent,
            ECONOMIC_THRESHOLDS,
        ),
        occurred_at=datetime.fromisoformat(
            current_observation["date"]
        ).replace(tzinfo=timezone.utc),
    )