from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Flow, FlowNode
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_flow_answer(
    db: Session,
    flow_id: int,
    question: str,
) -> str:
    stmt = (
        select(Flow)
        .where(Flow.id == flow_id)
        .options(
            selectinload(Flow.nodes)
            .selectinload(FlowNode.evidences)
        )
    )

    flow = db.scalar(stmt)

    if flow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flow {flow_id}를 찾을 수 없습니다.",
        )

    sorted_nodes = sorted(
        flow.nodes,
        key=lambda node: node.order_index,
    )

    flow_path = " → ".join(node.title for node in sorted_nodes)

    evidence_count = sum(
        len(node.evidences)
        for node in sorted_nodes
    )

    answer = (
        f"{flow.summary}\n\n"
        f"주요 흐름: {flow_path}\n"
        f"확인된 근거: {evidence_count}개"
    )

    return answer