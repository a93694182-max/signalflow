from fastapi import APIRouter

router = APIRouter(
    prefix="/api/home",
    tags=["Home"],
)


@router.get("")
def get_home():
    return {
        "biggest_why": {
            "flow_id": 1,
            "title": "왜 오늘 코스피가 하락했을까?",
            "summary": "미국 물가 지표, 원/달러 환율 상승, 외국인 순매도가 함께 하락 압력으로 작용했습니다.",
        },
        "top_whys": [
            {
                "flow_id": 2,
                "title": "왜 원/달러 환율이 상승했을까?",
            },
            {
                "flow_id": 3,
                "title": "왜 비트코인이 상승했을까?",
            },
        ],
    }