import { apiPost } from './client'
import type {
  AskRequest,
  AskResponse,
} from '../types/ask'

export function askFlow(
  request: AskRequest,
): Promise<AskResponse> {
  return apiPost<AskResponse>('/ask', request)
}