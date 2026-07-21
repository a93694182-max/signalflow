from datetime import datetime, timedelta, timezone

from app.core.flow_linking import (
    build_flow_link_candidate,
    discover_flow_links,
)
from app.models import Evidence, Flow, FlowNode


def create_test_flow(
    flow_id: int,
    title: str,
    category: str,
    evidence_type: str,
    occurred_at: datetime,
) -> Flow:
    flow = Flow(
        id=flow_id,
        title=title,
        target_asset="MARKET",
        summary=title,
    )

    node = FlowNode(
        id=flow_id,
        order_index=1,
        title=title,
        category=category,
        occurred_at=occurred_at,
        evidence_level="strong",
    )

    evidence = Evidence(
        id=flow_id,
        evidence_type=evidence_type,
        title=title,
        source="Reuters",
        relation_score=0.9,
        impact_score=0.8,
        time_score=1.0,
        reliability_score=0.95,
    )

    node.evidences.append(evidence)
    flow.nodes.append(node)

    return flow


def test_news_flow_links_to_market_flow():
    now = datetime.now(timezone.utc)

    news_flow = create_test_flow(
        flow_id=1,
        title="금리 인상 가능성",
        category="monetary_policy",
        evidence_type="news",
        occurred_at=now,
    )

    market_flow = create_test_flow(
        flow_id=2,
        title="국내 증시 하락",
        category="domestic_stock",
        evidence_type="market_data",
        occurred_at=now + timedelta(hours=2),
    )

    candidate = build_flow_link_candidate(
        news_flow,
        market_flow,
    )

    assert candidate is not None
    assert candidate.relation_type == "potential_cause"
    assert candidate.score >= 0.5


def test_old_flow_is_not_linked():
    now = datetime.now(timezone.utc)

    news_flow = create_test_flow(
        flow_id=1,
        title="금리 인상 가능성",
        category="monetary_policy",
        evidence_type="news",
        occurred_at=now,
    )

    market_flow = create_test_flow(
        flow_id=2,
        title="국내 증시 하락",
        category="domestic_stock",
        evidence_type="market_data",
        occurred_at=now + timedelta(days=5),
    )

    candidate = build_flow_link_candidate(
        news_flow,
        market_flow,
    )

    assert candidate is None


def test_discovers_links_in_score_order():
    now = datetime.now(timezone.utc)

    news_flow = create_test_flow(
        flow_id=1,
        title="원유 공급 충격",
        category="geopolitics",
        evidence_type="news",
        occurred_at=now,
    )

    close_market_flow = create_test_flow(
        flow_id=2,
        title="원자재 상승",
        category="commodity",
        evidence_type="market_data",
        occurred_at=now + timedelta(hours=1),
    )

    late_market_flow = create_test_flow(
        flow_id=3,
        title="국내 증시 하락",
        category="domestic_stock",
        evidence_type="market_data",
        occurred_at=now + timedelta(hours=20),
    )

    links = discover_flow_links(
        [
            news_flow,
            close_market_flow,
            late_market_flow,
        ]
    )

    assert len(links) == 2
    assert links[0].target_flow.id == 2
    assert links[0].score > links[1].score