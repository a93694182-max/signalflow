import { apiGet } from './client'
import type { HomeResponse } from '../types/home'

export function getHome(): Promise<HomeResponse> {
  return apiGet<HomeResponse>('/home')
}