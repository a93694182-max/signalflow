export type SearchType = 'all' | 'flow' | 'evidence'

export interface FlowSearchItem {
  flow_id: number
  title: string
  target_asset: string
  summary: string | null
  created_at: string
}

export interface EvidenceSearchItem {
  evidence_id: number
  flow_id: number
  flow_title: string
  target_asset: string
  title: string
  source: string
  content_summary: string | null
  url: string | null
  published_at: string | null
}

export interface UnifiedSearchResponse {
  query: string
  total: number
  flow_count: number
  evidence_count: number
  flows: FlowSearchItem[]
  evidences: EvidenceSearchItem[]
}

export interface UnifiedSearchParams {
  q: string
  limit?: number
  type?: SearchType
  target_asset?: string
  from_date?: string
  to_date?: string
}