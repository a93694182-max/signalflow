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
