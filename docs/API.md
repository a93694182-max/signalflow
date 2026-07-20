# API

## Sprint 1

### Flow

#### GET /api/flows/{flow_id}/trace

Flow와 FlowNode를 PostgreSQL에서 조회합니다.

### Response

- Flow
- FlowNode

-----------------------------------------------------

## Sprint 2

### Evidence

#### GET /api/evidence/{id}

Evidence를 조회합니다.

### Response

- Evidence

---

### Ask

#### POST /api/ask

Flow, FlowNode, Evidence를 기반으로 응답을 생성합니다.

### Request

- flow_id
- question

### Response

- answer

---

### Market

#### GET /api/market/price/{symbol}

시장 데이터를 조회합니다.

### Supported

- KOSPI
- KOSDAQ
- USD/KRW
- Bitcoin
- Gold
- WTI

---

#### GET /api/market/dashboard

실시간 시장 데이터를 조회합니다.

---

#### GET /api/market/history/{symbol}

시장 히스토리를 조회합니다.

### Query

- period
- interval

---

### Economic

#### GET /api/economic/fred/{series_id}

FRED 경제지표를 조회합니다.

### Supported

- CPIAUCSL
- FEDFUNDS
- UNRATE
- GDP

-----------------------------------------------------

## Sprint 3

### Signal Engine

#### POST /api/engine/run

Signal Engine를 실행하여 Flow를 자동 생성합니다.

### Process

Yahoo Finance
↓

FRED
↓

Signal 생성
↓

Signal Filtering
↓

Signal Grouping
↓

Flow 생성
↓

FlowNode 생성
↓

Evidence 생성
↓

PostgreSQL 저장

---

### Response

```json
{
    "collected_count": 10,
    "filtered_count": 8,
    "flow_count": 5,
    "flow_ids": [
        3,
        5,
        6,
        8,
        9
    ]
}
```

-----------------------------------------------------

## Sprint 4

### News Signal

Finnhub News API를 연동하여 News Signal을 생성합니다.

### Process

Finnhub News
↓

News Signal 생성
↓

Signal Filtering
↓

Flow 생성
↓

FlowNode 생성
↓

Evidence 생성
↓

PostgreSQL 저장

---

### Signal Engine

#### POST /api/engine/run

시장 데이터와 뉴스 데이터를 수집하여 Flow를 생성합니다.

### Process

Yahoo Finance
↓

FRED
↓

Finnhub News
↓

Signal 생성
↓

Signal Filtering
↓

Signal Grouping
↓

Flow 생성
↓

FlowNode 생성
↓

Evidence 생성
↓

PostgreSQL 저장

---

### Response

```json
{
    "collected_count": 30,
    "filtered_count": 27,
    "flow_count": 5,
    "flows": [
        {
            "id": 10,
            "title": "국내 증시 하락 흐름",
            "target_asset": "^KS11"
        },
        {
            "id": 14,
            "title": "주요 뉴스 흐름",
            "target_asset": "MARKET"
        }
    ]
}
```

---

### Flow Ranking

#### GET /api/flows/ranking

Evidence Score를 기반으로 Flow 순위를 조회합니다.

### Score

- relation_score
- impact_score
- time_score
- reliability_score

### Response

```json
[
    {
        "rank": 1,
        "flow_id": 14,
        "title": "주요 뉴스 흐름",
        "target_asset": "MARKET",
        "score": 0.91,
        "evidence_count": 20
    }
]
```