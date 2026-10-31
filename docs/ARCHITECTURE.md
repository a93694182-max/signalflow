# Architecture

SignalFlow의 Sprint별 시스템 구성 및 데이터 흐름을 기록합니다.

## Sprint 1

```text
Client
  ↓
FastAPI Router
  ↓
Service Layer
  ↓
SQLAlchemy ORM
  ↓
PostgreSQL
```

---

## Sprint 2

```text
Client
  ↓
FastAPI Router
  ↓
Service Layer
  ↓
SQLAlchemy ORM
  ↓
PostgreSQL
  ↓
External APIs
  ├── Yahoo Finance
  └── FRED
```

---

## Sprint 3

```text
Scheduler
  ↓
Collector Service
  ├── Yahoo Finance
  └── FRED
  ↓
Signal Service
  ↓
Signal Filter
  ↓
Flow Discovery
  ↓
Flow
  ↓
FlowNode
  ↓
Evidence
  ↓
PostgreSQL
```

---

## Sprint 4

```text
Yahoo Finance / FRED / Finnhub News
  ↓
Collector
  ↓
Signal Filter
  ↓
Flow Discovery
  ↓
Evidence Scoring
  ↓
Flow Ranking
  ↓
PostgreSQL
  ↓
FastAPI API
```

---

## Sprint 5

```text
External News
  ↓
News Relevance Filter
  ↓
News Topic Classifier
  ↓
Topic-based Signal Grouping
  ↓
Flow / FlowNode / Evidence
  ↓
Why Analysis Engine
  ├── Cause Ranking
  ├── Primary Cause
  └── Confidence Score
  ↓
Flow Timeline
  ↓
Flow Ranking v2
  ├── Evidence Quality
  └── Evidence Coverage
  ↓
Ask API v2
```

---

## Sprint 6

### Cross-Flow Cause Linking

```text
News / Economic Flow
  ↓
Cross-Flow Linking
  ├── Category Score
  ├── Time Score
  └── Evidence Quality Score
  ↓
FlowLink
  ↓
Market Flow
  ↓
Why Trail API
  ↓
Ask API v3
  ├── OpenAI Explanation
  └── Template Fallback
```

### Why Analysis v2

```text
Why Analysis v2
  ├── External Causes (FlowLink)
  ├── Internal Causes (FlowNode)
  ├── Primary Internal Signal
  └── Cross-Flow Summary
```

---

## Sprint 7

### Home Intelligence

```text
PostgreSQL Flow Data
  ↓
Recent Flow Filter
  ├── 최근 24시간
  └── News Flow 제외
  ↓
Flow Ranking
  ↓
Why Analysis
  ↓
Home API
  ├── Biggest Why
  └── Top Whys
```

### Flow Feed

```text
PostgreSQL Flow Data
  ↓
Flow Feed Query
  ├── Pagination
  ├── Target Asset Filter
  ├── News Filter
  ├── Title Search
  ├── Date Filter
  └── Latest / Score Sort
  ↓
Flow Ranking v2
  ↓
Feed Summary
  ├── Score
  ├── Evidence Count
  └── Link Count
  ↓
Flow Feed API
```

---

## Sprint 8

### Market Timeline

```text
PostgreSQL Flow Data
  ↓
Target Asset / Date Filter
  ↓
Recent Flow Selection
  ↓
Time Order
  ↓
Flow Ranking v2
  ↓
Timeline Enrichment
  ├── Evidence Summary
  └── External Causes (FlowLink)
  ↓
Market Timeline API
```

### Unified Search

```text
Search Query
  ↓
Unified Search Service
  ├── Flow Title / Summary
  └── Evidence Title / Summary / Source
  ↓
Target Asset / Date / Type Filter
  ↓
Flow Results + Evidence Results
  ↓
Unified Search API
```

---

## Sprint 9

```text
Browser
  ↓
React + TypeScript + Vite
  ↓
React Router
  ↓
API Client
  ↓
FastAPI
  ↓
Home Dashboard
  ├── Market Overview
  ├── Biggest Why
  ├── Top Whys
  └── Flow Feed
  ↓
Flow Feed Filter
  ↓
Flow Feed API
```

---

## Sprint 10

```text
React Router
  ├── /
  ├── /flows/{flow_id}
  ├── /timeline
  └── /search
  ↓
Flow Detail
  ├── Trace
  ├── Why Analysis
  ├── Why Trail
  └── Ask
  ↓
Market Timeline
  ↓
Timeline API
  ↓
Timeline UI
  ↓
Flow Detail
  ↓
Search Page
  ↓
Unified Search API
  ↓
Search Result
```

