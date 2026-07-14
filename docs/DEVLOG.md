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

### 2026-07-14 | Sprint 2 진행

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

#### Sprint 2 완료 ✅

- 실시간 금융 데이터(Yahoo Finance) 연동
- 미국 경제지표(FRED) 연동
- Flow + Evidence 기반 API 완성
- SignalFlow를 정적 데이터 프로젝트에서 실시간 데이터 플랫폼으로 확장