from app.models.signal import Signal


DIRECTION_LABELS = {
    "up": "상승",
    "down": "하락",
    "flat": "보합",
}

SEVERITY_LABELS = {
    "low": "낮음",
    "medium": "보통",
    "high": "높음",
}


def normalize_signal(signal: Signal) -> dict:
    return {
        "source": signal.source,
        "signal_type": signal.signal_type,
        "category": signal.category,
        "symbol": signal.symbol,
        "name": signal.name,
        "value": signal.value,
        "previous_value": signal.previous_value,
        "change": signal.change,
        "change_percent": signal.change_percent,
        "direction": signal.direction,
        "direction_label": DIRECTION_LABELS.get(
            signal.direction,
            signal.direction,
        ),
        "severity": signal.severity,
        "severity_label": SEVERITY_LABELS.get(
            signal.severity,
            signal.severity,
        ),
        "occurred_at": signal.occurred_at,
    }


def build_signal_title(signal: Signal) -> str:
    direction_label = DIRECTION_LABELS.get(
        signal.direction,
        signal.direction,
    )

    return (
        f"{signal.name} {abs(signal.change_percent):.2f}% "
        f"{direction_label}"
    )


def build_signal_summary(signal: Signal) -> str:
    direction_label = DIRECTION_LABELS.get(
        signal.direction,
        signal.direction,
    )

    return (
        f"{signal.name}은 이전 값 {signal.previous_value}에서 "
        f"{signal.value}로 {direction_label}했습니다. "
        f"변화량은 {signal.change:+.2f}, "
        f"변화율은 {signal.change_percent:+.2f}%입니다."
    )