from unittest.mock import Mock, patch

from app.services.ai_service import generate_openai_answer

@patch("app.services.ai_service.OPENAI_ENABLED", True)
@patch("app.services.ai_service.OPENAI_API_KEY", "test-key")
@patch("app.services.ai_service.OpenAI")
def test_generate_openai_answer_success(mock_openai):
    mock_client = Mock()
    mock_client.responses.create.return_value.output_text = (
        "외국인 매수세가 코스피 상승의 원인 후보로 분석됩니다."
    )
    mock_openai.return_value = mock_client

    result = generate_openai_answer(
        question="코스피가 왜 상승했어?",
        flow_title="코스피 상승 흐름",
        primary_cause="외국인 매수세",
        confidence_score=0.85,
        why_trail=["외국인 순매수 증가"],
        evidences=["코스피 지수 1.2% 상승"],
    )

    assert result is not None
    assert "외국인 매수세" in result

    mock_openai.assert_called_once()
    mock_client.responses.create.assert_called_once()


@patch("app.services.ai_service.OPENAI_ENABLED", True)
@patch("app.services.ai_service.OPENAI_API_KEY", "test-key")
@patch("app.services.ai_service.OpenAI")
def test_generate_openai_answer_failure(mock_openai):
    mock_client = Mock()
    mock_client.responses.create.side_effect = Exception("API Error")
    mock_openai.return_value = mock_client

    result = generate_openai_answer(
        question="코스피가 왜 상승했어?",
        flow_title="코스피 상승 흐름",
        primary_cause="외국인 매수세",
        confidence_score=0.85,
        why_trail=["외국인 순매수 증가"],
        evidences=["코스피 지수 1.2% 상승"],
    )

    assert result is None


@patch("app.services.ai_service.generate_openai_answer", return_value=None)
@patch("app.services.ai_service.get_why_trail")
@patch("app.services.ai_service.analyze_flow")
@patch("app.services.ai_service.get_flow_trace")
def test_generate_flow_answer_fallback(
    mock_get_flow_trace,
    mock_analyze_flow,
    mock_get_why_trail,
    mock_generate_openai_answer,
):
    from app.services.ai_service import generate_flow_answer

    flow = Mock()
    flow.title = "코스피 상승 흐름"

    node = Mock()
    node.title = "코스피 상승"
    node.order_index = 0

    evidence = Mock()
    evidence.title = "코스피 지수 1.2% 상승"

    node.evidences = [evidence]
    flow.nodes = [node]

    mock_get_flow_trace.return_value = flow

    why_result = Mock()
    why_result.primary_cause.title = "외국인 매수세"
    why_result.confidence_score = 0.85
    why_result.confidence_level = "high"

    mock_analyze_flow.return_value = why_result

    mock_get_why_trail.return_value = {
        "trail": [{"source_title": "외국인 순매수 증가"}]
    }

    result = generate_flow_answer(
        db=Mock(),
        flow_id=1,
        question="코스피가 왜 상승했어?",
    )

    assert result.answer_source == "template"
    assert result.primary_cause == "외국인 매수세"
    assert result.evidence_count == 1
    assert result.confidence_score == 0.85
    assert "외국인 순매수 증가" in result.answer

    mock_generate_openai_answer.assert_called_once()

    assert (
        mock_generate_openai_answer.call_args.kwargs["evidences"]
        == ["코스피 지수 1.2% 상승"]
    )


@patch(
    "app.services.ai_service.generate_openai_answer",
    return_value="외국인 매수세가 코스피 상승의 원인 후보입니다.",
)
@patch("app.services.ai_service.get_why_trail")
@patch("app.services.ai_service.analyze_flow")
@patch("app.services.ai_service.get_flow_trace")
def test_generate_flow_answer_ai_success(
    mock_get_flow_trace,
    mock_analyze_flow,
    mock_get_why_trail,
    mock_generate_openai_answer,
):
    flow = Mock()
    flow.title = "코스피 상승 흐름"
    flow.nodes = []

    mock_get_flow_trace.return_value = flow

    why_result = Mock()
    why_result.primary_cause.title = "외국인 매수세"
    why_result.confidence_score = 0.85
    why_result.confidence_level = "high"

    mock_analyze_flow.return_value = why_result
    mock_get_why_trail.return_value = {"trail": []}

    from app.services.ai_service import generate_flow_answer

    result = generate_flow_answer(
        db=Mock(),
        flow_id=1,
        question="코스피가 왜 상승했어?",
    )

    assert result.answer_source == "openai"
    assert "외국인 매수세" in result.answer
    mock_generate_openai_answer.assert_called_once()


@patch("app.services.ai_service.generate_openai_answer")
@patch("app.services.ai_service.get_why_trail")
@patch("app.services.ai_service.analyze_flow")
@patch("app.services.ai_service.get_flow_trace")
def test_generate_flow_answer_no_cause(
    mock_get_flow_trace,
    mock_analyze_flow,
    mock_get_why_trail,
    mock_generate_openai_answer,
):
    flow = Mock()
    flow.title = "코스피 상승 흐름"
    flow.nodes = []

    mock_get_flow_trace.return_value = flow

    why_result = Mock()
    why_result.primary_cause = None
    why_result.confidence_score = 0.0
    why_result.confidence_level = "low"

    mock_analyze_flow.return_value = why_result
    mock_get_why_trail.return_value = {"trail": []}

    from app.services.ai_service import generate_flow_answer

    result = generate_flow_answer(
        db=Mock(),
        flow_id=1,
        question="코스피가 왜 상승했어?",
    )

    assert result.answer_source == "template"
    assert result.primary_cause is None
    assert "충분한 근거가 아직 없습니다" in result.answer

    mock_generate_openai_answer.assert_not_called()