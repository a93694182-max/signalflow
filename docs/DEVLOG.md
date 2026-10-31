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



---

## 2026-07-21 | Sprint 6 진행

- FlowLink 모델 추가
- Alembic Migration 생성 및 PostgreSQL 적용
- Cross-Flow Linking Engine 구현
- 뉴스·경제지표 Flow와 시장 Flow 연결
- 카테고리·시간·근거 품질 기반 연결 점수 계산
- Signal Engine 응답에 `link_count` 추가
- `GET /api/flows/{flow_id}/trail` API 구현
- Ask API v3에 Why Trail 연결
- 중복 원인 후보 제거 및 상위 3개 제한
- OpenAI Responses API 연동 코드 구현
- OpenAI 미설정 시 Template Fallback 구현
- Cross-Flow Linking 테스트 작성
- FlowLink 저장 및 Why Trail 조회 테스트 작성

---

## 2026-07-21 | Sprint 6 고도화

- Why Analysis v2 구현
- `GET /api/flows/{flow_id}/why`에 `external_causes` 추가
- 외부 원인 후보와 내부 시장 신호를 결합한 `summary` 생성
- Cross-Flow Why Analysis 테스트 추가
- 전체 테스트 5개 통과

### Sprint 6 완료 ✅

- Flow 내부 분석을 Flow 간 원인 후보 분석으로 확장
- 뉴스·경제지표 → 시장 반응 Why Trail 구현
- OpenAI 설명 생성 구조 완성
- OpenAI 실제 호출 검증은 API Key 설정 후 진행




---



## 2026-07-21 ~ 2026-07-23 | Sprint 7 진행

- Home API Mock 제거
- DB 기반 Home Intelligence Service 구현
- Flow Ranking 기반 biggest_why 및 top_whys 구성
- 최근 24시간 Flow 필터 구현
- Home Ranking에서 뉴스 Flow 제외
- Why Analysis 요약 및 Confidence 정보 연결
- GET /api/flows Flow Feed API 구현
- limit 및 offset 페이지네이션 구현
- Target Asset 및 뉴스 포함 여부 필터 구현
- Flow 제목 검색 구현
- Asia/Seoul 기준 기간 필터 구현
- 잘못된 날짜 범위 422 검증
- latest 및 score 정렬 구현
- 기존 Flow Ranking v2 점수 기준 재사용
- Feed에 Score, Evidence Count, Link Count 추가
- FastAPI startup 이벤트를 lifespan 방식으로 전환
- Home Service 테스트 작성
- Flow Feed Service 테스트 7개 작성
- Flow Feed API 테스트 3개 작성
- 전체 테스트 17개 통과

### Sprint 7 완료 ✅

- 실제 데이터 기반 Home Intelligence API 완성
- 프론트엔드용 Flow Feed API 완성
- 검색·필터·기간 조회·정렬·페이지네이션 완성
- 사용자 조회 계층 구축



---

## 2026-07-24 | Sprint 8 진행

- Market Timeline 응답 Schema 구현
- Market Timeline Service 구현
- `GET /api/timeline` API 추가
- 최근 Flow 선택 및 시간 오름차순 반환
- Target Asset 및 기간 필터 구현
- Flow Ranking v2 Score 연결
- Timeline에 Evidence 요약 추가
- FlowLink 기반 외부 원인 후보 추가
- 외부 원인 후보 포함 여부 옵션 구현
- Flow·Evidence Unified Search 구현
- `GET /api/search` API 추가
- Flow 제목·요약 검색 구현
- Evidence 제목·내용·출처 검색 구현
- 검색 유형·자산·기간 필터 구현
- 공백 검색어 및 잘못된 날짜 범위 검증
- Market Timeline 테스트 6개 작성
- Unified Search 테스트 6개 작성
- 전체 테스트 29개 통과

### Sprint 8 완료 ✅

- 여러 시장 Flow의 시간 흐름을 조회하는 Market Timeline 완성
- Flow Ranking, Evidence, 외부 원인을 결합한 Timeline 응답 완성
- Flow와 Evidence를 한 번에 조회하는 통합 검색 완성
- SignalFlow의 탐색 및 시장 흐름 조회 계층 구축


---

## 2026-07-24 ~ 2026-07-27 | Sprint 9 진행

- React + TypeScript + Vite 프론트엔드 구축
- ESLint 및 환경변수 설정
- FastAPI CORS 연동
- 공통 레이아웃 및 Header 구현
- Home Dashboard 구현
  - Market Overview
  - Biggest Why
  - Top Whys
  - Flow Feed
- Flow Feed 검색·필터·정렬·페이지네이션 구현
- 반응형 UI 구현
- 프론트엔드 ESLint 및 Production Build 통과
- 백엔드 전체 테스트 29개 통과

### Sprint 9 완료 ✅

- React 기반 첫 사용자 화면 구축
- Home Dashboard와 백엔드 API 연동 완료
- 검색·필터·정렬 기능을 갖춘 Flow Feed 완성


---

## 2026-07-27 ~ 2026-08-04 | Sprint 10 진행

