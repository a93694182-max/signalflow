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





## Sprint 5

### Why Analysis

#### GET /api/flows/{flow_id}/why

FlowNode와 Evidence Score를 분석하여 가장 유력한 원인 후보를 반환합니다.

### Process

Flow 조회

↓

FlowNode별 Evidence Score 평균 계산

↓

원인 후보 정렬

↓

Primary Cause 선정

↓

Confidence 계산

### Response

```json
{
    "flow_id": 11,
    "title": "국내 증시 하락 흐름",
    "target_asset": "^KS11",
    "summary": "국내 증시 하락 흐름의 가장 유력한 원인은 'KOSPI 6.96% 하락'입니다.",
    "confidence_score": 0.97,
    "confidence_level": "high",
    "primary_cause": {
        "node_id": 20,
        "title": "KOSPI 6.96% 하락",
        "category": "domestic_stock",
        "description": "KOSPI는 이전 값보다 하락했습니다.",
        "score": 0.97,
        "evidence_count": 1
    },
    "causes": []
}
```

---

### Flow Timeline

#### GET /api/flows/{flow_id}/timeline

FlowNode를 발생 시각 기준으로 정렬하여 Flow Timeline을 반환합니다.

### Response

```json
{
    "flow_id": 11,
    "title": "국내 증시 하락 흐름",
    "target_asset": "^KS11",
    "event_count": 2,
    "timeline": [
        {
            "node_id": 20,
            "order_index": 1,
            "title": "KOSPI 6.96% 하락",
            "category": "domestic_stock",
            "description": "KOSPI 시장 변화",
            "occurred_at": "2026-07-16T00:00:00+09:00",
            "evidence_level": "strong",
            "evidence_count": 1
        }
    ]
}
```

---

### News Topic Classification

수집된 뉴스의 제목과 요약을 키워드 기반으로 분석하여 주제를 자동 분류합니다.

### Topics

- monetary_policy
- geopolitics
- commodity
- crypto
- technology
- corporate
- economic
- general

스포츠 등 금융·경제와 관련 없는 뉴스는 수집 단계에서 제외합니다.

---

### Flow Ranking v2

#### GET /api/flows/ranking

Evidence 품질과 근거 개수 충족도를 함께 반영하여 Flow 순위를 계산합니다.

### Score

```text
Flow Score
= Quality Score × 0.85
+ Coverage Score × 0.15
```

Evidence 5개를 Coverage Score 1.0의 기준으로 사용합니다.

### Response

```json
[
    {
        "rank": 1,
        "flow_id": 11,
        "title": "국내 증시 하락 흐름",
        "target_asset": "^KS11",
        "score": 0.855,
        "quality_score": 0.97,
        "coverage_score": 0.4,
        "evidence_count": 2
    }
]
```

---

### Ask API v2

#### POST /api/ask

Why Analysis 결과를 기반으로 구조화된 답변을 생성합니다.

OpenAI는 아직 사용하지 않습니다.

### Request

```json
{
    "flow_id": 11,
    "question": "왜 국내 증시가 하락했나요?"
}
```

### Response

```json
{
    "flow_id": 11,
    "question": "왜 국내 증시가 하락했나요?",
    "answer": "국내 증시 하락 흐름의 가장 유력한 원인은 'KOSPI 6.96% 하락'입니다.",
    "confidence_score": 0.97,
    "confidence_level": "high",
    "primary_cause": "KOSPI 6.96% 하락",
    "flow_path": [
        "KOSPI 6.96% 하락",
        "KOSDAQ 4.46% 하락"
    ],
    "evidence_count": 2
}
```




-----------------------------------------------------

# API Index

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/flows/{flow_id}/trace | Flow 조회 |
| GET | /api/flows/ranking | Flow Ranking v2 조회 |
| GET | /api/evidence/{id} | Evidence 조회 |
| POST | /api/ask | Why 기반 Ask API |
| GET | /api/market/dashboard | 시장 Dashboard |
| GET | /api/market/history/{symbol} | 시장 히스토리 |
| GET | /api/economic/fred/{series_id} | 경제지표 조회 |
| POST | /api/engine/run | Signal Engine 실행 |
| GET | /api/flows/{flow_id}/why | Why Analysis 조회 |
| GET | /api/flows/{flow_id}/timeline | Flow Timeline 조회 |

