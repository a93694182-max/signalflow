from app.core.flow_ranking import rank_flows
from app.models import Evidence, Flow, FlowNode


def create_flow(
    title: str,
    evidence_scores: list[tuple[float, float, float, float]],
) -> Flow:
    flow = Flow(
        title=title,
        target_asset="TEST",
        summary="테스트 Flow",
    )

    node = FlowNode(
        order_index=1,
        title=f"{title} Node",
        category="test",
        description="테스트 Node",
        evidence_level="moderate",
    )

    for index, scores in enumerate(evidence_scores, start=1):
        relation, impact, time, reliability = scores

        evidence = Evidence(
            evidence_type="news",
            title=f"Evidence {index}",
            source="test",
            relation_score=relation,
            impact_score=impact,
            time_score=time,
            reliability_score=reliability,
        )

        node.evidences.append(evidence)

    flow.nodes.append(node)

    return flow


flows = [
    create_flow(
        "중동 긴장 흐름",
        [
            (0.9, 0.8, 1.0, 0.95),
            (0.85, 0.7, 0.9, 0.9),
        ],
    ),
    create_flow(
        "원자재 상승 흐름",
        [
            (1.0, 0.7, 0.9, 0.9),
        ],
    ),
    create_flow(
        "신뢰도 낮은 뉴스 흐름",
        [
            (0.6, 0.4, 0.4, 0.5),
        ],
    ),
]

ranked_flows = rank_flows(flows)

for rank, result in enumerate(ranked_flows, start=1):
    print("=" * 60)
    print(f"rank: {rank}")
    print(f"title: {result.flow.title}")
    print(f"score: {result.score}")
    print(f"evidence_count: {result.evidence_count}")