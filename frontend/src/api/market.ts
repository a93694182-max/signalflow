import { apiGet } from './client'
import type { MarketDashboardResponse } from '../types/market'

export function getMarketDashboard(): Promise<MarketDashboardResponse> {
  return apiGet<MarketDashboardResponse>('/market/dashboard')
}