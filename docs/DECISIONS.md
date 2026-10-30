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
- Why Analysis는 FlowNode 내부 원인과 FlowLink 외부 원인을 함께 반환
- 외부 원인 후보는 연결 점수순 상위 3개로 제한
- Primary Cause는 기존 내부 시장 신호 구조를 유지
- 외부 Flow는 인과관계를 확정하지 않고 원인 후보로 구분




## Sprint 7

- Home API는 고정 Mock 대신 실제 Flow Ranking 결과를 사용
- Ranking 1위를 biggest_why, 2~4위를 top_whys로 선정
- 홈은 현재 상황을 보여주기 위해 최근 24시간 Flow만 사용
- 뉴스 Flow는 외부 원인 후보이므로 Home Ranking에서 제외
- 기존 Flow Ranking과 Why Analysis 로직을 Home API에서 재사용
- Flow Feed 페이지네이션은 limit과 offset 방식으로 구현
- 최신순은 created_at과 id 내림차순으로 정렬
- 점수순은 기존 Flow Ranking v2 기준을 재사용
- Flow Feed의 전체 개수에도 동일한 검색·필터 조건 적용
- 기간 필터는 Asia/Seoul 기준이며 종료일 전체를 포함
- Feed 항목에 Score, Evidence Count, Link Count 제공
- FastAPI 애플리케이션 시작 처리를 lifespan 방식으로 전환



## Sprint 8

- 기존 Flow Timeline은 단일 Flow 내부의 FlowNode 시간 흐름으로 유지
- Market Timeline은 여러 Flow 사이의 시장 흐름을 조회하는 별도 API로 분리
- Market Timeline은 최근 Flow를 선택한 뒤 시간 오름차순으로 반환
- Timeline Ranking Score는 기존 Flow Ranking v2를 재사용
- Timeline Evidence 요약과 외부 원인 후보는 각각 상위 3개로 제한
- 외부 원인 후보는 FlowLink의 incoming link를 사용
- Market Timeline과 Unified Search는 기존 테이블을 조합하여 구현
- Unified Search는 Flow와 Evidence 결과를 유형별로 분리하여 반환
- 검색 범위는 Flow 제목·요약과 Evidence 제목·내용·출처로 설정
- 기간 필터는 Asia/Seoul 기준이며 종료일 전체를 포함
- 공백 검색어는 전체 데이터 노출 방지를 위해 422로 거부


---

## Sprint 9

- 프론트엔드는 React + TypeScript + Vite 조합으로 구축
- ESLint를 기본 코드 검사 도구로 사용
- API 주소는 `VITE_API_BASE_URL` 환경변수로 관리
- 공통 요청 로직은 API Client로 분리
- API 요청 함수와 응답 타입을 `api` 및 `types` 계층으로 분리
- Home Dashboard는 기존 Home·Market·Flow Feed API를 재사용
- Home과 Market 데이터는 병렬 요청
- Flow Feed는 독립 상태로 필터와 페이지네이션을 관리
- 검색 조건은 입력 즉시 요청하지 않고 적용 버튼으로 반영
- UI 라이브러리 없이 CSS Grid와 Media Query로 반응형 UI 구현
- 새로운 DB 테이블과 백엔드 API는 추가하지 않음

---

## Sprint 10

- React Router를 도입하여 Home과 Flow Detail 페이지를 분리
- Flow Feed 카드를 Flow Detail 페이지의 진입점으로 사용
- Flow Detail 데이터는 Trace, Why Analysis, Why Trail API를 병렬 요청
- URL의 `flow_id`는 프론트엔드에서 양의 정수로 검증
- Why Analysis는 내부 원인, Why Trail은 외부 Flow 원인으로 구분
- FlowNode 내부에 Evidence를 표시하여 원인과 근거의 관계를 유지
- Ask UI는 현재 Flow ID를 자동으로 요청에 포함
- 공통 API Client에 POST 요청 기능 추가
- Header에 주요 페이지 내비게이션 추가
- 새로운 DB 테이블과 백엔드 API는 추가하지 않음

---

## Sprint 11

