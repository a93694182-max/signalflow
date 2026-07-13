from fastapi import FastAPI

from app.routers.home import router as home_router


app = FastAPI(
    title="SignalFlow API",
    description="시장의 흐름을 근거 기반으로 설명하는 경제 인텔리전스 플랫폼",
    version="0.1.0",
)

app.include_router(home_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to SignalFlow",
        "docs": "/docs",
    }