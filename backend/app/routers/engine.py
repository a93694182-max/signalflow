from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.engine_service import run_signal_engine

router = APIRouter(
    prefix="/api/engine",
    tags=["engine"],
)


@router.post("/run")
def run_engine(db: Session = Depends(get_db)) -> dict:
    result = run_signal_engine(db)

    return {
        "collected_count": result["collected_count"],
        "filtered_count": result["filtered_count"],
        "flow_count": result["flow_count"],
        "flows": [
            {
                "id": flow.id,
                "title": flow.title,
                "target_asset": flow.target_asset,
            }
            for flow in result["flows"]
        ],
    }