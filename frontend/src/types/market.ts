export interface MarketItem {
  symbol: string
  name: string
  price: number
  previous_close: number
  change: number
  change_percent: number
  currency: string
  market_time: string
}

export interface MarketDashboardResponse {
  markets: MarketItem[]
}