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


# Sprint 3 

Scheduler

↓

Collector Service
│
├── Yahoo Finance
└── FRED

↓

Signal Service

↓

Signal Filter

↓

Flow Discovery

↓

Flow

↓

FlowNode

↓

Evidence

↓

PostgreSQL



# Sprint 4

Yahoo Finance

↓

FRED

↓

Finnhub News

↓ 

Collector

↓

Signal Filter

↓

Flow Discovery

↓

Evidence Scoring

↓

Flow Ranking

↓

PostgreSQL

↓

FastAPI API