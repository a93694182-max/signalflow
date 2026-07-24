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


# Sprint 5

External News

↓

News Relevance Filter

↓

News Topic Classifier

↓

Topic-based Signal Grouping

↓

Flow / FlowNode / Evidence

↓

Why Analysis Engine

├── Cause Ranking
├── Primary Cause
└── Confidence Score

↓

Flow Timeline

↓

Flow Ranking v2

├── Evidence Quality
└── Evidence Coverage

↓

Ask API v2



---

# Sprint 6

News / Economic Flow

↓

Cross-Flow Linking

├── Category Score
├── Time Score
└── Evidence Quality Score

↓

FlowLink

↓

Market Flow

↓

Why Trail API

↓

Ask API v3

├── OpenAI Explanation
└── Template Fallback

Why Analysis v2

├── External Causes (FlowLink)
├── Internal Causes (FlowNode)
├── Primary Internal Signal
└── Cross-Flow Summary


---

---

# Sprint 7

## Home Intelligence

PostgreSQL Flow Data

↓

Recent Flow Filter

├── 최근 24시간
└── News Flow 제외

↓

Flow Ranking

↓

Why Analysis

↓

Home API

├── Biggest Why
└── Top Whys


## Flow Feed

PostgreSQL Flow Data

↓

Flow Feed Query

├── Pagination
├── Target Asset Filter
├── News Filter
├── Title Search
├── Date Filter
└── Latest / Score Sort

↓

Flow Ranking v2

↓

Feed Summary

├── Score
├── Evidence Count
└── Link Count

↓

Flow Feed API



---


# Sprint 8

## Market Timeline

PostgreSQL Flow Data

↓

Target Asset / Date Filter

↓

Recent Flow Selection

↓

Time Order

↓

Flow Ranking v2

↓

Timeline Enrichment

├── Evidence Summary
└── External Causes (FlowLink)

↓

Market Timeline API


## Unified Search

Search Query

↓

Unified Search Service

├── Flow Title / Summary
└── Evidence Title / Summary / Source

↓

Target Asset / Date / Type Filter

↓

Flow Results + Evidence Results

↓

Unified Search API