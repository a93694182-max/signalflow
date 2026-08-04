export interface AskRequest {
  flow_id: number
  question: string
}

export interface AskResponse {
  flow_id: number
  question: string
  answer: string
  confidence_score: number
  confidence_level: string
  primary_cause: string | null
  flow_path: string[]
  evidence_count: number
  answer_source: string
  why_trail: string[]
}