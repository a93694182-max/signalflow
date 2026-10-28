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
    filtered_signals: list[Signal] = []

    seen_ids = set()
    seen_urls = set()
    seen_titles = set()

    for signal in signals:
        if not is_meaningful_signal(signal):
            continue

        if signal.signal_type != "news":
            filtered_signals.append(signal)
            continue

        metadata = signal.metadata or {}
        news_id = metadata.get("news_id")

        url = (signal.url or "").strip().lower()
        title = " ".join(
            (signal.title or signal.name).split()
        ).casefold()

        if (
            (news_id is not None and news_id in seen_ids)
            or (url and url in seen_urls)
            or (title and title in seen_titles)
        ):
            continue

        filtered_signals.append(signal)

        if news_id is not None:
            seen_ids.add(news_id)

        if url:
            seen_urls.add(url)

        if title:
            seen_titles.add(title)

    return filtered_signals