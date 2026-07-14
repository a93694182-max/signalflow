import requests
from fastapi import HTTPException, status

from app.config import FRED_API_KEY


FRED_BASE_URL = "https://api.stlouisfed.org/fred"

FRED_SERIES = {
    "CPIAUCSL": {
        "name": "미국 소비자물가지수",
        "unit": "Index",
    },
    "FEDFUNDS": {
        "name": "미국 연방기금금리",
        "unit": "%",
    },
    "UNRATE": {
        "name": "미국 실업률",
        "unit": "%",
    },
    "GDP": {
        "name": "미국 국내총생산",
        "unit": "Billions of Dollars",
    },
}


def get_fred_series(
    series_id: str,
    limit: int = 24,
) -> dict:
    if not FRED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="FRED_API_KEY가 설정되지 않았습니다.",
        )

    series_id = series_id.upper()

    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": limit,
    }

    try:
        response = requests.get(
            f"{FRED_BASE_URL}/series/observations",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="FRED 데이터를 가져오는 중 오류가 발생했습니다.",
        ) from exc

    data = response.json()
    raw_observations = data.get("observations", [])

    observations = []

    for item in reversed(raw_observations):
        value = item.get("value")

        # FRED는 값이 없을 때 "."을 반환하는 경우가 있음
        if value in (None, "."):
            continue

        observations.append(
            {
                "date": item["date"],
                "value": float(value),
            }
        )

    if not observations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{series_id} 데이터를 찾을 수 없습니다.",
        )

    metadata = FRED_SERIES.get(
        series_id,
        {
            "name": series_id,
            "unit": "Unknown",
        },
    )

    return {
        "series_id": series_id,
        "name": metadata["name"],
        "unit": metadata["unit"],
        "observations": observations,
    }