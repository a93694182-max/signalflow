# Decisions

## Sprint 1

- FastAPI를 백엔드 프레임워크로 채택
- PostgreSQL을 메인 데이터베이스로 사용
- SQLAlchemy ORM 사용
- Alembic으로 Migration 관리
- Router / Service / Model / Schema 구조 채택
- Mock 대신 실제 DB 조회 방식 사용

---

## Sprint 2

- Yahoo Finance를 실시간 시장 데이터 API로 채택
- FRED를 경제지표 API로 채택
- Ask API는 DB 기반으로 우선 구현
- OpenAI 연동은 Sprint 3에서 진행