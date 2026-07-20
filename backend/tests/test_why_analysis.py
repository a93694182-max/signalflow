from app.core.why_analysis import analyze_flow
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
assert result.confidence_level == "high"

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