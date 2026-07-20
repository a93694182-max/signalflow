from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.core.why_analysis import analyze_flow
from app.services.flow_service import get_flow_trace


@dataclass(frozen=True, slots=True)
class FlowAnswer:
    answer: str
    confidence_score: float
    confidence_level: str
    primary_cause: str | None
    flow_path: list[str]
    evidence_count: int


def generate_flow_answer(
    db: Session,
    flow_id: int,
    question: str,
) -> FlowAnswer:
    flow = get_flow_trace(
        db=db,
        flow_id=flow_id,
    )

    why_result = analyze_flow(flow)

    sorted_nodes = sorted(
        flow.nodes,
        key=lambda node: node.order_index,
    )

    flow_path = [
        node.title
        for node in sorted_nodes
    ]

    evidence_count = sum(
        len(node.evidences)
        for node in sorted_nodes
    )

    if why_result.primary_cause is None:
        answer = (
            f"'{question}'에 답할 수 있는 "
            "충분한 근거가 아직 없습니다."
        )
        primary_cause = None
    else:
        primary_cause = why_result.primary_cause.title

        answer = (
            f"{flow.title}의 가장 유력한 원인은 "
            f"'{primary_cause}'입니다. "
            f"현재 {evidence_count}개의 근거를 확인했으며, "
            f"분석 신뢰도는 "
            f"{why_result.confidence_score:.1%}입니다."
        )

    return FlowAnswer(
        answer=answer,
        confidence_score=why_result.confidence_score,
        confidence_level=why_result.confidence_level,
        primary_cause=primary_cause,
        flow_path=flow_path,
        evidence_count=evidence_count,
    )