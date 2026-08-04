import { apiGet } from './client'
import type {
  MarketTimelineParams,
  MarketTimelineResponse,
} from '../types/timeline'

export function getMarketTimeline(
  params: MarketTimelineParams = {},
): Promise<MarketTimelineResponse> {
  const searchParams = new URLSearchParams()

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') {
      searchParams.set(key, String(value))
    }
  })

  const queryString = searchParams.toString()
  const path = queryString
    ? `/timeline?${queryString}`
    : '/timeline'

  return apiGet<MarketTimelineResponse>(path)
}