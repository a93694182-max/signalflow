# ERD

Flow
│
├── id
├── title
├── target_asset
├── summary
└── updated_at

        │ 1:N
        ▼

FlowNode
│
├── id
├── flow_id
├── order_index
├── title
├── category
├── description
├── occurred_at
└── evidence_level

        │ 1:N
        ▼

Evidence
│
├── id
├── flow_node_id
├── evidence_type
├── title
├── source
├── url
├── content_summary
├── relation_score
├── impact_score
├── time_score
├── reliability_score
├── published_at
└── created_at