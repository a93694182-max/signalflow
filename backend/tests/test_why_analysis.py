from app.core.why_analysis import (
    WhyCause,
    analyze_flow,
    calculate_confidence_score,
    calculate_confidence_breakdown,
    explain_cause_ranking,
)
from app.models import Evidence, Flow, FlowNode


def create_node(
    node_id: int,
    title: str,
    scores: list[tuple[float, float, float, float]],
) -> FlowNode:
    node = FlowNode(
        id=node_id,
        order_index=node_id,
        title=title,
        category="market",
        description=f"{title} 설명",
        evidence_level="moderate",
    )

    for index, scores_item in enumerate(
        scores,
        start=1,
    ):
        relation, impact, time, reliability = scores_item

        evidence = Evidence(
            id=node_id * 10 + index,
            evidence_type="news",
            title=f"Evidence {index}",
            source="Reuters",
            relation_score=relation,
            impact_score=impact,
            time_score=time,
            reliability_score=reliability,
        )

        node.evidences.append(evidence)

    return node


flow = Flow(
    id=1,
    title="국내 증시 하락 흐름",
    target_asset="^KS11",
    summary="국내 증시 하락 테스트",
)

flow.nodes.extend(
    [
        create_node(
            node_id=1,
            title="금리 상승",
            scores=[
                (0.7, 0.6, 0.8, 0.9),
            ],
        ),
        create_node(
            node_id=2,
            title="외국인 매도",
            scores=[
                (1.0, 0.9, 1.0, 0.95),
            ],
        ),
    ]
)

result = analyze_flow(flow)

assert result.primary_cause is not None
assert result.primary_cause.node_id == 2
assert result.causes[0].score > result.causes[1].score
assert result.confidence_level == "medium"

print("=" * 60)
print(f"summary: {result.summary}")
print(f"confidence_score: {result.confidence_score}")
print(f"confidence_level: {result.confidence_level}")
print(f"primary_cause: {result.primary_cause.title}")

for cause in result.causes:
    print("-" * 60)
    print(f"cause: {cause.title}")
    print(f"score: {cause.score}")
    print(f"evidence_count: {cause.evidence_count}")

print("Why Analysis 테스트 통과")


def test_confidence_without_evidence():
    score = calculate_confidence_score(
        quality_score=0.95,
        evidence_count=0,
    )

    assert score == 0.0


def test_confidence_with_one_evidence():
    score = calculate_confidence_score(
        quality_score=0.95,
        evidence_count=1,
    )

    assert score == 0.59


def test_confidence_with_three_evidences():
    score = calculate_confidence_score(
        quality_score=0.95,
        evidence_count=3,
    )

    assert score == 0.79


def test_confidence_with_five_evidences():
    score = calculate_confidence_score(
        quality_score=0.95,
        evidence_count=5,
    )

    assert score == 0.958


def test_confidence_breakdown():
    result = calculate_confidence_breakdown(
        quality_score=0.95,
        evidence_count=3,
    )

    assert result["quality_score"] == 0.95
    assert result["coverage_score"] == 0.6
    assert result["raw_score"] == 0.897
    assert result["confidence_cap"] == 0.79
    assert result["confidence_score"] == 0.79
    assert result["confidence_level"] == "medium"


def test_confidence_breakdown_without_evidence():
    result = calculate_confidence_breakdown(
        quality_score=0.0,
        evidence_count=0,
    )

    assert result["evidence_count"] == 0
    assert result["confidence_cap"] == 0.0
    assert result["confidence_score"] == 0.0
    assert result["confidence_level"] == "low"


def test_confidence_breakdown_without_cap():
    result = calculate_confidence_breakdown(
        quality_score=0.95,
        evidence_count=5,
    )

    assert result["coverage_score"] == 1.0
    assert result["confidence_cap"] is None
    assert result["confidence_score"] == 0.958
    assert result["confidence_level"] == "high"

def test_cause_ranking_explanation():
    explanations = explain_cause_ranking(
        result.causes,
    )

    assert explanations[0]["rank"] == 1
    assert explanations[0]["node_id"] == 2
    assert explanations[0]["score"] > explanations[1]["score"]
    assert explanations[0]["reason"] == (
        "Evidence 평균 점수가 가장 높은 원인 후보"
    )


def test_cause_ranking_without_evidence():
    empty_flow = Flow(
        id=2,
        title="근거 없는 흐름",
        target_asset="^KS11",
    )

    empty_flow.nodes.append(
        create_node(
            node_id=3,
            title="근거 없는 원인",
            scores=[],
        )
    )

    analysis = analyze_flow(empty_flow)
    explanations = explain_cause_ranking(analysis.causes)

    assert explanations[0]["rank"] == 1
    assert explanations[0]["evidence_count"] == 0
    assert explanations[0]["reason"] == "분석 가능한 Evidence 없음"


def test_cause_ranking_tie_breaker():
    causes = [
        WhyCause(
            node_id=1,
            title="원인 A",
            category="market",
            description=None,
            score=0.8,
            evidence_count=1,
        ),
        WhyCause(
            node_id=2,
            title="원인 B",
            category="market",
            description=None,
            score=0.8,
            evidence_count=3,
        ),
    ]

    explanations = explain_cause_ranking(causes)

    assert explanations[0]["node_id"] == 2
    assert explanations[1]["node_id"] == 1


def test_primary_cause_matches_ranking():
    analysis = analyze_flow(flow)
    explanations = explain_cause_ranking(analysis.causes)

    assert analysis.primary_cause is not None
    assert analysis.primary_cause.node_id == explanations[0]["node_id"]


def test_confidence_breakdown_matches_analysis():
    analysis = analyze_flow(flow)

    evidence_count = sum(
        cause.evidence_count
        for cause in analysis.causes
    )

    quality_score = (
        sum(
            cause.score * cause.evidence_count
            for cause in analysis.causes
        )
        / evidence_count
    )

    breakdown = calculate_confidence_breakdown(
        quality_score=quality_score,
        evidence_count=evidence_count,
    )

    assert breakdown["confidence_score"] == analysis.confidence_score
    assert breakdown["confidence_level"] == analysis.confidence_level
    