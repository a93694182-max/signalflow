import { apiGet } from './client'
import type {
  FlowFeedParams,
  FlowFeedResponse,
} from '../types/flow'

export function getFlowFeed(
  params: FlowFeedParams = {},
): Promise<FlowFeedResponse> {
  const searchParams = new URLSearchParams()

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') {
      searchParams.set(key, String(value))
    }
  })

  const queryString = searchParams.toString()
  const path = queryString ? `/flows?${queryString}` : '/flows'

  return apiGet<FlowFeedResponse>(path)
}