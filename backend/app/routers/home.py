from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.home import HomeResponse
from app.services.home_service import get_home_data


router = APIRouter(
    prefix="/api/home",
    tags=["Home"],
)


@router.get(
    "",
    response_model=HomeResponse,
)
def get_home(
    db: Session = Depends(get_db),
):
    return get_home_data(db)