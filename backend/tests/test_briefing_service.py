from datetime import datetime, timezone
from unittest.mock import Mock, patch

from app.services.briefing_service import get_daily_briefing


def test_daily_briefing_without_flows():
    db = Mock()

    with patch(
        "app.services.briefing_service.get_ranked_flows",
        return_value=[],
    ):
        result = get_daily_briefing(db)

    assert result["headline"] == "오늘 생성된 주요 시장 흐름이 없습니다."
    assert result["top_flows"] == []
    assert result["key_causes"] == []


def test_daily_briefing_with_ranked_flows():
    db = Mock()

    flow = Mock()
    flow.id = 1
    flow.title = "원자재 상승 흐름"
    flow.target_asset = "CL=F"
    flow.created_at = datetime.now(timezone.utc)

    ranked_result = Mock()
    ranked_result.flow = flow
    ranked_result.score = 0.9

    why_result = Mock()
    why_result.summary = "원자재 상승의 주요 원인을 분석했습니다."
    why_result.external_causes = [
        {"source_title": "주요 뉴스 흐름"},
    ]

    with (
        patch(
            "app.services.briefing_service.get_ranked_flows",
            return_value=[ranked_result],
        ),
        patch(
            "app.services.briefing_service.get_flow_why_analysis",
            return_value=why_result,
        ),
    ):
        result = get_daily_briefing(db)

    assert result["headline"] == "원자재 상승 흐름"
    assert result["summary"] == "원자재 상승의 주요 원인을 분석했습니다."
    assert len(result["top_flows"]) == 1
    assert result["top_flows"][0]["flow_id"] == 1
    assert result["top_flows"][0]["target_asset"] == "CL=F"
    assert result["key_causes"] == ["주요 뉴스 흐름"]