# Architecture

## Sprint 1

Client

↓

FastAPI Router

↓

Service Layer

↓

SQLAlchemy ORM

↓

PostgreSQL

---

## Sprint 2

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


# Sprint 3 Architecture

Scheduler
│
▼
Collector Service
│
├── Yahoo Finance
└── FRED

▼

Signal Service

▼

Signal Filter

▼

Flow Discovery

▼

Flow

▼

FlowNode

▼

Evidence

▼

PostgreSQL

---

새로운 컴포넌트

- collector_service
- signal_service
- signal_filter_service
- engine_service
- scheduler_service
- Signal(dataclass)
