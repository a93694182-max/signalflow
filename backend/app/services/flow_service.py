from fastapi import HTTPException, status

from app.data.mock_flows import MOCK_FLOWS


def get_flow_trace(flow_id: int) -> dict:
    flow = MOCK_FLOWS.get(flow_id)

    if flow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flow {flow_id}를 찾을 수 없습니다.",
        )

    return flow