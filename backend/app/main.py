from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from fastapi import Depends

from app.routers.flows import router as flows_router
from app.routers.home import router as home_router


app = FastAPI(
    title="SignalFlow API",
    description="시장의 흐름을 근거 기반으로 설명하는 경제 인텔리전스 플랫폼",
    version="0.1.0",
)

app.include_router(home_router)
app.include_router(flows_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to SignalFlow",
        "docs": "/docs",
    }

@app.get("/api/health/db", tags=["Health"])
def check_database(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar_one()

    return {
        "status": "ok",
        "database": "connected",
        "result": result,
    }