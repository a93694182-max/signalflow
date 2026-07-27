import { useEffect, useState } from 'react'

import { getFlowFeed } from '../api/flows'
import FlowFilters from './FlowFilters'
import type { FlowFilterValues } from './FlowFilters'
import type { FlowFeedResponse } from '../types/flow'

const PAGE_SIZE = 6

const INITIAL_FILTERS: FlowFilterValues = {
  target_asset: '',
  include_news: true,
  query: '',
  from_date: '',
  to_date: '',
  sort: 'latest',
}

function FlowFeed() {
  const [feed, setFeed] = useState<FlowFeedResponse | null>(null)
  const [filters, setFilters] =
    useState<FlowFilterValues>(INITIAL_FILTERS)
  const [appliedFilters, setAppliedFilters] =
    useState<FlowFilterValues>(INITIAL_FILTERS)
  const [page, setPage] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadFlows() {
      setIsLoading(true)
      setError(null)

      try {
        const data = await getFlowFeed({
          limit: PAGE_SIZE,
          offset: page * PAGE_SIZE,
          target_asset: appliedFilters.target_asset,
          include_news: appliedFilters.include_news,
          query: appliedFilters.query,
          from_date: appliedFilters.from_date,
          to_date: appliedFilters.to_date,
          sort: appliedFilters.sort,
        })

        setFeed(data)
      } catch {
        setError('Flow 목록을 불러오지 못했습니다.')
      } finally {
        setIsLoading(false)
      }
    }

    void loadFlows()
  }, [appliedFilters, page])

  function applyFilters() {
    if (
      filters.from_date &&
      filters.to_date &&
      filters.from_date > filters.to_date
    ) {
      setError('시작 날짜는 종료 날짜보다 늦을 수 없습니다.')
      return
    }

    setPage(0)
    setAppliedFilters({ ...filters })
  }

  function resetFilters() {
    setFilters({ ...INITIAL_FILTERS })
    setAppliedFilters({ ...INITIAL_FILTERS })
    setPage(0)
  }

  const totalPages = Math.ceil((feed?.total ?? 0) / PAGE_SIZE)

  return (
    <section className="flow-feed">
      <div className="section-heading">
        <div>
          <p className="section-label">FLOW FEED</p>
          <h2>최근 시장 흐름</h2>
        </div>

        <span>전체 {feed?.total ?? 0}개</span>
      </div>

      <FlowFilters
        values={filters}
        onChange={setFilters}
        onSubmit={applyFilters}
        onReset={resetFilters}
      />

      {isLoading && (
        <div className="empty-state">Flow를 불러오는 중입니다...</div>
      )}

      {!isLoading && error && (
        <div className="error-state">{error}</div>
      )}

      {!isLoading && !error && feed?.flows.length === 0 && (
        <div className="empty-state">
          조건에 맞는 Flow가 없습니다.
        </div>
      )}

      {!isLoading && !error && feed && feed.flows.length > 0 && (
        <>
          <div className="flow-feed__list">
            {feed.flows.map((flow) => (
              <article className="flow-card" key={flow.flow_id}>
                <div className="flow-card__top">
                  <span className="asset-badge">
                    {flow.target_asset}
                  </span>

                  <time dateTime={flow.created_at}>
                    {new Intl.DateTimeFormat('ko-KR', {
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                    }).format(new Date(flow.created_at))}
                  </time>
                </div>

                <h3>{flow.title}</h3>
                <p>{flow.summary}</p>

                <div className="flow-card__metrics">
                  <span>
                    중요도 {Math.round(flow.score * 100)}점
                  </span>
                  <span>근거 {flow.evidence_count}개</span>
                  <span>연결 {flow.link_count}개</span>
                </div>
              </article>
            ))}
          </div>

          {totalPages > 1 && (
            <nav className="pagination" aria-label="Flow 페이지">
              <button
                type="button"
                disabled={page === 0}
                onClick={() => setPage((current) => current - 1)}
              >
                이전
              </button>

              <span>
                {page + 1} / {totalPages}
              </span>

              <button
                type="button"
                disabled={page + 1 >= totalPages}
                onClick={() => setPage((current) => current + 1)}
              >
                다음
              </button>
            </nav>
          )}
        </>
      )}
    </section>
  )
}

export default FlowFeed