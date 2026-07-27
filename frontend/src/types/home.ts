export interface BiggestWhy {
  flow_id: number
  title: string
  target_asset: string
  summary: string
  score: number
  confidence_score: number
  confidence_level: string
  external_cause_count: number
  created_at: string
}

export interface TopWhy {
  flow_id: number
  title: string
  target_asset: string
  score: number
  created_at: string
}

export interface HomeResponse {
  biggest_why: BiggestWhy | null
  top_whys: TopWhy[]
}