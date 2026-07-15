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

