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

Sprint 5 기준으로 OpenAI는 사용하지 않으며, Sprint 13에서 선택적 OpenAI 연동을 추가합니다.

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

뉴스 Flow는 Home Ranking에서 제외하고 시장 Flow의 외부 원인 후보로 사용합니다.

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

Flow 목록을 검색·필터링하고 최신순 또는 점수순으로 조회합니다.

#### Query Parameters

| Parameter | Default | Description |
|---|---:|---|
| `limit` | `20` | 조회 개수, 1~100 |
| `offset` | `0` | 건너뛸 Flow 개수 |
| `target_asset` | `null` | 자산 코드 필터 |
| `include_news` | `true` | 뉴스 Flow 포함 여부 |
| `query` | `null` | Flow 제목 검색 |
| `from_date` | `null` | 조회 시작일 |
| `to_date` | `null` | 조회 종료일 |
| `sort` | `latest` | `latest` 또는 `score` |

날짜 필터는 `Asia/Seoul`을 기준으로 하며 `to_date` 당일 전체를 포함합니다.

#### Examples

```text

GET /api/flows?limit=10&offset=0

GET /api/flows?target_asset=%5EKS11

GET /api/flows?include_news=false

GET /api/flows?query=국내%20증시

GET /api/flows?from_date=2026-07-20&to_date=2026-07-21

GET /api/flows?sort=score

GET /api/flows?target_asset=%5EKS11&query=상승&sort=score

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

            "score": 0.817,

            "evidence_count": 2,

            "link_count": 3,

            "created_at": "2026-07-21T11:01:31+09:00",

            "updated_at": "2026-07-21T11:01:31+09:00"

        }

    ]

}

```

#### Validation

- `limit`: 1~100
- `offset`: 0 이상
- `sort`: `latest`, `score`
- `from_date`는 `to_date`보다 늦을 수 없음

---

## Sprint 8

### Market Timeline

#### GET /api/timeline

최근 Flow를 조회한 뒤 시간 오름차순으로 반환합니다.

각 Flow의 Ranking Score, Evidence 요약, 연결된 외부 원인 후보를 함께 제공합니다.

#### Query Parameters

| Parameter | Default | Description |
|---|---:|---|
| `limit` | `20` | 최근 Flow 조회 개수, 1~100 |
| `target_asset` | `null` | 자산 코드 필터 |
| `from_date` | `null` | 조회 시작일 |
| `to_date` | `null` | 조회 종료일 |
| `include_causes` | `true` | 외부 원인 후보 포함 여부 |

날짜 필터는 `Asia/Seoul`을 기준으로 하며 `to_date` 당일 전체를 포함합니다.

#### Response

```json

{

    "total": 6,

    "limit": 20,

    "target_asset": "^KS11",

    "timeline": [

        {

            "flow_id": 24,

            "title": "국내 증시 상승 흐름",

            "target_asset": "^KS11",

            "summary": "KOSPI와 KOSDAQ이 상승했습니다.",

            "score": 0.817,

            "event_at": "2026-07-21T11:01:31+09:00",

            "evidence_count": 2,

            "evidences": [

                {

                    "evidence_id": 24,

                    "title": "KOSPI 실시간 데이터",

                    "source": "yahoo_finance",

                    "url": "https://finance.yahoo.com/"

                }

            ],

            "causes": [

                {

                    "flow_id": 20,

                    "title": "금리 인상 뉴스 흐름",

                    "target_asset": "MARKET",

                    "relation_type": "potential_cause",

                    "score": 0.9,

                    "reason": "금리 인상 우려가 증시에 영향을 줌"

                }

            ]

        }

    ]

}

```

### Unified Search

#### GET /api/search

Flow와 Evidence를 통합 검색합니다.

#### Query Parameters

| Parameter | Default | Description |
|---|---:|---|
| `q` | 필수 | 검색어 |
| `limit` | `20` | 유형별 최대 결과 개수, 1~100 |
| `type` | `all` | `all`, `flow`, `evidence` |
| `target_asset` | `null` | 자산 코드 필터 |
| `from_date` | `null` | 조회 시작일 |
| `to_date` | `null` | 조회 종료일 |

#### Search Fields

- Flow 제목
- Flow 요약
- Evidence 제목
- Evidence 내용 요약
- Evidence 출처

#### Response

```json

{

    "query": "KOSPI",

    "total": 14,

    "flow_count": 7,

    "evidence_count": 7,

    "flows": [

        {

            "flow_id": 24,

            "title": "국내 증시 상승 흐름",

            "target_asset": "^KS11",

            "summary": "KOSPI와 KOSDAQ이 상승했습니다.",

            "created_at": "2026-07-21T11:01:31+09:00"

        }

    ],

    "evidences": [

        {

            "evidence_id": 24,

            "flow_id": 24,

            "flow_title": "국내 증시 상승 흐름",

            "target_asset": "^KS11",

            "title": "KOSPI 실시간 데이터",

            "source": "yahoo_finance",

            "content_summary": "KOSPI 상승 데이터",

            "url": "https://finance.yahoo.com/",

            "published_at": "2026-07-21T11:01:31+09:00"

        }

    ]

}

```

