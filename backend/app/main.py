from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.flows import router as flows_router
from app.routers.home import router as home_router
from app.routers.evidence import router as evidence_router
from app.routers.ask import router as ask_router
from app.routers.market import router as market_router
from app.routers.economic import router as economic_router


app = FastAPI(
    title="SignalFlow API",
    description="시장의 흐름을 근거 기반으로 설명하는 경제 인텔리전스 플랫폼",
    version="0.1.0",
)

app.include_router(home_router)
app.include_router(flows_router)
app.include_router(evidence_router)
app.include_router(ask_router)
app.include_router(market_router)
app.include_router(economic_router)


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