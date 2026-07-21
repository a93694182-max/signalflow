# API

## Sprint 1

### Flow Trace

#### GET /api/flows/{flow_id}/trace

Flow와 연결된 FlowNode를 PostgreSQL에서 조회합니다.

#### Response

- Flow
- FlowNode
- Evidence

---

## Sprint 2

### Evidence

#### GET /api/evidence/{id}

Evidence ID를 기준으로 근거 데이터를 조회합니다.

#### Response

- Evidence 정보
- Evidence Score
- 출처 및 URL

### Ask

#### POST /api/ask

Flow, FlowNode, Evidence를 기반으로 질문에 답변합니다.

#### Request

```json
{
    "flow_id": 1,
    "question": "왜 시장이 하락했나요?"
}
```

#### Response

- Flow 요약
- Flow 경로
- Evidence 개수

### Market Price

#### GET /api/market/price/{symbol}

Yahoo Finance에서 시장 가격을 조회합니다.

#### Supported Symbols

- KOSPI
- KOSDAQ
- USD/KRW
- Bitcoin
- Gold
- WTI

### Market Dashboard

#### GET /api/market/dashboard

주요 금융자산의 실시간 시장 데이터를 조회합니다.

### Market History

#### GET /api/market/history/{symbol}

특정 금융자산의 시장 히스토리를 조회합니다.

#### Query Parameters

- `period`
- `interval`

### Economic Indicator

#### GET /api/economic/fred/{series_id}

FRED에서 경제지표를 조회합니다.

#### Supported Series

- CPIAUCSL
- FEDFUNDS
- UNRATE
- GDP

---

## Sprint 3

### Signal Engine

#### POST /api/engine/run

시장·경제 데이터를 수집하고 Signal을 분석하여 Flow를 자동 생성합니다.

#### Process

```text
Yahoo Finance / FRED
        ↓
Signal 생성
        ↓
Signal Filtering
        ↓
Signal Grouping
        ↓
Flow Discovery
        ↓
Flow / FlowNode / Evidence 생성
        ↓
PostgreSQL 저장
```

#### Response

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

---

## Sprint 4

### News Signal

Finnhub News API에서 뉴스를 수집하고 News Signal로 변환합니다.

#### Process

```text
Finnhub News
      ↓
News Signal 생성
      ↓
Signal Filtering
      ↓
Signal Grouping
      ↓
Flow / FlowNode / Evidence 생성
      ↓
PostgreSQL 저장
```

### Signal Engine v2

#### POST /api/engine/run

시장·경제·뉴스 데이터를 통합 수집하여 Flow를 생성합니다.

#### Process

```text
Yahoo Finance / FRED / Finnhub News
                  ↓
             Signal 생성
                  ↓
           Signal Filtering
                  ↓
           Signal Grouping
                  ↓
            Flow Discovery
                  ↓
      Flow / FlowNode / Evidence 생성
                  ↓
            PostgreSQL 저장
```

#### Response

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

### Flow Ranking v1

#### GET /api/flows/ranking

Evidence 평균점수를 기반으로 Flow 순위를 조회합니다.

#### Evidence Score

- `relation_score`
- `impact_score`
- `time_score`
- `reliability_score`

#### Response

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

---

## Sprint 5

### Why Analysis

#### GET /api/flows/{flow_id}/why

FlowNode와 Evidence Score를 분석하여 가장 유력한 원인 후보와 분석 신뢰도를 반환합니다.

#### Process

```text
Flow 조회
    ↓
FlowNode별 Evidence 평균점수 계산
    ↓
원인 후보 정렬
    ↓
Primary Cause 선정
    ↓
Confidence Score 계산
```

#### Response

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
    "causes": [
        {
            "node_id": 20,
            "title": "KOSPI 6.96% 하락",
            "category": "domestic_stock",
            "description": "KOSPI는 이전 값보다 하락했습니다.",
            "score": 0.97,
            "evidence_count": 1
        }
    ]
}
```

### Flow Timeline

#### GET /api/flows/{flow_id}/timeline

FlowNode를 발생 시각 기준으로 정렬하여 시간순으로 반환합니다.

#### Response

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

### News Topic Classification

수집된 뉴스의 제목과 요약을 분석하여 주제를 자동 분류합니다.

#### Supported Topics

- `monetary_policy`
- `geopolitics`
- `commodity`
- `crypto`
- `technology`
- `corporate`
- `economic`
- `general`

스포츠 등 금융·경제와 관련 없는 뉴스는 Signal 생성 전에 제외합니다.

### Flow Ranking v2

#### GET /api/flows/ranking

Evidence 품질과 근거 개수 충족도를 반영하여 Flow 순위를 계산합니다.

#### Score

```text
Flow Score
= Quality Score × 0.85
+ Coverage Score × 0.15
```

Evidence 5개를 `coverage_score` 1.0의 기준으로 사용합니다.

#### Response

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

### Ask API v2

#### POST /api/ask

Why Analysis 결과를 기반으로 구조화된 답변을 생성합니다.

OpenAI는 아직 사용하지 않습니다.

#### Request

```json
{
    "flow_id": 11,
    "question": "왜 국내 증시가 하락했나요?"
}
```

#### Response

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



## Sprint 6

### Why Trail

#### GET /api/flows/{flow_id}/trail

시장 Flow와 연결된 뉴스·경제지표 원인 후보를 조회합니다.

### Response

```json
{
    "flow_id": 24,
    "title": "국내 증시 혼조 흐름",
    "trail_count": 3,
    "trail": [
        {
            "source_flow_id": 28,
            "source_title": "원자재 흐름",
            "target_flow_id": 24,
            "target_title": "국내 증시 혼조 흐름",
            "relation_type": "potential_cause",
            "score": 0.965,
            "reason": "카테고리 연관성 1.00, 시간 근접성 1.00, 근거 품질 0.83"
        }
    ]
}

