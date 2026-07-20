from __future__ import annotations

from dataclasses import dataclass

from app.models import Evidence, Flow


EVIDENCE_SCORE_WEIGHTS = {
    "relation": 0.3,
    "impact": 0.2,
    "time": 0.2,
    "reliability": 0.3,
}


@dataclass(frozen=True, slots=True)
class FlowRankingResult:
    flow: Flow
    score: float
    evidence_count: int


def calculate_evidence_total_score(evidence: Evidence) -> float:
    relation_score = evidence.relation_score or 0.0
    impact_score = evidence.impact_score or 0.0
    time_score = evidence.time_score or 0.0
    reliability_score = evidence.reliability_score or 0.0

    total_score = (
        relation_score * EVIDENCE_SCORE_WEIGHTS["relation"]
        + impact_score * EVIDENCE_SCORE_WEIGHTS["impact"]
        + time_score * EVIDENCE_SCORE_WEIGHTS["time"]
        + reliability_score * EVIDENCE_SCORE_WEIGHTS["reliability"]
    )

    return round(total_score, 3)


def get_flow_evidences(flow: Flow) -> list[Evidence]:
    return [
        evidence
        for node in flow.nodes
        for evidence in node.evidences
    ]


def calculate_flow_score(flow: Flow) -> float:
    evidences = get_flow_evidences(flow)

    if not evidences:
        return 0.0

    evidence_scores = [
        calculate_evidence_total_score(evidence)
        for evidence in evidences
    ]

    average_score = sum(evidence_scores) / len(evidence_scores)

    return round(average_score, 3)


def rank_flows(flows: list[Flow]) -> list[FlowRankingResult]:
    ranking_results = [
        FlowRankingResult(
            flow=flow,
            score=calculate_flow_score(flow),
            evidence_count=len(get_flow_evidences(flow)),
        )
        for flow in flows
    ]

    return sorted(
        ranking_results,
        key=lambda result: (
            result.score,
            result.evidence_count,
        ),
        reverse=True,
    )