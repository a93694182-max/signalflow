from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Evidence, Flow, FlowNode
from app.services.flow_link_service import create_flow_links
from app.services.flow_service import get_flow_why_analysis


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


def test_cross_flow_why_analysis():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

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

    with Session(engine) as db:
        db.add_all([
            news_flow,
            market_flow,
        ])
        db.commit()

        create_flow_links(
            db=db,
            flows=[
                news_flow,
                market_flow,
            ],
        )

        result = get_flow_why_analysis(
            db=db,
            flow_id=market_flow.id,
        )

        assert result.analysis.primary_cause is not None
        assert len(result.external_causes) == 1
        assert (
            result.external_causes[0]["source_title"]
            == "금리 인상 가능성"
        )
        assert "외부 원인 후보" in result.summary