```
### Why Analysis v2

#### GET /api/flows/{flow_id}/why

기존 FlowNode 기반 내부 원인 분석에 Cross-Flow 외부 원인 후보를 추가합니다.

추가 응답:

- `external_causes`: 연결 점수가 높은 외부 Flow 원인 후보
- `summary`: 외부 원인 후보와 내부 시장 신호를 함께 설명

외부 원인 후보는 연결 점수순 상위 3개를 반환합니다.




---




## Sprint 7

### Home Intelligence

#### GET /api/home

최근 24시간 내 생성된 시장 Flow를 Ranking하여 홈 화면 데이터를 반환합니다.

뉴스 Flow는 분석 대상에서 제외하고 시장 Flow의 외부 원인 후보로 사용합니다.

#### Selection

- Flow Ranking 1위: `biggest_why`
- Flow Ranking 2~4위: `top_whys`
- 최근 24시간 Flow만 사용
- `target_asset=MARKET`인 뉴스 Flow 제외

#### Response

```json
{
    "biggest_why": {
        "flow_id": 24,
        "title": "국내 증시 상승 흐름",
        "target_asset": "^KS11",
        "score": 0.817,
        "created_at": "2026-07-21T11:01:31+09:00",
        "summary": "국내 증시 상승 흐름과 연결된 외부 원인 후보를 분석했습니다.",
        "confidence_score": 0.89,
        "confidence_level": "high",
        "external_cause_count": 3
    },
    "top_whys": [
        {
            "flow_id": 25,
            "title": "원달러 하락 흐름",
            "target_asset": "KRW=X",
            "score": 0.752,
            "created_at": "2026-07-21T11:01:31+09:00"
        }
    ]
}
```

Flow가 없으면 다음과 같이 반환합니다.

```json
{
    "biggest_why": null,
    "top_whys": []
}
```

### Flow Feed

#### GET /api/flows

Flow 목록을 최신 생성순으로 조회합니다.

#### Query Parameters

| Parameter | Default | Description |
|---|---:|---|
| `limit` | `20` | 조회 개수, 1~100 |
| `offset` | `0` | 건너뛸 개수 |
| `target_asset` | `null` | 자산 코드 필터 |
| `include_news` | `true` | 뉴스 Flow 포함 여부 |
| `query` | `null` | Flow 제목 검색 |

#### Examples

```text
GET /api/flows?limit=10&offset=0
GET /api/flows?target_asset=%5EKS11
GET /api/flows?include_news=false
GET /api/flows?query=국내%20증시
GET /api/flows?target_asset=%5EKS11&query=상승
```

#### Response

```json
{
    "total": 6,
    "limit": 20,
    "offset": 0,
    "flows": [
        {
            "flow_id": 24,
            "title": "국내 증시 상승 흐름",
            "target_asset": "^KS11",
            "summary": "KOSPI와 KOSDAQ이 상승했습니다.",
            "created_at": "2026-07-21T11:01:31+09:00",
            "updated_at": "2026-07-21T11:01:31+09:00"
        }
    ]
}
```


---

# API Index

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/flows/{flow_id}/trace` | Flow Trace 조회 |
| GET | `/api/flows/{flow_id}/why` | Why Analysis 조회 |
| GET | `/api/flows/{flow_id}/timeline` | Flow Timeline 조회 |
| GET | `/api/flows/ranking` | Flow Ranking v2 조회 |
| GET | `/api/evidence/{id}` | Evidence 조회 |
| POST | `/api/ask` | Why 기반 Ask API |
| GET | `/api/market/price/{symbol}` | 시장 가격 조회 |
| GET | `/api/market/dashboard` | 시장 Dashboard 조회 |
| GET | `/api/market/history/{symbol}` | 시장 히스토리 조회 |
| GET | `/api/economic/fred/{series_id}` | FRED 경제지표 조회 |
| POST | `/api/engine/run` | Signal Engine 실행 |
| GET | `/api/flows/{flow_id}/trail` | Why Trail 조회 |
| GET | `/api/home` | Home Intelligence 조회 |
| GET | `/api/flows` | Flow Feed 조회 |
