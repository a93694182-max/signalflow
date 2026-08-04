import { apiGet } from './client'
import type {
  UnifiedSearchParams,
  UnifiedSearchResponse,
} from '../types/search'

export function searchSignalFlow(
  params: UnifiedSearchParams,
): Promise<UnifiedSearchResponse> {
  const searchParams = new URLSearchParams()

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') {
      searchParams.set(key, String(value))
    }
  })

  return apiGet<UnifiedSearchResponse>(
    `/search?${searchParams.toString()}`,
  )
}