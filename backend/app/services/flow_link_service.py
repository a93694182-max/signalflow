from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException, status

from app.core.flow_linking import discover_flow_links
from app.models import Flow, FlowLink


def create_flow_links(
    db: Session,
    flows: list[Flow],
) -> list[FlowLink]:
    candidates = discover_flow_links(flows)
    saved_links = []

    try:
        for candidate in candidates:
            stmt = select(FlowLink).where(
                FlowLink.source_flow_id
                == candidate.source_flow.id,
                FlowLink.target_flow_id
                == candidate.target_flow.id,
                FlowLink.relation_type
                == candidate.relation_type,
            )

            existing_link = db.scalar(stmt)

            if existing_link is not None:
                existing_link.score = candidate.score
                existing_link.reason = candidate.reason
                saved_links.append(existing_link)
                continue

            flow_link = FlowLink(
                source_flow_id=candidate.source_flow.id,
                target_flow_id=candidate.target_flow.id,
                relation_type=candidate.relation_type,
                score=candidate.score,
                reason=candidate.reason,
            )

            db.add(flow_link)
            saved_links.append(flow_link)

        db.commit()

    except Exception:
        db.rollback()
        raise

    return saved_links


def get_why_trail(
    db: Session,
    flow_id: int,
) -> dict:
    flow = db.get(Flow, flow_id)

    if flow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flow {flow_id}를 찾을 수 없습니다.",
        )

    stmt = (
        select(FlowLink)
        .where(
            FlowLink.target_flow_id == flow_id,
        )
        .options(
            selectinload(FlowLink.source_flow),
            selectinload(FlowLink.target_flow),
        )
        .order_by(
            FlowLink.score.desc(),
        )
    )

    links = db.scalars(stmt).all()

    trail = [
        {
            "source_flow_id": link.source_flow_id,
            "source_title": link.source_flow.title,
            "target_flow_id": link.target_flow_id,
            "target_title": link.target_flow.title,
            "relation_type": link.relation_type,
            "score": link.score,
            "reason": link.reason,
        }
        for link in links
    ]

    return {
        "flow_id": flow.id,
        "title": flow.title,
        "trail_count": len(trail),
        "trail": trail,
    }