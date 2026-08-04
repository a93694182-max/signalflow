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
        getMarketTimeline(appliedFilters)
            .then(setTimeline)
            .catch(() => {
                setError('시장 타임라인을 불러오지 못했습니다.')
            })
            .finally(() => {
                setIsLoading(false)
            })
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
                    type="date"
                    value={filters.to_date}
                    onChange={(event) =>
                        setFilters((current) => ({
                            ...current,
                            to_date: event.target.value,
                        }))
                    }
                />

                <label>
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

                <button type="button" onClick={applyFilters}>
                    적용
                </button>

                <button type="button" onClick={resetFilters}>
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
                    <div className="market-timeline">
                        {timeline.timeline.map((item) => (
                            <article
                                className="market-timeline-card"
                                key={item.flow_id}
                            >
                                <time dateTime={item.event_at}>
                                    {new Date(item.event_at).toLocaleString('ko-KR')}
                                </time>

                                <div className="market-timeline-card__body">
                                    <div className="market-timeline-card__top">
                                        <span>{item.target_asset}</span>
                                        <strong>
                                            {Math.round(item.score * 100)}점
                                        </strong>
                                    </div>

                                    <Link to={`/flows/${item.flow_id}`}>
                                        {item.title}
                                    </Link>

                                    {item.summary && <p>{item.summary}</p>}

                                    <small>근거 {item.evidence_count}개</small>

                                    {item.causes.length > 0 && (
                                        <div className="market-timeline-causes">
                                            <strong>연결 원인</strong>

                                            {item.causes.map((cause) => (
                                                <Link
                                                    key={cause.flow_id}
                                                    to={`/flows/${cause.flow_id}`}
                                                >
                                                    {cause.title} ·{' '}
                                                    {Math.round(cause.score * 100)}점
                                                </Link>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </article>
                        ))}
                    </div>
                )}
        </section>
    )
}

export default TimelinePage