#### Validation

- `q`: 1~100자이며 공백만 입력할 수 없음
- `limit`: 1~100
- `type`: `all`, `flow`, `evidence`
- `from_date`는 `to_date`보다 늦을 수 없음

---

## Sprint 9

### Home Dashboard

#### Route

/

#### 사용 API

- GET /api/home
- GET /api/market/dashboard
- GET /api/flows

#### 주요 기능

- 시장 Overview
- Biggest Why
- Top Whys
- Flow Feed
- 검색 및 필터
- 페이지네이션

---

### Frontend

#### Environment

- React
- Vite
- React Router
- VITE_API_BASE_URL

---

### CORS

개발 환경에서 React(`http://localhost:5173`)와 FastAPI 간 통신을 허용합니다.

Sprint 9에서는 새로운 API를 추가하지 않고 기존 API를 React Home 화면과 연동합니다.

---

## Sprint 10

### Flow Detail Page

#### Route

/flows/{flow_id}

#### 사용 API

- GET /api/flows/{flow_id}/trace
- GET /api/flows/{flow_id}/why
- GET /api/flows/{flow_id}/trail
- POST /api/ask

#### 주요 기능

- Flow 상세 정보
- Flow Timeline
- Evidence 목록
- Why Analysis
- Why Trail
- Ask 기능

---

### Market Timeline Page

#### Route

/timeline

#### 사용 API

- GET /api/timeline

#### 주요 기능

- Timeline 조회
- 자산 필터
- 기간 필터
- 원인 포함 여부
- Flow 상세 이동

Sprint 10에서는 기존 API를 활용하여 Flow 상세 화면과 Timeline 화면을 구현합니다.

---

## Sprint 11

### Unified Search

#### Route

/search

#### 사용 API

- GET /api/search

#### 주요 기능

- Flow 검색
- Evidence 검색
- 검색 유형 선택
- 자산 필터
- 기간 필터
- Flow 상세 이동
- Evidence 원문 링크

---

### Frontend Navigation

#### Routes

| Route | Page |
|-------|------|
| `/` | Home Dashboard |
| `/flows/{flow_id}` | Flow Detail |
| `/timeline` | Market Timeline |
| `/search` | Unified Search |

Sprint 11에서는 React Router 기반의 페이지 이동과 통합 검색 기능을 완성합니다.

---

## Sprint 12

### Daily Market Briefing

#### Route

GET /api/briefing/daily

#### 주요 기능

- 최근 24시간 주요 Flow 분석
- Flow Ranking 기반 Top Flow 선정
- Why Analysis 기반 시장 요약
- 주요 원인(Key Causes) 제공
- Top Flows 제공

---

### Home Dashboard

#### 추가 기능

- Daily Market Briefing 표시
- 60초 주기 Dashboard 자동 갱신

Sprint 12에서는 기존 Flow Ranking과 Why Analysis를 활용하여 일일 시장 브리핑을 제공하고 Home Dashboard의 최신 데이터를 자동 갱신합니다.

---

## Sprint 13 — AI Intelligence

### Ask API 개선

기존 `POST /api/ask`의 AI 설명 생성 기능을 개선했습니다. 새로운 Endpoint는 추가하지 않았습니다.

- Flow Trace, Why Analysis, Why Trail을 기반으로 답변 생성
- Evidence 제목 최대 10개를 AI 프롬프트에 포함
- 제공된 근거만 사용하도록 프롬프트 구성
- 불확실한 인과관계는 원인 후보로 표현
- 답변은 한국어 최대 5문장으로 제한
- AI 호출 실패 또는 비활성화 시 Template Fallback 사용

### Answer Source

응답의 `answer_source` 필드로 답변 생성 방식을 구분합니다.

| Value | Description |
|---|---|
| `openai` | OpenAI 기반 설명 |
| `template` | 기존 분석 결과 기반 기본 설명 |

### OpenAI Configuration

| Environment Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API 인증 키 |
| `OPENAI_MODEL` | AI 응답 생성 모델 |
| `OPENAI_ENABLED` | OpenAI 호출 활성화 여부 |

`OPENAI_ENABLED=false`이면 실제 OpenAI API를 호출하지 않고 기본 분석을 사용합니다.

> 실제 OpenAI 응답은 API 크레딧 부족으로 검증하지 못했으며, 성공·실패·Fallback 경로는 Mock 테스트로 검증했습니다.

---



## Sprint 14

### Signal Engine — Data Quality

#### POST /api/engine/run

