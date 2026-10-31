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

export interface EvidenceScoreBreakdown {
  evidence_id: number
  title: string
  total_score: number
  scores: {
    relation: number
    impact: number
    time: number
    reliability: number
  }
  weights: {
    relation: number
    impact: number
    time: number
    reliability: number
  }
  weighted_scores: {
    relation: number
    impact: number
    time: number
    reliability: number
  }
}

export interface ConfidenceBreakdown {
  quality_score: number
  coverage_score: number
  quality_weight: number
  coverage_weight: number
  evidence_count: number
  raw_score: number
  confidence_cap: number | null
  confidence_score: number
  confidence_level: 'high' | 'medium' | 'low'
}

export interface CauseRankingItem {
  rank: number
  node_id: number
  title: string
  score: number
  evidence_count: number
  reason: string
}

export interface FlowWhyAnalysis {
  flow_id: number
  title: string
  target_asset: string
  summary: string
  confidence_score: number
  confidence_level: 'high' | 'medium' | 'low'
  primary_cause: WhyCause | null
  causes: WhyCause[]
  external_causes: unknown[]
  evidence_breakdowns: EvidenceScoreBreakdown[]
  confidence_breakdown: ConfidenceBreakdown
  cause_ranking: CauseRankingItem[]
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