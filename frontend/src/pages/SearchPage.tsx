import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link } from 'react-router-dom'

import { searchSignalFlow } from '../api/search'
import type {
  SearchType,
  UnifiedSearchParams,
  UnifiedSearchResponse,
} from '../types/search'

const INITIAL_PARAMS: UnifiedSearchParams = {
  q: '',
  limit: 20,
  type: 'all',
  target_asset: '',
  from_date: '',
  to_date: '',
}

function formatDate(value: string | null) {
  if (!value) {
    return '날짜 정보 없음'
  }

  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(value))
}

function SearchPage() {
  const [params, setParams] =
    useState<UnifiedSearchParams>(INITIAL_PARAMS)

  const [result, setResult] =
    useState<UnifiedSearchResponse | null>(null)

  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const trimmedQuery = params.q.trim()

    if (!trimmedQuery) {
      setError('검색어를 입력해주세요.')
      setResult(null)
      return
    }

    if (
      params.from_date &&
      params.to_date &&
      params.from_date > params.to_date
    ) {
      setResult(null)
      setError('시작 날짜는 종료 날짜보다 늦을 수 없습니다.')
      return
    }

    try {
      setIsLoading(true)
      setError('')

      const data = await searchSignalFlow({
        ...params,
        q: trimmedQuery,
      })

      setResult(data)
    } catch {
      setError('검색 결과를 불러오지 못했습니다.')
      setResult(null)
    } finally {
      setIsLoading(false)
    }
  }

  function changeType(type: SearchType) {
    setParams((current) => ({
      ...current,
      type,
    }))
  }

  function resetSearch() {
    setParams({ ...INITIAL_PARAMS })
    setResult(null)
    setError('')
  }

  return (
    <section className="search-page">
      <div className="search-page__heading">
        <div>
          <p className="section-label">UNIFIED SEARCH</p>
          <h1>통합 검색</h1>
          <p>
            시장 흐름과 근거 데이터를 한 번에 검색합니다.
          </p>
        </div>

        <Link to="/">← 홈으로</Link>
      </div>

      <form
        className="search-form"
        onSubmit={handleSubmit}
      >
        <div className="search-form__main">
          <input
            aria-label="검색어"
            type="search"
            placeholder="시장 흐름, 뉴스, 경제지표 검색"
            value={params.q}
            onChange={(event) =>
              setParams((current) => ({
                ...current,
                q: event.target.value,
              }))
            }
          />

          <button
            type="submit"
            disabled={isLoading}
          >
            {isLoading ? '검색 중...' : '검색'}
          </button>
        </div>

        <div className="search-tabs">
          {(['all', 'flow', 'evidence'] as SearchType[]).map(
            (type) => (
              <button
                className={
                  params.type === type
                    ? 'search-tabs__button search-tabs__button--active'
                    : 'search-tabs__button'
                }
                key={type}
                type="button"
                onClick={() => changeType(type)}
              >
                {type === 'all' && '전체'}
                {type === 'flow' && 'Flow'}
                {type === 'evidence' && 'Evidence'}
              </button>
            ),
          )}
        </div>

        <div className="search-filters">
          <select
            aria-label="자산 선택"
            value={params.target_asset}
            onChange={(event) =>
              setParams((current) => ({
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
            value={params.from_date}
            onChange={(event) =>
              setParams((current) => ({
                ...current,
                from_date: event.target.value,
              }))
            }
          />

          <input
            aria-label="종료 날짜"
            type="date"
            value={params.to_date}
            onChange={(event) =>
              setParams((current) => ({
                ...current,
                to_date: event.target.value,
              }))
            }
          />

          <button
            className="search-form__reset"
            type="button"
            onClick={resetSearch}
          >
            초기화
          </button>
        </div>
      </form>

      {error && (
        <div className="error-state">{error}</div>
      )}

      {isLoading && (
        <div className="empty-state">
          검색 결과를 불러오는 중입니다.
        </div>
      )}

      {!isLoading && result && (
        <div className="search-results">
          <div className="search-results__summary">
            <div>
              <p className="section-label">RESULT</p>
              <h2>
                “{result.query}” 검색 결과
              </h2>
            </div>

            <span>
              전체 {result.total}건 · Flow {result.flow_count}건
              · Evidence {result.evidence_count}건
            </span>
          </div>

          {result.total === 0 && (
            <div className="empty-state">
              조건에 맞는 검색 결과가 없습니다.
            </div>
          )}

          {result.flows.length > 0 && (
            <section className="search-result-group">
              <div className="search-result-group__heading">
                <h3>Flow</h3>
                <span>{result.flow_count}건</span>
              </div>

              <div className="search-result-list">
                {result.flows.map((flow) => (
                  <article
                    className="search-result-card"
                    key={flow.flow_id}
                  >
                    <div className="search-result-card__meta">
                      <span className="asset-badge">
                        {flow.target_asset}
                      </span>

                      <time dateTime={flow.created_at}>
                        {formatDate(flow.created_at)}
                      </time>
                    </div>

                    <Link to={`/flows/${flow.flow_id}`}>
                      {flow.title}
                    </Link>

                    {flow.summary && (
                      <p>{flow.summary}</p>
                    )}
                  </article>
                ))}
              </div>
            </section>
          )}

          {result.evidences.length > 0 && (
            <section className="search-result-group">
              <div className="search-result-group__heading">
                <h3>Evidence</h3>
                <span>{result.evidence_count}건</span>
              </div>

              <div className="search-result-list">
                {result.evidences.map((evidence) => (
                  <article
                    className="search-result-card"
                    key={evidence.evidence_id}
                  >
                    <div className="search-result-card__meta">
                      <span className="asset-badge">
                        {evidence.target_asset}
                      </span>

                      <span>{evidence.source}</span>

                      <time dateTime={evidence.published_at ?? undefined}>
                        {formatDate(evidence.published_at)}
                      </time>
                    </div>

                    <h4>{evidence.title}</h4>

                    <Link
                      className="search-result-card__flow"
                      to={`/flows/${evidence.flow_id}`}
                    >
                      연결 Flow: {evidence.flow_title}
                    </Link>

                    {evidence.content_summary && (
                      <p>{evidence.content_summary}</p>
                    )}

                    {evidence.url && (
                      <a
                        className="search-result-card__source"
                        href={evidence.url}
                        target="_blank"
                        rel="noreferrer"
                      >
                        원문 보기
                      </a>
                    )}
                  </article>
                ))}
              </div>
            </section>
          )}
        </div>
      )}
    </section>
  )
}

export default SearchPage