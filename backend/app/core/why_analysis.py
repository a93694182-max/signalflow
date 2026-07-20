from __future__ import annotations

from dataclasses import dataclass

from app.core.flow_ranking import calculate_evidence_total_score
from app.models import Flow, FlowNode


@dataclass(frozen=True, slots=True)
class WhyCause:
    node_id: int
    title: str
    category: str
    description: str | None
    score: float
    evidence_count: int


@dataclass(frozen=True, slots=True)
class WhyAnalysisResult:
    flow: Flow
    summary: str
    confidence_score: float
    confidence_level: str
    primary_cause: WhyCause | None
    causes: list[WhyCause]


def get_confidence_level(score: float) -> str:
    if score >= 0.8:
        return "high"

    if score >= 0.6:
        return "medium"

    return "low"


def analyze_node(node: FlowNode) -> WhyCause:
    evidence_scores = [
        calculate_evidence_total_score(evidence)
        for evidence in node.evidences
    ]

    if evidence_scores:
        score = round(
            sum(evidence_scores) / len(evidence_scores),
            3,
        )
    else:
        score = 0.0

    return WhyCause(
        node_id=node.id,
        title=node.title,
        category=node.category,
        description=node.description,
        score=score,
        evidence_count=len(evidence_scores),
    )


def build_why_summary(
    flow: Flow,
    primary_cause: WhyCause | None,
) -> str:
    if primary_cause is None:
        return f"{flow.title}을 설명할 수 있는 근거가 아직 없습니다."

    return (
        f"{flow.title}의 가장 유력한 원인은 "
        f"'{primary_cause.title}'입니다."
    )


def analyze_flow(flow: Flow) -> WhyAnalysisResult:
    causes = [
        analyze_node(node)
        for node in flow.nodes
    ]

    causes.sort(
        key=lambda cause: (
            cause.score,
            cause.evidence_count,
        ),
        reverse=True,
    )

    scored_causes = [
        cause
        for cause in causes
        if cause.evidence_count > 0
    ]

    primary_cause = (
        scored_causes[0]
        if scored_causes
        else None
    )

    total_evidence_count = sum(
        cause.evidence_count
        for cause in scored_causes
    )

    if total_evidence_count:
        confidence_score = round(
            sum(
                cause.score * cause.evidence_count
                for cause in scored_causes
            )
            / total_evidence_count,
            3,
        )
    else:
        confidence_score = 0.0

    return WhyAnalysisResult(
        flow=flow,
        summary=build_why_summary(
            flow=flow,
            primary_cause=primary_cause,
        ),
        confidence_score=confidence_score,
        confidence_level=get_confidence_level(
            confidence_score,
        ),
        primary_cause=primary_cause,
        causes=causes,
    )