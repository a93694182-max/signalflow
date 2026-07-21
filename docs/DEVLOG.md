# DEVLOG

## 2026-07-12 | Sprint 1 시작

- SignalFlow 프로젝트 기획 및 백엔드 구조 설계
- FastAPI 프로젝트 생성
- Router, Service, Model, Schema 구조 구성
- GitHub Repository 생성 및 프로젝트 관리 시작

---

## 2026-07-13 | Sprint 1 진행

- PostgreSQL 설치 및 데이터베이스 생성
- SQLAlchemy ORM 모델(Flow, FlowNode, Evidence) 작성
- Alembic 설정 및 초기 Migration 생성
- 데이터베이스 테이블 생성
- Seed Data 작성 및 삽입
- Flow Trace API를 Mock 데이터에서 PostgreSQL 조회 방식으로 변경
- API를 통한 실제 DB 데이터 조회 확인

### Sprint 1 완료 ✅

- FastAPI + PostgreSQL + SQLAlchemy + Alembic 기반 백엔드 구축
- SignalFlow 기본 데이터 흐름(Flow → Node → Evidence) 구현



---

## 2026-07-14 | Sprint 2 진행


- Evidence API 구현 (GET /api/evidence/{id})
- Flow Trace API에 Evidence 포함
- Ask API 구현 (POST /api/ask)
- Yahoo Finance 연동
- Market Price API 구현
- Market Dashboard API 구현
- Market History API 구현
- FRED API 연동
- Economic API 구현 (GET /api/economic/fred/{series_id})


---

### Sprint 2 완료 ✅


- 실시간 금융 데이터(Yahoo Finance) 연동
- 미국 경제지표(FRED) 연동
- Flow + Evidence 기반 API 완성


- SignalFlow를 정적 데이터 프로젝트에서 실시간 데이터 플랫폼으로 확장

---



## 2026-07-15 | Sprint 3 진행

- Signal(dataclass) 설계
- Market / Economic Signal 생성 기능 구현
- Signal Normalizer 구현
- Signal Grouping 구현
- Flow Discovery 구현
- Flow 자동 생성 기능 구현
- FlowNode 자동 생성 기능 구현
- Evidence 자동 생성 기능 구현
- Signal Engine 구현
- Collector Service 구현
- Signal Filter 구현
- Engine API 구현 (POST /api/engine/run)
- APScheduler 기반 자동 실행 기능 구현
- 중복 Flow 생성 방지 로직 구현

### Sprint 3 완료 ✅

- Signal Engine 기반 이벤트 처리 파이프라인 구축
- 실시간 데이터 기반 Flow 자동 생성 기능 완성
- Collector → Filter → Grouping → Flow Discovery → DB 저장 구조 확립
- SignalFlow를 이벤트 기반 데이터 파이프라인으로 확장


## 2026-07-20 | Sprint 4 진행

- Finnhub News API 연동
- news_service 구현
- News Signal 생성
- Signal 모델 일반화
- Signal Filter 뉴스 지원
- News Flow 생성
- Evidence 생성 로직 개선
- Evidence Scoring Engine 구현
- Flow Ranking Engine 구현
- GET /api/flows/ranking API 추가
- Engine API 응답 개선
- 테스트 코드 작성 및 검증

### Sprint 4 완료 ✅

- 뉴스 데이터 기반 Flow 자동 생성
- Evidence Score 계산
- Flow Ranking 기능 구현
- SignalFlow 데이터 파이프라인 완성


---

## 2026-07-20 | Sprint 5 진행

- Why Analysis Engine 구현
- FlowNode별 Evidence 평균점수 계산
- Primary Cause 선정 로직 구현
- Confidence Score 및 Confidence Level 구현
- GET /api/flows/{flow_id}/why API 추가
- Flow Timeline 구현
- GET /api/flows/{flow_id}/timeline API 추가
- 뉴스 자동 주제 분류 구현
- 정규식 단어 경계 적용으로 부분 문자열 오분류 수정
- 금융·경제 비관련 뉴스 필터 구현
- Flow Ranking v2 구현
- Evidence Quality 및 Coverage Score 반영
- Ask API에 Why Analysis 결과 연결
- Ask API 구조화 응답 추가
- Swagger 및 단위 테스트 검증

### Sprint 5 완료 ✅

- Evidence 기반 Why Analysis 기능 완성
- Flow Timeline 조회 기능 완성
- 뉴스 주제별 Flow 생성 기반 마련
- 근거 품질과 개수를 반영한 Ranking 완성
- Why 기반 Ask API 완성





## 2026-07-21 | Sprint 6 진행

- FlowLink 모델 추가
- Alembic Migration 생성 및 PostgreSQL 적용
- Cross-Flow Linking Engine 구현
- 뉴스·경제지표 Flow와 시장 Flow 연결
- 카테고리·시간·근거 품질 기반 연결 점수 계산
- Signal Engine 응답에 link_count 추가
- GET /api/flows/{flow_id}/trail API 구현
- Ask API v3에 Why Trail 연결
- 중복 원인 후보 제거 및 상위 3개 제한
- OpenAI Responses API 연동 코드 구현
- OpenAI 미설정 시 Template Fallback 구현
- Cross-Flow Linking 테스트 작성
- FlowLink 저장 및 Why Trail 조회 테스트 작성
- 전체 테스트 통과

### Sprint 6 완료 ✅

- Flow 내부 분석을 Flow 간 원인 후보 분석으로 확장
- 뉴스·경제지표 → 시장 반응 Why Trail 구현
- OpenAI 설명 생성 구조 완성
- OpenAI 실제 호출 검증은 API Key 설정 후 진행

