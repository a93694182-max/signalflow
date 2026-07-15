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
- OpenAI 연동은 Sprint 4에서 진행

---

## Sprint 3

- Signal을 DB 테이블이 아닌 dataclass 기반 엔진 객체로 설계
- Signal → Flow → FlowNode → Evidence 파이프라인 구조 채택
- 동일 카테고리 Signal을 하나의 Flow로 그룹화
- Collector / Filter / Engine 계층 분리
- APScheduler를 이용한 Signal Engine 자동 실행
- Signal Engine을 API와 Scheduler 모두에서 재사용하도록 설계
- 중복 Flow 생성 방지 로직 추가

