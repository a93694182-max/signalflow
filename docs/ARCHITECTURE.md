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



---

# Sprint 9

## Frontend Foundation

Browser

↓

React + TypeScript + Vite

↓

Environment Configuration

└── VITE_API_BASE_URL

↓

API Client

↓

FastAPI CORS Middleware

↓

FastAPI API


## Home Dashboard

Home Page

├── Common Layout
├── Header
├── Market Overview
├── Biggest Why
├── Top Whys
└── Flow Feed

↓

Frontend API Layer

├── Home API
├── Market Dashboard API
└── Flow Feed API

↓

UI State

├── Loading
├── Error
└── Empty Data


## Flow Feed UI

Flow Filters

├── Search Query
├── Target Asset
├── News Inclusion
├── Date Range
└── Latest / Score Sort

↓

Flow Feed API

↓

Flow Cards

├── Score
├── Evidence Count
└── Link Count

↓

Offset Pagination



---

# Sprint 10

## Frontend Routing

Browser

↓

React Router

├── `/` Home Dashboard
├── `/flows/{flow_id}` Flow Detail
├── `/timeline` Market Timeline
└── `/search` Unified Search

↓

Common Layout

├── Header
├── Navigation
└── Page Content


## Flow Detail Page

Flow Feed Card

↓

Flow Detail Route

↓

Parallel API Requests

├── Flow Trace API
├── Why Analysis API
└── Why Trail API

↓

Flow Detail UI

├── Flow Summary
├── Why Analysis
├── Why Trail
├── Ask Flow
├── Flow Timeline
└── Evidence Cards


## Why Analysis UI

Why Analysis API

↓

Internal Cause Data

├── Primary Cause
├── Additional Causes
├── Cause Score
└── Evidence Count

↓

Why Analysis Component


## Why Trail UI

Why Trail API

↓

External Cause Data

├── Source Flow
├── Target Flow
├── Relation Type
├── Link Score
└── Link Reason

↓

Why Trail Component

↓

Connected Flow Detail Route


## Ask Flow UI

User Question

↓

Ask Flow Component

↓

API Client POST Request

↓

Ask API

↓

Answer Result

├── Answer
├── Confidence Score
├── Confidence Level
├── Answer Source
├── Primary Cause
├── Flow Path
├── Why Trail
└── Evidence Count


## Market Timeline Page

Timeline Filters

├── Target Asset
├── Date Range
└── External Cause Inclusion

↓

Market Timeline API

↓

Timeline Items

├── Event Time
├── Flow Score
├── Evidence Count
└── External Causes

↓

Flow Detail Route


## Unified Search Page

Search Form

├── Search Query
├── Search Type
├── Target Asset
└── Date Range

↓

Unified Search API

↓

Search Results

├── Flow Results
└── Evidence Results

↓

Result Navigation

├── Flow Detail Route
└── Evidence Original URL


## Frontend API Layer

API Client

├── GET Request
└── POST Request

↓

Feature API Modules

├── Flow API
├── Timeline API
├── Search API
└── Ask API

↓

TypeScript Response Types

├── Flow Types
├── Timeline Types
├── Search Types
└── Ask Types


## UI State

Frontend Pages

↓

State Handling

├── Loading
├── Error
├── Empty Data
├── Invalid Route Parameter
└── API Response Data


## Responsive UI

Desktop Layout

↓

CSS Grid / Flexbox / Vertical Timeline

↓

Media Query

↓

Mobile Layout