---

## Sprint 11

```text
Home
  ├── Dashboard
  ├── Market Timeline
  └── Flow Feed
  ↓
Timeline
  ├── Asset Filter
  ├── Date Filter
  └── Related Causes
  ↓
Search
  ├── Unified Search
  ├── Flow Result
  └── Evidence Result
  ↓
Flow Detail
```

---

## Sprint 12

### Daily Market Briefing

```text
Flow / Evidence
  ↓
Flow Ranking
  ↓
Why Analysis
  ↓
Daily Briefing Service
  ↓
GET /api/briefing/daily
  ↓
Daily Briefing UI
  ↓
Home Dashboard
  ↓
60s Auto Refresh
```

---

## Sprint 13 — AI Intelligence

### AI Explanation Pipeline

```text
POST /api/ask
  ↓
Flow Trace / Why Analysis / Why Trail
  ↓
Evidence Collection (제목 최대 10개)
  ↓
Evidence-based Prompt
  ↓
OPENAI_ENABLED 및 API Key 확인
  ├── 활성화 → OpenAI 응답 시도
  │                 ├── 성공 → AI Explanation
  │                 └── 실패 → Template Fallback
  └── 비활성화 → Template Fallback
  ↓
FlowAnswer (answer_source: openai / template)
  ↓
Ask UI (AI 분석 / 기본 분석 배지)
```

### 주요 구성

- `ai_service.py`: 근거 기반 프롬프트 생성, OpenAI 응답 처리, Template Fallback
- `config.py`: `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_ENABLED` 설정 관리
- Flow Trace, Why Analysis, Why Trail 및 Evidence 제목을 설명 생성의 입력으로 활용
- 제공된 근거만 사용하고 불확실한 인과관계를 원인 후보로 표현하도록 프롬프트 구성
- OpenAI 비활성화 또는 호출 실패 시 기존 Template 답변 사용
- 프론트엔드: `answer_source`에 따라 `AI 분석` / `기본 분석` 배지 표시
- 기존 API Endpoint 및 데이터베이스 스키마 유지

### 검증 범위

- 백엔드 테스트 36개 통과
- 프론트엔드 ESLint 및 Production Build 통과
- OpenAI 성공·실패 경로는 Mock 테스트로 검증
- 실제 OpenAI 응답은 API 크레딧 부족으로 미검증



---

## Sprint 14 — Data Quality & Reliability

### Signal Processing Pipeline

```text
Yahoo Finance / FRED / Finnhub
  ↓
Signal Collection
  ↓
Signal Filter
  ├── Meaningful Change Filter
  ├── News Relevance Filter
  └── News Deduplication
        ├── News ID
        ├── URL
        └── Title
  ↓
Flow Discovery
  ↓
Flow Deduplication
  ├── Title / Target Asset
  ├── Occurred At
  └── FlowNode Signature
  ↓
New Flow Persistence
  ↓
Cross-Flow Linking
  ↓
PostgreSQL
```

### 주요 구성

- `signal_filter_service.py`: 뉴스 ID, URL, 제목 기반 중복 Signal 제거
- `news_topic_classifier.py`: 경제·금융 키워드 기반 뉴스 관련성 판단
- `flow_service.py`: FlowNode 내용 기반 중복 Flow 판정
- `engine_service.py`: 신규 Flow만 반환하고 Cross-Flow Linking 수행
- 발생 시각 비교 시 UTC 정규화
- 기존 데이터베이스 스키마 유지

### 검증 범위

- 백엔드 테스트 48개 통과
- 중복 Flow 생성 방지 검증
- 뉴스 중복 제거 및 관련성 필터링 검증
- 외부 뉴스 API에 의존하지 않는 Flow 테스트

---

## Sprint 15

### Cross-Flow Linking Enhancement

Flow 간 원인 후보 연결의 시간 순서와 근거 품질을 검증합니다.

#### Process

```text
Source Flow / Target Flow
            ↓
      Category Validation
            ↓
       Time Validation
            ↓
   Evidence Quality Validation
            ↓
       Link Score 계산
            ↓
       FlowLink 생성
```

#### 주요 변경 사항

- 원인 Flow가 결과 Flow보다 늦게 발생한 경우 연결 제외
- 최대 연결 시간 72시간 유지
- general 카테고리의 시장 Flow 연결 제한
- 최소 Evidence Quality 0.5 적용

