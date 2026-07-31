import { apiGet } from './client'
import type {
  FlowFeedParams,
  FlowFeedResponse,
  FlowTrace,
  FlowWhyAnalysis,
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

export function getFlowTrace(flowId: number): Promise<FlowTrace> {
  return apiGet<FlowTrace>(`/flows/${flowId}/trace`)
}

export function getFlowWhy(
  flowId: number,
): Promise<FlowWhyAnalysis> {
  return apiGet<FlowWhyAnalysis>(`/flows/${flowId}/why`)
}