- React Router 기반 페이지 구조 구성
- Flow Detail 페이지 구현
  - Flow Trace
  - Why Analysis
  - Why Trail
  - Ask UI
  - Evidence 표시
- Market Timeline 페이지 구현
- Unified Search 페이지 구현
- 공통 API Client 개선 (POST 지원)
- Header 내비게이션 추가
- 반응형 UI 개선
- PostgreSQL Migration 및 Seed 데이터 정리
- Signal Engine 실행 및 데이터 검증
- 프론트엔드 ESLint 및 Production Build 통과
- 백엔드 전체 테스트 29개 통과

### Sprint 10 완료 ✅

- Flow 상세 분석 화면 완성
- Market Timeline 및 Unified Search 화면 완성
- Home → Detail → Timeline → Search 사용자 흐름 구축

--- 

## 2026-08-05 | Sprint 11 진행

- Timeline 페이지 개선
- Timeline 필터 및 UI 개선
- Search 페이지 구현
- Unified Search 연동
- Flow / Evidence 검색 지원
- 날짜 필터 검증 추가
- Home UI 개선
- 프론트엔드 ESLint 및 Production Build 통과

### Sprint 11 완료 ✅

- Timeline 화면 개선 및 필터 기능 완성
- Unified Search 기반 검색 화면 완성
- Home · Timeline · Search UI 통일



---

## 2026-09-15 | Sprint 12 진행

- Daily Market Briefing Schema 구현
- Daily Briefing Service 구현
- Daily Briefing API 추가
- Flow Ranking 및 Why Analysis 연동
- Daily Briefing UI 구현
- Home Dashboard 연동
- 60초 자동 갱신 추가
- Daily Briefing Service 테스트 추가
- 백엔드 전체 테스트 31개 통과
- 프론트엔드 ESLint 및 Production Build 통과

### Sprint 12 완료 ✅

- 기존 Flow 분석 데이터를 종합하는 Daily Market Briefing 완성
- Home Dashboard에 시장 브리핑 통합
- Dashboard 자동 갱신 적용
---



## 2026-10-28 | Sprint 13 진행

- Evidence 기반 AI 프롬프트 개선
- Flow Trace / Why Analysis / Why Trail 연동
- OpenAI 답변 생성 로직 개선
- AI 호출 실패 시 Template Fallback 유지
- `OPENAI_ENABLED` 환경변수 추가
- API 비활성화 시 실제 OpenAI 호출 방지
- OpenAI 성공 / 실패 Mock 테스트 추가
- AI 답변 / 기본 답변 / 원인 부재 테스트 추가
- Ask UI에 분석 유형 배지 추가
- 백엔드 전체 테스트 36개 통과
- 프론트엔드 ESLint 및 Production Build 통과
- 실제 OpenAI API 응답은 크레딧 부족으로 미검증

### Sprint 13 완료 ✅

- Evidence 기반 AI 설명 구조 개선
- AI 호출 활성화 설정 및 Fallback 처리
- Ask UI 분석 유형 구분
- Mock 기반 AI 로직 검증 완료


---

## 2026-10-28 | Sprint 14 진행

- 중복 Flow의 신규 생성 결과 반환 방지
- FlowNode 전체 내용 기반 중복 판정 개선
- Flow 발생 시각 UTC 정규화
- 뉴스 ID 기반 중복 제거 구현
- 뉴스 URL 기반 중복 제거 구현
- 뉴스 제목 공백 및 대소문자 정규화
- 경제·금융 키워드 기반 뉴스 관련성 필터링 개선
- 경제적 영향이 있는 스포츠 뉴스 허용
- 외부 뉴스 API에 의존하던 테스트 개선
- 중복 Flow 테스트 2개 추가
- 뉴스 중복 제거 테스트 4개 추가
- 뉴스 관련성 테스트 4개 추가
- 뉴스 Flow 테스트 2개 추가
- 백엔드 전체 테스트 48개 통과

### Sprint 14 완료 ✅

- Flow 및 뉴스 중복 제거를 통한 데이터 품질 개선
- 경제·금융 관련 뉴스 중심의 Signal 수집 체계 강화
- 외부 API 상태와 무관한 테스트 환경 개선
- 기존 API 및 데이터베이스 구조 유지



---


---

## 2026-10-30 | Sprint 16 진행

- Evidence Score Breakdown 구현
- Evidence 원본 점수 및 가중치 제공
- Evidence 가중 점수 계산 결과 제공
- Confidence Score Breakdown 구현
- Quality Score 및 Coverage Score 계산 과정 제공
- Evidence 개수별 Confidence Score 상한 정보 제공
- Cause Ranking Explanation 구현
- 원인 후보별 순위 및 선정 이유 제공
- Evidence 개수가 없는 원인 후보 처리
- Cause Ranking 동점 처리 테스트 추가
- Primary Cause와 Cause Ranking 일치 여부 검증
- Confidence Breakdown과 Why Analysis 결과 일치 여부 검증
- Why Analysis API 응답 Schema 확장
- Evidence Breakdown API 응답 추가
- Confidence Breakdown API 응답 추가
- Cause Ranking API 응답 추가
- Why API 응답 테스트 2개 추가
- Evidence가 없는 Flow의 API 응답 검증
- 백엔드 전체 테스트 75개 통과