### Evidence Scoring Enhancement

Evidence의 관련성, 영향도, 시간, 출처 신뢰도 평가 방식을 개선합니다.

#### Evidence Score

- Relation Score: 30%
- Impact Score: 20%
- Time Score: 20%
- Reliability Score: 30%

#### 주요 변경 사항

- 뉴스 관련성 기반 Relation Score 계산
- 시장 변동률 기반 Impact Score 계산
- 미래 시각 Evidence의 Time Score 0.0 처리
- 출처 이름의 정확한 일치 기반 Reliability Score 계산

### Why Analysis Confidence Enhancement

Evidence Quality와 Coverage를 결합하여 Confidence Score를 계산합니다.

#### Process

```text
Flow 조회
    ↓
FlowNode별 Evidence Score 계산
    ↓
Evidence Quality 계산
    ↓
Evidence Coverage 계산
    ↓
Confidence Score 계산
    ↓
Evidence 개수별 상한 적용
    ↓
Confidence Level 결정
```

#### Confidence Score

- Evidence Quality: 85%
- Evidence Coverage: 15%
- Evidence Coverage Target: 5
- Evidence 1개: 최대 0.59
- Evidence 2~4개: 최대 0.79
- Evidence 5개 이상: 근거 개수에 따른 상한 없음

### Cross-Flow Why Analysis

- 내부 Why Analysis는 Flow 내부 Evidence를 기반으로 계산
- 외부 원인 후보는 FlowLink를 통해 별도 조회
- 외부 원인 후보는 최대 3개 사용
- 외부 FlowLink Score는 내부 Confidence Score에 합산하지 않음

### Database

- 기존 Flow, FlowNode, Evidence, FlowLink 모델 유지
- 데이터베이스 스키마 변경 없음

---

---

## Sprint 16

### Analysis Explainability

```text
Flow / FlowNode / Evidence
  ↓
Evidence Scoring
  ├── Relation Score
  ├── Impact Score
  ├── Time Score
  └── Reliability Score
  ↓
Evidence Score Breakdown
  ├── Original Scores
  ├── Score Weights
  └── Weighted Scores
  ↓
Why Analysis Engine
  ├── Cause Ranking
  ├── Primary Cause
  └── Confidence Score
  ↓
Analysis Explainability
  ├── Confidence Breakdown
  └── Cause Ranking Explanation
  ↓
Why Analysis API
  ├── evidence_breakdowns
  ├── confidence_breakdown
  └── cause_ranking
```

### Analysis Validation

```text
Evidence Score Validation
  ↓
Confidence Breakdown Validation
  ↓
Cause Ranking Validation
  ↓
Why Analysis Consistency Validation
  ↓
Why API Response Validation
```

---

## Sprint 17

### Explainability UI

```text
Flow Detail Page
  ↓
GET /api/flows/{flow_id}/why
  ↓
FlowWhyAnalysis
  ├── Why Analysis
  ├── Evidence Breakdown
  │     ├── Original Scores
  │     ├── Score Weights
  │     └── Weighted Contributions
  ├── Confidence Breakdown
  │     ├── Quality Score
  │     ├── Coverage Score
  │     └── Confidence Cap
  └── Cause Ranking
        ├── Rank
        ├── Evidence Count
        └── Ranking Reason
```


---

## Sprint 18

### Analysis Accuracy & Consistency

```text
Flow / FlowNode / Evidence
  ↓
Why Analysis Engine
  ↓
Cause Score Calculation
  ↓
Shared Cause Ranking
  ├── Evidence Average Score DESC
  ├── Evidence Count DESC
  └── Node ID ASC
  ↓
Primary Cause Selection
  ↓
Cause Ranking Explanation
  ├── Score-based Ranking
  ├── Evidence Count Tie-breaker
  └── Node ID Tie-breaker
  ↓
Why Analysis API
```

### Analysis Consistency

- `rank_causes()`를 공통 정렬 함수로 사용
- `analyze_flow()`와 `explain_cause_ranking()`의 정렬 기준 통일
- 점수와 근거 개수가 동일한 경우 Node ID 오름차순 정렬
- Primary Cause와 Cause Ranking 1위의 일관성 유지
- Evidence가 없는 경우 Primary Cause를 생성하지 않음

### Validation

