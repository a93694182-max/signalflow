import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { getMarketTimeline } from '../api/timeline'
import type { MarketTimelineItem } from '../types/timeline'

function formatDateTime(value: string) {
  return new Intl.DateTimeFormat('ko-KR', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

function MarketTimeline() {
  const [items, setItems] = useState<MarketTimelineItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadTimeline() {
      try {
        const data = await getMarketTimeline({
          limit: 8,
          include_causes: true,
        })

        setItems(data.timeline)
      } catch {
        setError('시장 타임라인을 불러오지 못했습니다.')
      } finally {
        setIsLoading(false)
      }
    }

    void loadTimeline()
  }, [])

  return (
    <section className="market-timeline">
      <div className="section-heading">
        <div>
          <p className="section-label">MARKET TIMELINE</p>
          <h2>시장 흐름 타임라인</h2>
        </div>

        <span>최근 감지된 흐름</span>
      </div>

      {isLoading && (
        <div className="empty-state">
          시장 타임라인을 불러오는 중입니다...
        </div>
      )}

      {error && <div className="empty-state">{error}</div>}

      {!isLoading && !error && items.length === 0 && (
        <div className="empty-state">
          표시할 시장 흐름이 없습니다.
        </div>
      )}

      {!isLoading && !error && items.length > 0 && (
        <div className="market-timeline__list">
          {items.map((item) => (
            <article
              className="market-timeline__card"
              key={item.flow_id}
            >
              <div className="market-timeline__top">
                <div className="market-timeline__meta">
                  <time dateTime={item.event_at}>
                    {formatDateTime(item.event_at)}
                  </time>

                  <span className="asset-badge">
                    {item.target_asset}
                  </span>
                </div>

                <span className="market-timeline__score">
                  {item.score.toFixed(2)}
                </span>
              </div>

              <Link
                className="market-timeline__title"
                to={`/flows/${item.flow_id}`}
              >
                {item.title}
              </Link>

              {item.summary && (
                <p className="market-timeline__summary">
                  {item.summary}
                </p>
              )}

              <div className="market-timeline__metrics">
                <span>근거 {item.evidence_count}개</span>
                <span>원인 {item.causes.length}개</span>
              </div>

              {item.causes.length > 0 && (
                <div className="market-timeline__causes">
                  {item.causes.slice(0, 2).map((cause) => (
                    <div
                      className="market-timeline__cause"
                      key={`${item.flow_id}-${cause.flow_id}`}
                    >
                      <div className="market-timeline__cause-top">
                        <span>{cause.target_asset}</span>
                        <strong>{cause.score.toFixed(2)}</strong>
                      </div>

                      <p>{cause.reason}</p>
                    </div>
                  ))}
                </div>
              )}
            </article>
          ))}
        </div>
      )}
    </section>
  )
}

export default MarketTimeline