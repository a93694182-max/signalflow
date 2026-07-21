
Flow
 │
 └── 1:N
        │
        ▼
    FlowNode
        │
        └── 1:N
                │
                ▼
            Evidence




Flow
 │
 ├── 1:N (source_flow_id)
 │        │
 │        ▼
 │    FlowLink
 │        ▲
 └── 1:N (target_flow_id)

FlowLink
- id (PK)
- source_flow_id (FK → Flow.id)
- target_flow_id (FK → Flow.id)
- relation_type
- score
- reason
- created_at