기존 Signal Engine API의 데이터 품질 처리 방식을 개선합니다.

#### 주요 변경 사항

- 중복 Flow는 새로 생성하지 않음
- `flow_count`는 신규 생성된 Flow 개수만 반환
- 신규 Flow만 Cross-Flow Linking 대상으로 사용
- 동일 실행 내 뉴스 ID, URL, 제목 기반 중복 제거
- 경제·금융 관련성이 있는 뉴스 Signal만 유지

#### Response

기존 응답 구조를 유지합니다.

- `collected_count`: 수집한 Signal 개수
- `filtered_count`: 필터링 후 Signal 개수
- `flow_count`: 신규 생성한 Flow 개수
- `link_count`: 생성한 FlowLink 개수
- `flows`: 신규 생성한 Flow 목록

#### Compatibility

- 기존 Endpoint 유지
- Response 필드 구조 유지
- 데이터베이스 스키마 변경 없음


---


## Sprint 15

### Analysis Engine — Reliability Enhancement

#### GET /api/flows/{flow_id}/why

기존 Why Analysis API의 Confidence Score 계산 방식을 개선합니다.

#### 주요 변경 사항

- Evidence Quality와 Evidence Coverage를 결합하여 Confidence Score 계산
- Evidence Quality 가중치 85% 적용
- Evidence Coverage 가중치 15% 적용
- Evidence 1개일 때 Confidence Score 최대 0.59
- Evidence 2~4개일 때 Confidence Score 최대 0.79
- Evidence 5개 이상일 때 근거 개수에 따른 상한 해제
- 내부 Confidence Score와 외부 원인 연결 점수 분리 유지

#### GET /api/flows/{flow_id}/trail

기존 Cross-Flow Linking의 원인 후보 연결 기준을 개선합니다.

#### 주요 변경 사항

- 원인 Flow와 결과 Flow의 시간 순서 검증
- 72시간을 초과하는 Flow 연결 제외
- general 카테고리의 무분별한 시장 Flow 연결 방지
- Evidence Quality가 0.5 미만인 Flow 연결 제외
- 기존 potential_cause 관계 유형 유지

#### Response

기존 응답 구조를 유지합니다.

- `confidence_score`: Evidence Quality와 Coverage를 반영한 분석 신뢰도
- `confidence_level`: low, medium, high
- `primary_cause`: 가장 높은 점수의 내부 원인 후보
- `external_causes`: 외부 원인 후보 목록

#### Compatibility

- 기존 Endpoint 유지
- Response 필드 구조 유지
- 데이터베이스 스키마 변경 없음

---


## Sprint 16

### Why Analysis Explainability

#### GET /api/flows/{flow_id}/why

기존 Why Analysis API에 분석 점수와 원인 순위를 설명하는 정보를 추가합니다.

#### 주요 변경 사항

- Evidence별 점수 구성 요소 및 가중치 제공
- Confidence Score 계산 과정 제공
- Cause Ranking 순위 및 선정 이유 제공
- 기존 Why Analysis 응답 구조 유지

#### 추가 Response Fields

- `evidence_breakdowns`: Evidence별 점수 및 가중치 상세 정보
- `confidence_breakdown`: Confidence Score 계산 과정
- `cause_ranking`: 내부 원인 후보의 순위 및 선정 이유

#### Evidence Score Breakdown

- `scores`: Relation, Impact, Time, Reliability 원본 점수
- `weights`: 각 점수의 가중치
- `weighted_scores`: 가중치가 반영된 점수
- `total_score`: 최종 Evidence Score

#### Confidence Score Breakdown

- `quality_score`: Evidence 품질 점수
- `coverage_score`: Evidence 개수 충족도
- `quality_weight`: 품질 점수 가중치 0.85
- `coverage_weight`: 근거 충족도 가중치 0.15
- `evidence_count`: 전체 Evidence 개수
- `raw_score`: 상한 적용 전 점수
- `confidence_cap`: Evidence 개수에 따른 점수 상한
- `confidence_score`: 최종 Confidence Score
- `confidence_level`: Confidence 등급

#### Cause Ranking

- `rank`: 원인 후보 순위
- `node_id`: FlowNode ID
- `title`: 원인 후보 제목
- `score`: Evidence 평균 점수
- `evidence_count`: Evidence 개수
- `reason`: 순위 선정 이유

#### Compatibility

- 기존 Endpoint 유지
- 기존 Response 필드 유지
- 새로운 설명 필드만 추가
- 데이터베이스 스키마 변경 없음

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
| GET | `/api/flows` | Flow Feed 검색·필터·정렬 |
| GET | `/api/timeline` | 여러 Flow의 Market Timeline 조회 |
| GET | `/api/search` | Flow·Evidence 통합 검색 |
| GET | `/api/briefing/daily` | Daily Market Briefing 조회 |

---
