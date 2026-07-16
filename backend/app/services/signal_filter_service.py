from app.models.signal import Signal


MINIMUM_CHANGE_PERCENT = {
    "market_change": 0.5,
    "economic_change": 0.1,
}


def is_meaningful_signal(signal: Signal) -> bool:
    if signal.signal_type == "news":
        return bool(signal.title or signal.name)

    if signal.direction in (None, "flat"):
        return False

    if signal.change_percent is None:
        return False

    minimum_change = MINIMUM_CHANGE_PERCENT.get(
        signal.signal_type,
        0.5,
    )

    return abs(signal.change_percent) >= minimum_change


def filter_signals(signals: list[Signal]) -> list[Signal]:
    return [
        signal
        for signal in signals
        if is_meaningful_signal(signal)
    ]