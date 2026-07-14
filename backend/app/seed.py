from datetime import datetime

from app.database import SessionLocal
from app.models import Evidence, Flow, FlowNode


def seed_database() -> None:
    db = SessionLocal()

    try:
        existing_flow = db.query(Flow).filter(Flow.id == 1).first()

        if existing_flow:
            print("Seed data already exists.")
            return

        flow = Flow(
            id=1,
            title="왜 오늘 코스피가 하락했을까?",
            target_asset="KOSPI",
            summary=(
                "미국 CPI가 예상치를 웃돌며 달러가 강세를 보였고, "
                "외국인 순매도와 반도체 업종 약세가 이어져 "
                "코스피 하락 압력이 커졌습니다."
            ),
        )

        nodes = [
            FlowNode(
                order_index=1,
                title="미국 CPI 예상치 상회",
                category="macro",
                description="미국 소비자물가지수가 시장 예상보다 높게 발표됐습니다.",
                occurred_at=datetime(2026, 7, 13, 8, 30),
                evidence_level="strong",
            ),
            FlowNode(
                order_index=2,
                title="달러 강세",
                category="fx",
                description="금리 인하 기대가 약해지며 달러 가치가 상승했습니다.",
                occurred_at=datetime(2026, 7, 13, 9, 10),
                evidence_level="strong",
            ),
            FlowNode(
                order_index=3,
                title="외국인 순매도 확대",
                category="fund_flow",
                description="환율 부담이 커지면서 외국인의 국내 주식 매도가 확대됐습니다.",
                occurred_at=datetime(2026, 7, 13, 9, 25),
                evidence_level="moderate",
            ),
            FlowNode(
                order_index=4,
                title="반도체 업종 약세",
                category="sector",
                description="외국인 매도가 반도체 대형주에 집중되며 업종이 하락했습니다.",
                occurred_at=datetime(2026, 7, 13, 9, 40),
                evidence_level="moderate",
            ),
            FlowNode(
                order_index=5,
                title="코스피 하락",
                category="market",
                description="대형 반도체주의 하락으로 코스피가 약세를 보였습니다.",
                occurred_at=datetime(2026, 7, 13, 9, 50),
                evidence_level="strong",
            ),
        ]

        flow.nodes = nodes

        nodes[0].evidences = [
            Evidence(
                evidence_type="economic_indicator",
                title="미국 CPI 발표",
                source="Sample Data",
                content_summary="미국 CPI가 시장 예상치를 상회했습니다.",
                relation_score=0.95,
                impact_score=0.90,
                time_score=1.0,
                reliability_score=0.90,
            )
        ]

        db.add(flow)
        db.commit()

        print("Seed data inserted successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()