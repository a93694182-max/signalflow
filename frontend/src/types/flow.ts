export interface FlowFeedItem {
  flow_id: number
  title: string
  target_asset: string
  summary: string
  score: number
  evidence_count: number
  link_count: number
  created_at: string
  updated_at: string
}

export interface FlowFeedResponse {
  total: number
  limit: number
  offset: number
  flows: FlowFeedItem[]
}

export interface FlowFeedParams {
  limit?: number
  offset?: number
  target_asset?: string
  include_news?: boolean
  query?: string
  from_date?: string
  to_date?: string
  sort?: 'latest' | 'score'
}


export interface FlowEvidence {
  id: number
  flow_node_id: number
  evidence_type: string
  title: string
  source: string
  url: string | null
  content_summary: string
  relation_score: number
  impact_score: number
  time_score: number
  reliability_score: number
  published_at: string
}

export interface FlowNode {
  id: number
  order_index: number
  title: string
  category: string
  description: string
  occurred_at: string
  evidence_level: string
  evidences: FlowEvidence[]
}

export interface FlowTrace {
  id: number
  title: string
  target_asset: string
  summary: string
  nodes: FlowNode[]
}

export interface WhyCause {
  node_id: number
  title: string
  category: string
  description: string
  score: number
  evidence_count: number
}

export interface FlowWhyAnalysis {
  flow_id: number
  title: string
  target_asset: string
  summary: string
  primary_cause: WhyCause | null
  causes: WhyCause[]
  external_causes: unknown[]
}


export interface WhyTrailStep {
  source_flow_id: number
  source_title: string
  target_flow_id: number
  target_title: string
  relation_type: string
  score: number
  reason: string
}

export interface FlowWhyTrail {
  flow_id: number
  title: string
  trail_count: number
  trail: WhyTrailStep[]
}