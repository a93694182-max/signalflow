from fastapi import APIRouter

from app.schemas.flow import FlowTraceResponse
from app.services.flow_service import get_flow_trace

router = APIRouter(
    prefix="/api/flows",
    tags=["Flows"],
)


@router.get(
    "/{flow_id}/trace",
    response_model=FlowTraceResponse,
)
def read_flow_trace(flow_id: int):
    return get_flow_trace(flow_id)