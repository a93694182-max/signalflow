export interface MarketTimelineEvidence {
  evidence_id: number
  title: string
  source: string
  url: string | null
}

export interface MarketTimelineCause {
  flow_id: number
  title: string
  target_asset: string
  relation_type: string
  score: number
  reason: string
}

export interface MarketTimelineItem {
  flow_id: number
  title: string
  target_asset: string
  summary: string | null
  score: number
  event_at: string
  evidence_count: number
  evidences: MarketTimelineEvidence[]
  causes: MarketTimelineCause[]
}

export interface MarketTimelineResponse {
  total: number
  limit: number
  target_asset: string | null
  timeline: MarketTimelineItem[]
}

export interface MarketTimelineParams {
  limit?: number
  target_asset?: string
  from_date?: string
  to_date?: string
  include_causes?: boolean
}