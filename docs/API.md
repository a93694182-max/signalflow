# API

## Sprint 1

### Flow

#### GET /api/flows/{flow_id}/trace

Flow와 FlowNode를 PostgreSQL에서 조회한다.

Response
- Flow
- FlowNode

---

## Sprint 2

### Evidence

#### GET /api/evidence/{id}

Evidence 단건 조회

Response
- Evidence

---

### Ask

#### POST /api/ask

Flow, FlowNode, Evidence를 기반으로 응답을 생성한다.

Request
- flow_id
- question

Response
- answer

---

### Market

#### GET /api/market/price/{symbol}

시장 단일 데이터 조회

지원
- KOSPI
- KOSDAQ
- USD/KRW
- Bitcoin
- Gold
- WTI

---

#### GET /api/market/dashboard

실시간 시장 데이터를 한번에 조회

---

#### GET /api/market/history/{symbol}

시장 히스토리 조회

Query
- period
- interval

---

### Economic

#### GET /api/economic/fred/{series_id}

FRED 경제지표 조회

지원
- CPIAUCSL
- FEDFUNDS
- UNRATE
- GDP