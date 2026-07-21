from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.core.flow_ranking import calculate_flow_quality_score
from app.models import Flow


MAX_LINK_HOURS = 72
MIN_LINK_SCORE = 0.5

MARKET_CATEGORIES = {
    "domestic_stock",
    "currency",
    "crypto",
    "commodity",
    "market",
}

CATEGORY_LINKS = {
    "economic": MARKET_CATEGORIES,
    "monetary_policy": {
        "domestic_stock",
        "currency",
        "market",
    },
    "geopolitics": {
        "domestic_stock",
        "currency",
        "commodity",
        "market",
    },
    "commodity": {
        "commodity",
        "domestic_stock",
        "market",
    },
    "crypto": {
        "crypto",
        "market",
    },
    "technology": {
        "domestic_stock",
        "market",
    },
    "corporate": {
        "domestic_stock",
        "market",
    },
    "general": MARKET_CATEGORIES,
}


@dataclass(frozen=True, slots=True)
class FlowLinkCandidate:
    source_flow: Flow
    target_flow: Flow
    relation_type: str
    score: float
    reason: str


def get_evidence_types(flow: Flow) -> set[str]:
    return {
        evidence.evidence_type
        for node in flow.nodes
        for evidence in node.evidences
    }


def get_flow_categories(flow: Flow) -> set[str]:
    return {
        node.category
        for node in flow.nodes
    }


def get_flow_time(flow: Flow) -> datetime | None:
    occurred_times = [
        node.occurred_at
        for node in flow.nodes
        if node.occurred_at is not None
    ]

    if not occurred_times:
        return None

    return min(occurred_times)


def calculate_category_score(
    source_flow: Flow,
    target_flow: Flow,
) -> float:
    source_categories = get_flow_categories(source_flow)
    target_categories = get_flow_categories(target_flow)

    for source_category in source_categories:
        allowed_targets = CATEGORY_LINKS.get(
            source_category,
            set(),
        )

        if allowed_targets & target_categories:
            return 1.0

    return 0.0


def calculate_time_score(
    source_flow: Flow,
    target_flow: Flow,
) -> float:
    source_time = get_flow_time(source_flow)
    target_time = get_flow_time(target_flow)

    if source_time is None or target_time is None:
        return 0.0

    if source_time.tzinfo is None:
        source_time = source_time.replace(
            tzinfo=timezone.utc,
        )

    if target_time.tzinfo is None:
        target_time = target_time.replace(
            tzinfo=timezone.utc,
        )

    difference_hours = abs(
        (target_time - source_time).total_seconds()
    ) / 3600

    if difference_hours > MAX_LINK_HOURS:
        return 0.0

    return round(
        1.0 - difference_hours / MAX_LINK_HOURS,
        3,
    )


def build_flow_link_candidate(
    source_flow: Flow,
    target_flow: Flow,
) -> FlowLinkCandidate | None:
    if source_flow.id == target_flow.id:
        return None

    source_types = get_evidence_types(source_flow)
    target_types = get_evidence_types(target_flow)

    if not source_types & {"news", "economic_data"}:
        return None

    if "market_data" not in target_types:
        return None

    category_score = calculate_category_score(
        source_flow,
        target_flow,
    )
    time_score = calculate_time_score(
        source_flow,
        target_flow,
    )

    if category_score == 0.0 or time_score == 0.0:
        return None

    quality_score = calculate_flow_quality_score(
        source_flow,
    )

    score = round(
        category_score * 0.5
        + time_score * 0.3
        + quality_score * 0.2,
        3,
    )

    if score < MIN_LINK_SCORE:
        return None

    reason = (
        f"카테고리 연관성 {category_score:.2f}, "
        f"시간 근접성 {time_score:.2f}, "
        f"근거 품질 {quality_score:.2f}"
    )

    return FlowLinkCandidate(
        source_flow=source_flow,
        target_flow=target_flow,
        relation_type="potential_cause",
        score=score,
        reason=reason,
    )


def discover_flow_links(
    flows: list[Flow],
) -> list[FlowLinkCandidate]:
    candidates = []

    for source_flow in flows:
        for target_flow in flows:
            candidate = build_flow_link_candidate(
                source_flow,
                target_flow,
            )

            if candidate is not None:
                candidates.append(candidate)

    return sorted(
        candidates,
        key=lambda candidate: candidate.score,
        reverse=True,
    )