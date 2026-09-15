import { apiGet } from './client'
import type { DailyBriefingResponse } from '../types/briefing'

export function getDailyBriefing(): Promise<DailyBriefingResponse> {
  return apiGet<DailyBriefingResponse>('/briefing/daily')
}