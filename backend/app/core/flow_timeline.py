from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.models import Flow


@dataclass(frozen=True, slots=True)
class TimelineEvent:
    node_id: int
    order_index: int
    title: str
    category: str
    description: str | None
    occurred_at: datetime | None
    evidence_level: str
    evidence_count: int


@dataclass(frozen=True, slots=True)
class FlowTimelineResult:
    flow: Flow
    events: list[TimelineEvent]


def build_flow_timeline(
    flow: Flow,
) -> FlowTimelineResult:
    sorted_nodes = sorted(
        flow.nodes,
        key=lambda node: (
            node.occurred_at is None,
            node.occurred_at.timestamp()
            if node.occurred_at
            else 0,
            node.order_index,
        ),
    )

    events = [
        TimelineEvent(
            node_id=node.id,
            order_index=node.order_index,
            title=node.title,
            category=node.category,
            description=node.description,
            occurred_at=node.occurred_at,
            evidence_level=node.evidence_level,
            evidence_count=len(node.evidences),
        )
        for node in sorted_nodes
    ]

    return FlowTimelineResult(
        flow=flow,
        events=events,
    )