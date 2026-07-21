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

## Sprint 4

- Finnhub를 뉴스 수집 API로 채택
- News를 Signal로 변환하여 기존 파이프라인 재사용
- Signal 모델을 범용 구조로 리팩터링
- Evidence Score를 Relation / Impact / Time / Reliability 기반으로 계산
- Flow Ranking은 Evidence 평균 점수 기반으로 계산
- Engine API는 Flow ID 대신 Flow 요약 정보를 반환

## Sprint 5

- Why Analysis는 OpenAI 없이 Evidence Score 기반의 결정적 로직으로 우선 구현
- FlowNode를 원인 후보 단위로 사용
- Node별 Evidence 평균점수를 원인 후보 점수로 사용
- 전체 Evidence 가중평균을 Why Analysis 신뢰도로 사용
- Confidence Level은 high / medium / low로 구분
- Flow Timeline은 FlowNode의 occurred_at 기준으로 정렬
- 뉴스 주제 분류는 키워드와 정규식 단어 경계를 사용
- 스포츠 등 금융·경제 비관련 뉴스는 Signal 생성 전에 제외
- Flow Ranking은 Evidence 품질 85%, 근거 개수 충족도 15%를 반영
- Evidence 5개를 Coverage Score 1.0 기준으로 설정
- Ask API는 Why Analysis 결과를 재사용
- OpenAI 연동은 데이터 기반 Why 구조가 안정된 이후 진행



## Sprint 6

- Flow 간 관계를 저장하기 위해 FlowLink 테이블 도입
- 원인 후보 Flow에서 시장 Flow 방향으로 연결
- 인과관계를 확정하지 않고 potential_cause로 표현
- 뉴스·경제지표 Evidence를 원인 후보로 사용
- Market Evidence를 연결 대상으로 사용
- 링크 점수는 카테고리 50%, 시간 30%, 근거 품질 20%로 계산
- 최대 연결 시간 범위를 72시간으로 설정
- 동일한 Flow 연결은 Unique Constraint로 중복 방지
- Ask API에서 상위 3개의 외부 원인 후보 사용
- OpenAI 호출 실패 시 템플릿 답변으로 대체
- OpenAI 실제 API 호출 검증은 API Key 설정 후 진행

