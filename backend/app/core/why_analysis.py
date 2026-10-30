from __future__ import annotations

from dataclasses import dataclass

from app.core.flow_ranking import (
    EVIDENCE_COUNT_TARGET,
    calculate_coverage_score,
    calculate_evidence_total_score,
)
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

def calculate_confidence_score(
    quality_score: float,
    evidence_count: int,
) -> float:
    if evidence_count <= 0:
        return 0.0

    coverage_score = calculate_coverage_score(
        evidence_count,
    )

    confidence_score = (
        quality_score * 0.85
        + coverage_score * 0.15
    )

    if evidence_count == 1:
        confidence_score = min(confidence_score, 0.59)

    elif evidence_count < EVIDENCE_COUNT_TARGET:
        confidence_score = min(confidence_score, 0.79)

    return round(confidence_score, 3)

def calculate_confidence_breakdown(
    quality_score: float,
    evidence_count: int,
) -> dict:
    coverage_score = calculate_coverage_score(
        evidence_count,
    )

    raw_score = (
        quality_score * 0.85
        + coverage_score * 0.15
    )

    if evidence_count <= 0:
        confidence_cap = 0.0
    elif evidence_count == 1:
        confidence_cap = 0.59
    elif evidence_count < EVIDENCE_COUNT_TARGET:
        confidence_cap = 0.79
    else:
        confidence_cap = None

    confidence_score = calculate_confidence_score(
        quality_score=quality_score,
        evidence_count=evidence_count,
    )

    return {
        "quality_score": round(quality_score, 3),
        "coverage_score": coverage_score,
        "quality_weight": 0.85,
        "coverage_weight": 0.15,
        "evidence_count": evidence_count,
        "raw_score": round(raw_score, 3),
        "confidence_cap": confidence_cap,
        "confidence_score": confidence_score,
        "confidence_level": get_confidence_level(confidence_score),
    }


def explain_cause_ranking(
    causes: list[WhyCause],
) -> list[dict]:
    ranked_causes = sorted(
        causes,
        key=lambda cause: (
            cause.score,
            cause.evidence_count,
        ),
        reverse=True,
    )

    explanations = []

    for rank, cause in enumerate(ranked_causes, start=1):
        if cause.evidence_count == 0:
            reason = "분석 가능한 Evidence 없음"
        elif rank == 1:
            reason = "Evidence 평균 점수가 가장 높은 원인 후보"
        else:
            reason = "Evidence 평균 점수와 근거 개수를 기준으로 정렬"

        explanations.append(
            {
                "rank": rank,
                "node_id": cause.node_id,
                "title": cause.title,
                "score": cause.score,
                "evidence_count": cause.evidence_count,
                "reason": reason,
            }
        )

    return explanations


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
        quality_score = (
            sum(
                cause.score * cause.evidence_count
                for cause in scored_causes
            )
            / total_evidence_count
        )
    else:
        quality_score = 0.0

    confidence_score = calculate_confidence_score(
        quality_score=quality_score,
        evidence_count=total_evidence_count,
    )

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