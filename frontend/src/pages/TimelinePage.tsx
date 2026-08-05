import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { getMarketTimeline } from '../api/timeline'
import type {
  MarketTimelineParams,
  MarketTimelineResponse,
} from '../types/timeline'

const INITIAL_FILTERS: MarketTimelineParams = {
  limit: 20,
  target_asset: '',
  from_date: '',
  to_date: '',
  include_causes: true,
}

function formatDateTime(value: string) {
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

function TimelinePage() {
  const [timeline, setTimeline] =
    useState<MarketTimelineResponse | null>(null)

  const [filters, setFilters] =
    useState<MarketTimelineParams>(INITIAL_FILTERS)

  const [appliedFilters, setAppliedFilters] =
    useState<MarketTimelineParams>(INITIAL_FILTERS)

  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    async function loadTimeline() {
      try {
        const data = await getMarketTimeline(appliedFilters)

        if (isMounted) {
          setTimeline(data)
          setError('')
        }
      } catch {
        if (isMounted) {
          setError('시장 타임라인을 불러오지 못했습니다.')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    void loadTimeline()

    return () => {
      isMounted = false
    }
  }, [appliedFilters])

  function applyFilters() {
    if (
      filters.from_date &&
      filters.to_date &&
      filters.from_date > filters.to_date
    ) {
      setError('시작 날짜는 종료 날짜보다 늦을 수 없습니다.')
      return
    }

    setIsLoading(true)
    setError('')
    setAppliedFilters({ ...filters })
  }

  function resetFilters() {
    setFilters({ ...INITIAL_FILTERS })
    setIsLoading(true)
    setError('')
    setAppliedFilters({ ...INITIAL_FILTERS })
  }

  return (
    <section className="timeline-page">
      <div className="timeline-page__heading">
        <div>
          <p className="section-label">MARKET TIMELINE</p>
          <h1>시장 타임라인</h1>
          <p>시장 흐름과 연결된 원인을 시간순으로 확인합니다.</p>
        </div>

        <Link to="/">← 홈으로</Link>
      </div>

      <div className="timeline-filters">
        <select
          aria-label="자산 선택"
          value={filters.target_asset}
          onChange={(event) =>
            setFilters((current) => ({
              ...current,
              target_asset: event.target.value,
            }))
          }
        >
          <option value="">전체 자산</option>
          <option value="^KS11">KOSPI</option>
          <option value="^KQ11">KOSDAQ</option>
          <option value="KRW=X">원/달러</option>
          <option value="BTC-USD">비트코인</option>
          <option value="GC=F">금</option>
          <option value="CL=F">WTI</option>
        </select>

        <input
          aria-label="시작 날짜"
          type="date"
          value={filters.from_date}
          onChange={(event) =>
            setFilters((current) => ({
              ...current,
              from_date: event.target.value,
            }))
          }
        />

        <input
          aria-label="종료 날짜"
          type="date"
          value={filters.to_date}
          onChange={(event) =>
            setFilters((current) => ({
              ...current,
              to_date: event.target.value,
            }))
          }
        />

        <label className="timeline-filters__checkbox">
          <input
            type="checkbox"
            checked={filters.include_causes}
            onChange={(event) =>
              setFilters((current) => ({
                ...current,
                include_causes: event.target.checked,
              }))
            }
          />
          원인 포함
        </label>

        <button
          className="timeline-filters__button timeline-filters__button--primary"
          type="button"
          onClick={applyFilters}
        >
          적용
        </button>

        <button
          className="timeline-filters__button"
          type="button"
          onClick={resetFilters}
        >
          초기화
        </button>
      </div>

      {isLoading && (
        <div className="empty-state">
          시장 타임라인을 불러오는 중입니다.
        </div>
      )}

      {!isLoading && error && (
        <div className="error-state">{error}</div>
      )}

      {!isLoading &&
        !error &&
        timeline?.timeline.length === 0 && (
          <div className="empty-state">
            조건에 맞는 시장 흐름이 없습니다.
          </div>
        )}

      {!isLoading &&
        !error &&
        timeline &&
        timeline.timeline.length > 0 && (
          <div className="market-timeline__list">
            {timeline.timeline.map((item) => (
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
                    {item.causes.map((cause) => (
                      <Link
                        className="market-timeline__cause"
                        key={`${item.flow_id}-${cause.flow_id}`}
                        to={`/flows/${cause.flow_id}`}
                      >
                        <div className="market-timeline__cause-top">
                          <span>{cause.target_asset}</span>
                          <strong>{cause.score.toFixed(2)}</strong>
                        </div>

                        <p>{cause.title}</p>
                        <small>{cause.reason}</small>
                      </Link>
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

export default TimelinePage