- Market Timeline과 Unified Search를 독립 페이지로 제공
- Timeline과 Home의 시장 흐름 UI는 공통 카드 스타일을 재사용
- Timeline 필터는 적용 버튼을 통해 요청에 반영
- Unified Search는 기존 Search API 하나로 Flow와 Evidence를 함께 조회
- Flow와 Evidence 결과는 유형별 영역으로 구분하여 표시
- 공백 검색어와 잘못된 날짜 범위는 프론트엔드에서 사전 차단
- 검색 결과는 Flow 상세 페이지와 Evidence 원문으로 연결
- 새로운 DB 테이블과 백엔드 API는 추가하지 않음


---

## Sprint 12

- Daily Briefing은 기존 Flow Ranking과 Why Analysis를 재사용
- 최근 24시간 Flow를 브리핑 분석 범위로 사용
- MARKET Flow는 주요 시장 자산 Flow 선정에서 제외
- 상위 3개 Flow를 Daily Briefing에 제공
- 외부 연결 원인을 우선 Key Cause로 사용
- 외부 원인이 없으면 내부 Primary Cause를 사용
- Home Dashboard 데이터는 60초 주기로 자동 갱신
- 새로운 DB 테이블은 추가하지 않음
---

## Sprint 13

- 기존 Ask API를 유지하면서 AI 설명 생성 로직 개선
- AI 설명은 Flow Trace, Why Analysis, Why Trail을 기반으로 생성
- Evidence 제목 최대 10개를 프롬프트에 포함
- 근거 없는 단정과 불확실한 인과관계 표현을 제한
- OpenAI 호출은 `OPENAI_ENABLED` 환경변수로 제어
- 기본값은 `false`로 설정하여 불필요한 API 비용 방지
- API 비활성화 또는 호출 실패 시 Template Fallback 사용
- 외부 API 비용 없이 검증할 수 있도록 Mock 테스트 활용
- 프론트엔드에 AI 분석 / 기본 분석 배지 추가
- 새로운 DB 테이블 및 API Endpoint는 추가하지 않음


---

## Sprint 14

- 동일 자산의 Flow라도 노드 내용이 다르면 별도 Flow로 처리
- Flow 제목, 대상 자산, 발생 시각을 기준으로 중복 후보 검색
- 전체 FlowNode의 제목, 카테고리, 설명, 발생 시각으로 최종 중복 판정
- 발생 시각 비교 시 UTC 기준으로 정규화
- 중복 Flow는 신규 생성 결과 및 Cross-Flow Linking 대상에서 제외
- 뉴스 ID, URL, 제목 중 하나라도 중복되면 최초 Signal 유지
- 뉴스 중복 제거 범위는 단일 엔진 실행으로 제한
- 경제·금융 키워드가 포함된 뉴스만 관련 뉴스로 판단
- 키워드 기반 필터링의 오탐 및 누락 가능성은 향후 개선 대상으로 유지
- 외부 API에 의존하는 테스트는 고정 Signal 기반으로 변경
- 기존 데이터베이스 스키마 유지


---

## Sprint 16

- 기존 Evidence Score 계산 로직을 유지하고 점수 구성 요소를 별도로 제공
- Evidence Score 가중치는 Relation 0.3, Impact 0.2, Time 0.2, Reliability 0.3으로 유지
- Confidence Score는 Quality Score와 Coverage Score의 가중합을 사용
- Confidence Score 계산 과정과 최종 결과를 함께 제공
- Evidence 개수에 따른 Confidence Score 상한 정책 유지
- Evidence가 없으면 Confidence Score를 0으로 처리
- Cause Ranking은 Evidence 평균 점수와 Evidence 개수를 기준으로 정렬
- Cause Ranking에 순위 및 선정 이유 추가
- Primary Cause는 기존 Why Analysis 결과를 유지
- Explainability 기능은 기존 계산 로직을 재사용하도록 구성
- 새로운 API Endpoint를 추가하지 않고 기존 Why Analysis API 확장
- 기존 Response 필드를 유지하여 하위 호환성 확보
- 새로운 데이터베이스 테이블 및 컬럼 추가 없음

---