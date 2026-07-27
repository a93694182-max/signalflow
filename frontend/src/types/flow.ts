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