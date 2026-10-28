from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI
from sqlalchemy.orm import Session

from app.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_ENABLED,
)
from app.core.why_analysis import analyze_flow
from app.services.flow_link_service import get_why_trail
from app.services.flow_service import get_flow_trace


@dataclass(frozen=True, slots=True)
class FlowAnswer:
    answer: str
    confidence_score: float
    confidence_level: str
    primary_cause: str | None
    flow_path: list[str]
    evidence_count: int
    answer_source: str
    why_trail: list[str]


def generate_openai_answer(
    question: str,
    flow_title: str,
    primary_cause: str,
    confidence_score: float,
    why_trail: list[str],
    evidences: list[str],
) -> str | None:
    if not OPENAI_ENABLED or not OPENAI_API_KEY:
        return None

    trail_text = "\n".join(f"- {cause}" for cause in why_trail)

    evidence_text = "\n".join(f"- {evidence}" for evidence in evidences[:10])

    prompt = f"""
당신은 경제·금융 시장 분석 보조 AI입니다.

다음에 제공된 분석 결과와 근거만 사용하여 질문에 답변하세요.

규칙:
1. 제공되지 않은 사실을 만들어내지 마세요.
2. 인과관계가 확실하지 않으면 원인 후보라고 표현하세요.
3. 근거가 부족하면 불확실성을 명시하세요.
4. 한국어로 간결하게 설명하세요.
5. 최대 5문장으로 답변하세요.

[질문]
{question}

[분석 대상]
{flow_title}

[주요 원인 후보]
{primary_cause}

[분석 신뢰도]
{confidence_score:.1%}

[Why Trail]
{trail_text}

[Evidence]
{evidence_text}
"""

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
        )

        answer = response.output_text.strip()

        return answer or None

    except Exception as error:
        print(f"[OpenAI ERROR] {type(error).__name__}: {error}")
        return None


def generate_flow_answer(
    db: Session,
    flow_id: int,
    question: str,
) -> FlowAnswer:
    flow = get_flow_trace(
        db=db,
        flow_id=flow_id,
    )

    why_result = analyze_flow(flow)

    trail_result = get_why_trail(
        db=db,
        flow_id=flow_id,
    )

    why_trail = []

    for step in trail_result["trail"]:
        source_title = step["source_title"]

        if source_title not in why_trail:
            why_trail.append(source_title)

    why_trail = why_trail[:3]

    why_trail.append(flow.title)

    sorted_nodes = sorted(
        flow.nodes,
        key=lambda node: node.order_index,
    )

    flow_path = [node.title for node in sorted_nodes]

    evidences = [evidence.title for node in sorted_nodes for evidence in node.evidences]

    evidence_count = len(evidences)

    if why_result.primary_cause is None:
        answer = f"'{question}'에 답할 수 있는 충분한 근거가 아직 없습니다."

        primary_cause = None
        answer_source = "template"

    else:
        primary_cause = why_result.primary_cause.title

        external_causes = why_trail[:-1]

        if external_causes:
            cause_text = ", ".join(f"'{cause}'" for cause in external_causes)

            template_answer = (
                f"{flow.title}과 연결된 외부 원인 후보는 "
                f"{cause_text}입니다. "
                f"내부 시장 신호 중에서는 "
                f"'{primary_cause}'가 가장 강하게 나타났습니다. "
                f"분석 신뢰도는 "
                f"{why_result.confidence_score:.1%}입니다."
            )

        else:
            template_answer = (
                f"{flow.title}의 가장 강한 내부 신호는 "
                f"'{primary_cause}'입니다. "
                f"현재 {evidence_count}개의 근거를 확인했으며, "
                f"분석 신뢰도는 "
                f"{why_result.confidence_score:.1%}입니다."
            )

        openai_answer = generate_openai_answer(
            question=question,
            flow_title=flow.title,
            primary_cause=primary_cause,
            confidence_score=(why_result.confidence_score),
            why_trail=why_trail,
            evidences=evidences,
        )

        if openai_answer is not None:
            answer = openai_answer
            answer_source = "openai"

        else:
            answer = template_answer
            answer_source = "template"

    return FlowAnswer(
        answer=answer,
        confidence_score=why_result.confidence_score,
        confidence_level=why_result.confidence_level,
        primary_cause=primary_cause,
        flow_path=flow_path,
        evidence_count=evidence_count,
        answer_source=answer_source,
        why_trail=why_trail,
    )