- Cause Ranking 동점 처리 검증
- 입력 순서에 따른 Ranking 결과 일관성 검증
- Ranking 1위 선정 이유 검증
- Primary Cause 일관성 검증
- 백엔드 전체 테스트 82개 통과
- 기존 API 및 데이터베이스 구조 유지


---

## Sprint 19

### Analysis Reliability & UX

```text
Flow Detail Page
  ↓
Why Analysis API
  ↓
Analysis Reliability UI
  ├── Confidence Breakdown
  │     ├── Confidence Level Description
  │     └── Insufficient Evidence Warning
  ├── Cause Ranking
  │     ├── Ranking Reason
  │     └── Equal Score Badge
  └── Flow Detail Error Handling
        ├── Invalid Flow ID
        ├── HTTP 404
        ├── HTTP 5xx
        └── Network Error
```

### 주요 변경 사항

- Confidence Level별 해석 안내 추가
- Evidence 0~1개인 경우 근거 부족 경고 표시
- Cause Ranking의 동일 점수 후보 표시
- `ApiError`를 통한 HTTP 상태 코드 전달
- Flow Detail 페이지의 오류 유형별 메시지 구분
- 기존 API 응답 및 데이터베이스 구조 유지

### Validation

- 프론트엔드 Production Build 통과
- 프론트엔드 ESLint 통과
- Flow Detail 오류 화면 검증
- 백엔드 전체 테스트 82개 통과

---

## Sprint 20

### Flow Detail State Management

```text
Flow ID 변경
  ↓
Flow ID Validation
  ↓
Parallel API Requests
  ├── Flow Trace
  ├── Why Analysis
  └── Why Trail
  ↓
Request Lifecycle Validation
  ├── Active Request → State Update
  └── Inactive Request → Ignore
  ↓
FlowDetailState
  ├── Loading
  ├── Success
  └── Error
  ↓
Flow ID Consistency Check
  ↓
Flow Detail UI
```

### 주요 변경 사항

- 이전 API 요청 결과가 새로운 Flow 화면을 덮어쓰지 않도록 방지
- 현재 URL의 Flow ID와 로딩된 데이터의 Flow ID 비교
- 로딩, 성공, 오류 상태를 `FlowDetailState`로 통합
- 여러 API 응답을 하나의 성공 상태로 관리
- 기존 HTTP 오류 처리 및 Explainability UI 유지
- 백엔드 API 및 데이터베이스 스키마 변경 없음

### Validation

- 프론트엔드 Production Build 통과
- 프론트엔드 ESLint 통과
- Flow Detail 정상 및 오류 화면 검증

---

## Sprint 21

### Testing & Reliability

```text
Frontend Tests
  ├── Vitest
  ├── API Client Tests
  │     ├── GET / POST
  │     ├── HTTP 404 / 500
  │     └── Network Error
  └── Flow Detail Tests
        ├── Loading / Success / Error
        ├── Invalid Flow ID
        └── Stale Response Prevention

Backend Tests
  ├── Existing API / Service Tests
  └── Scheduler Reliability Tests
        ├── Successful Execution
        ├── Failure Handling
        └── Database Session Cleanup
```

### Validation

- 프론트엔드 자동화 테스트 10개 통과
- 백엔드 전체 테스트 85개 통과
- 외부 API 및 실제 스케줄러 실행 없이 Mock 기반 검증
- 기존 API 및 데이터베이스 스키마 변경 없음

---

## Sprint 22

### Docker Infrastructure

```text
Host Machine
  ↓
Docker Desktop / WSL2
  ↓
Docker Compose
  ├── FastAPI Backend
  │     ├── Python 3.13
  │     ├── Uvicorn
  │     ├── Alembic
  │     └── Healthcheck
  │
  └── PostgreSQL 17
        ├── Healthcheck
        └── Docker Named Volume
```

### Environment Configuration

```text
Local Development
  └── .env

Docker Development
  ├── .env.docker
  └── compose.yaml
        ↓
  Container Environment Variables
```

### Validation

- PostgreSQL 및 FastAPI 컨테이너 정상 실행
- 컨테이너 재시작 후 API 및 DB 연결 확인
- API 순차 요청 30회 성공, 실패 0회
- 평균 응답 시간 88.47ms
- 최대 응답 시간 2084.24ms
- 백엔드 테스트 85개 통과
- 프론트엔드 테스트 10개 통과
- 프론트엔드 Build / Lint 통과
- 동시 접속 부하 테스트 및 실제 운영 환경 검증은 미실시