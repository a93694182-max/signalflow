export interface BriefingFlowItem {
  flow_id: number
  title: string
  target_asset: string
  score: number
  created_at: string
}

export interface DailyBriefingResponse {
  date: string
  headline: string
  summary: string
  top_flows: BriefingFlowItem[]
  key_causes: string[]
}