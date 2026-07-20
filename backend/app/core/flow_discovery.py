from collections import defaultdict

from app.core.signal_normalizer import (
    build_signal_summary,
    build_signal_title,
)
from app.models import Evidence, Flow, FlowNode
from app.models.signal import Signal
from app.core.evidence_scoring import calculate_evidence_scores



EVIDENCE_LEVELS = {
    "info": "moderate",
    "low": "weak",
    "medium": "moderate",
    "high": "strong",
}

IMPACT_SCORES = {
    "info": 0.5,
    "low": 0.4,
    "medium": 0.7,
    "high": 1.0,
}

CATEGORY_NAMES = {
    "domestic_stock": "국내 증시",
    "currency": "환율",
    "crypto": "가상자산",
    "commodity": "원자재",
    "economic": "경제지표",
    "market": "시장",
    "general": "주요 뉴스",
    "monetary_policy": "통화정책 뉴스",
    "geopolitics": "지정학 뉴스",
    "technology": "기술 뉴스",
    "corporate": "기업 뉴스",
}


def get_signal_category(signal: Signal) -> str:
    if signal.signal_type == "economic_change":
        return "economic"

    if signal.signal_type == "news":
        return signal.category or "general"

    return signal.category


def get_evidence_type(signal: Signal) -> str:
    if signal.signal_type == "market_change":
        return "market_data"

    if signal.signal_type == "economic_change":
        return "economic_data"

    if signal.signal_type == "news":
        return "news"

    return "external_data"


def get_source_url(signal: Signal) -> str | None:
    if signal.url:
        return signal.url

    if signal.source == "yahoo_finance":
        return f"https://finance.yahoo.com/quote/{signal.symbol}"

    if signal.source == "fred":
        return f"https://fred.stlouisfed.org/series/{signal.symbol}"

    return None


def get_signal_sort_score(signal: Signal) -> float:
    if signal.change_percent is not None:
        return abs(signal.change_percent)

    if signal.signal_type == "news":
        return IMPACT_SCORES.get(signal.severity, 0.5)

    return 0.0


def determine_group_direction(signals: list[Signal]) -> str:
    comparable_signals = [
        signal
        for signal in signals
        if signal.signal_type != "news"
    ]

    if not comparable_signals:
        return "주요"

    direction_score = 0

    for signal in comparable_signals:
        if signal.direction == "up":
            direction_score += 1
        elif signal.direction == "down":
            direction_score -= 1

    if direction_score > 0:
        return "상승"

    if direction_score < 0:
        return "하락"

    return "혼조"


def build_flow_from_group(
    category: str,
    signals: list[Signal],
) -> Flow:
    category_name = CATEGORY_NAMES.get(category, category)
    group_direction = determine_group_direction(signals)

    sorted_signals = sorted(
        signals,
        key=get_signal_sort_score,
        reverse=True,
    )

    strongest_signal = sorted_signals[0]

    if all(
        signal.signal_type == "news"
        for signal in signals
    ):
        flow_title = f"{category_name} 흐름"
    else:
        flow_title = f"{category_name} {group_direction} 흐름"

    flow = Flow(
        title=flow_title,
        target_asset=strongest_signal.symbol,
        summary=" ".join(
            build_signal_summary(signal)
            for signal in sorted_signals
        ),
    )

    for order_index, signal in enumerate(
        sorted_signals,
        start=1,
    ):
        signal_summary = build_signal_summary(signal)
        scores = calculate_evidence_scores(signal)

        node = FlowNode(
            order_index=order_index,
            title=build_signal_title(signal),
            category=get_signal_category(signal),
            description=signal_summary,
            occurred_at=signal.occurred_at,
            evidence_level=EVIDENCE_LEVELS.get(
                signal.severity,
                "moderate",
            ),
        )

        evidence = Evidence(
            evidence_type=get_evidence_type(signal),
            title=(
                signal.title
                if signal.signal_type == "news"
                else f"{signal.name} 원천 데이터"
            ),
            source=signal.source,
            url=get_source_url(signal),
            content_summary=signal_summary,
            relation_score=scores.relation_score,
            impact_score=scores.impact_score,
            time_score=scores.time_score,
            reliability_score=scores.reliability_score,
            published_at=signal.occurred_at,
        )

        node.evidences.append(evidence)
        flow.nodes.append(node)

    return flow


def discover_flows(signals: list[Signal]) -> list[Flow]:
    if not signals:
        raise ValueError(
            "Flow를 생성하려면 Signal이 하나 이상 필요합니다."
        )

    grouped_signals: dict[str, list[Signal]] = defaultdict(list)

    for signal in signals:
        category = get_signal_category(signal)
        grouped_signals[category].append(signal)

    flows = []

    for category, category_signals in grouped_signals.items():
        flow = build_flow_from_group(
            category=category,
            signals=category_signals,
        )
        flows.append(flow)

    return flows


def discover_flow(signals: list[Signal]) -> Flow:
    flows = discover_flows(signals)

    if len(flows) != 1:
        raise ValueError(
            "discover_flow는 동일 카테고리 Signal에만 사용할 수 있습니다."
        )

    return flows[0]