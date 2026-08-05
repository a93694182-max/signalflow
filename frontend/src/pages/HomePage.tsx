import { useEffect, useState } from 'react'

import { getHome } from '../api/home'
import { getMarketDashboard } from '../api/market'
import BiggestWhyCard from '../components/BiggestWhyCard'
import MarketOverview from '../components/MarketOverview'
import TopWhysList from '../components/TopWhysList'
import type { HomeResponse } from '../types/home'
import type { MarketItem } from '../types/market'
import FlowFeed from '../components/FlowFeed'
import MarketTimeline from '../components/MarketTimeline'


function HomePage() {
    const [home, setHome] = useState<HomeResponse | null>(null)
    const [markets, setMarkets] = useState<MarketItem[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function loadDashboard() {
            try {
                const [homeData, marketData] = await Promise.all([
                    getHome(),
                    getMarketDashboard(),
                ])

                setHome(homeData)
                setMarkets(marketData.markets)
            } catch {
                setError('대시보드 데이터를 불러오지 못했습니다.')
            } finally {
                setIsLoading(false)
            }
        }

        void loadDashboard()
    }, [])

    if (isLoading) {
        return <p>시장 흐름을 불러오는 중입니다...</p>
    }

    if (error) {
        return <p>{error}</p>
    }

    return (
        <main className="home-page">
            <MarketOverview markets={markets} />

            {home?.biggest_why ? (
                <>
                    <BiggestWhyCard flow={home.biggest_why} />
                    <TopWhysList flows={home.top_whys} />
                </>
            ) : (
                <div className="empty-state">
                    최근 24시간 동안 감지된 시장 흐름이 없습니다.
                </div>
            )}
            <MarketTimeline />
            <FlowFeed />
        </main>
    )
}

export default HomePage