### Sprint 16 완료 ✅

- Evidence Score 계산 과정 설명 기능 완성
- Confidence Score 계산 근거 제공
- Cause Ranking 선정 이유 제공
- Why Analysis 결과 일관성 검증
- 기존 Why Analysis API의 Explainability 확장
- 기존 데이터베이스 구조 유지

---

## 2026-10-31 | Sprint 17 진행

- Flow Detail Explainability UI 구현
- Evidence Score Breakdown 컴포넌트 추가
- Evidence별 원본 점수, 가중치 및 기여도 시각화
- Confidence Score Breakdown 컴포넌트 추가
- Quality Score와 Coverage Score 계산 과정 표시
- Confidence Score 상한 및 등급 표시
- Cause Ranking 컴포넌트 추가
- 원인 후보 순위, 점수, 근거 개수 및 선정 이유 표시
- 기존 Why Analysis API 응답 재사용
- 잘못된 Flow ID 및 API 요청 실패 화면 확인
- 실제 Flow 상세 페이지에서 Explainability UI 검증
- 프론트엔드 ESLint 및 Production Build 통과
- 백엔드 전체 테스트 75개 통과

### Sprint 17 완료 ✅

- Evidence Score 계산 과정 시각화
- Confidence Score 계산 근거 시각화
- Cause Ranking 선정 이유 표시
- Flow Detail Explainability UI 통합
- 기존 API 및 데이터베이스 구조 유지

---

---

## 2026-10-31 | Sprint 18 진행

- Cause Ranking 공통 정렬 함수 `rank_causes()` 구현
- Why Analysis와 Cause Ranking의 정렬 기준 통합
- Evidence 평균 점수 기준 내림차순 정렬
- Evidence 개수 기준 동점 처리
- Node ID 기준 최종 동점 처리
- Cause Ranking 선정 이유 개선
- Ranking 1위 동점 선정 이유 개선
- 입력 순서 독립성 테스트 추가
- Evidence 개수 동점 처리 테스트 추가
- Node ID 동점 처리 테스트 추가
- Ranking 1위 선정 이유 테스트 추가
- Primary Cause와 Ranking 1위 일관성 테스트 추가
- Evidence가 없는 Flow의 Primary Cause 검증
- 백엔드 전체 테스트 82개 통과

### Sprint 18 완료 ✅

- Cause Ranking 정렬 기준 통합
- 동점 처리 결과의 일관성 확보
- 실제 정렬 기준에 맞는 Ranking 선정 이유 제공
- Primary Cause와 Cause Ranking 일관성 검증
- 기존 API 및 데이터베이스 구조 유지

---


## 2026-10-31 | Sprint 19 진행

- Confidence Breakdown UI 개선
- Confidence Level별 설명 추가
- Evidence 0개인 경우 근거 부족 경고 추가
- Evidence 1개인 경우 신중한 해석 안내 추가
- Cause Ranking 동일 점수 배지 추가
- API 원본 점수 기반 동점 여부 판단
- `ApiError` 클래스 구현
- TypeScript `erasableSyntaxOnly` 설정 호환성 수정
- Flow Detail HTTP 404 오류 메시지 구분
- HTTP 5xx 서버 오류 메시지 구분
- 네트워크 연결 실패 메시지 구분
- 존재하지 않는 Flow ID 화면 검증
- 프론트엔드 ESLint 및 Production Build 통과
- 백엔드 전체 테스트 82개 통과

### Sprint 19 완료 ✅

- 분석 신뢰도 해석 안내 개선
- 근거 부족 상황의 사용자 안내 강화
- Cause Ranking 동점 후보 시각화
- Flow Detail 오류 유형별 메시지 제공
- 기존 API 및 데이터베이스 구조 유지

---

## 2026-10-31 | Sprint 20 진행

- Flow Detail 비동기 요청 처리 구조 점검
- Flow ID 변경 시 이전 요청 결과 반영 방지
- `isActive` 기반 요청 생명주기 관리
- 현재 URL과 로딩된 Flow ID의 일치 여부 검증
- `loadedFlowId`를 활용한 중간 로딩 상태 개선
- Flow Detail 상태를 `FlowDetailState`로 통합
- 로딩, 성공, 오류 상태 분리
- 기존 개별 상태 관리 코드 제거
- 기존 HTTP 오류 메시지 처리 유지
- Why Analysis, Why Trail 및 Explainability UI 유지
- 프론트엔드 ESLint 및 Production Build 통과
- Flow Detail 정상 및 오류 화면 검증

### Sprint 20 완료 ✅

- Flow ID 변경 시 데이터 일관성 개선
- 이전 비동기 요청에 의한 화면 충돌 방지
- Flow Detail 상태 관리 구조 단순화
- 기존 API 및 데이터베이스 구조 유지

---