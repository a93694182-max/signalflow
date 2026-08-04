import { type FormEvent, useState } from 'react'
import { Link } from 'react-router-dom'

import { searchSignalFlow } from '../api/search'
import type {
  SearchType,
  UnifiedSearchResponse,
} from '../types/search'

function SearchPage() {
  const [query, setQuery] = useState('')
  const [searchType, setSearchType] =
    useState<SearchType>('all')
  const [targetAsset, setTargetAsset] = useState('')
  const [fromDate, setFromDate] = useState('')
  const [toDate, setToDate] = useState('')
  const [result, setResult] =
    useState<UnifiedSearchResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  async function submitSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const trimmedQuery = query.trim()

    if (!trimmedQuery) {
      setError('검색어를 입력해 주세요.')
      return
    }

    if (fromDate && toDate && fromDate > toDate) {
      setError('시작 날짜는 종료 날짜보다 늦을 수 없습니다.')
      return
    }

    setIsLoading(true)
    setError('')

    try {
      const data = await searchSignalFlow({
        q: trimmedQuery,
        limit: 20,
        type: searchType,
        target_asset: targetAsset,
        from_date: fromDate,
        to_date: toDate,
      })

      setResult(data)
    } catch {
      setError('검색 결과를 불러오지 못했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="search-page">
      <div className="search-page__heading">
        <div>
          <p className="section-label">UNIFIED SEARCH</p>
          <h1>통합 검색</h1>
          <p>Flow와 Evidence를 한 번에 검색합니다.</p>
        </div>

        <Link to="/">← 홈으로</Link>
      </div>

      <form className="search-form" onSubmit={submitSearch}>
        <input
          type="search"
          value={query}
          placeholder="시장 흐름 또는 근거 검색"
          onChange={(event) => setQuery(event.target.value)}
        />

        <select
          value={searchType}
          onChange={(event) =>
            setSearchType(event.target.value as SearchType)
          }
        >
          <option value="all">전체</option>
          <option value="flow">Flow</option>
          <option value="evidence">Evidence</option>
        </select>

        <select
          value={targetAsset}
          onChange={(event) => setTargetAsset(event.target.value)}
        >
          <option value="">전체 자산</option>
          <option value="^KS11">KOSPI</option>
          <option value="^KQ11">KOSDAQ</option>
          <option value="KRW=X">원/달러</option>
          <option value="BTC-USD">비트코인</option>
          <option value="GC=F">금</option>
          <option value="CL=F">WTI</option>
          <option value="MARKET">뉴스</option>
        </select>

        <input
          type="date"
          value={fromDate}
          onChange={(event) => setFromDate(event.target.value)}
        />

        <input
          type="date"
          value={toDate}
          onChange={(event) => setToDate(event.target.value)}
        />

        <button type="submit" disabled={isLoading}>
          {isLoading ? '검색 중...' : '검색'}
        </button>
      </form>

      {error && <div className="error-state">{error}</div>}

      {!isLoading && result && (
        <div className="search-results">
          <div className="search-results__summary">
            <strong>“{result.query}” 검색 결과</strong>
            <span>
              전체 {result.total}개 · Flow {result.flow_count}개 ·
              Evidence {result.evidence_count}개
            </span>
          </div>

          {result.total === 0 && (
            <div className="empty-state">
              검색 결과가 없습니다.
            </div>
          )}

          {result.flows.length > 0 && (
            <section className="search-result-section">
              <h2>Flow</h2>

              <div className="search-result-list">
                {result.flows.map((flow) => (
                  <article
                    className="search-result-card"
                    key={flow.flow_id}
                  >
                    <div>
                      <span>{flow.target_asset}</span>
                      <time dateTime={flow.created_at}>
                        {new Date(flow.created_at).toLocaleString(
                          'ko-KR',
                        )}
                      </time>
                    </div>

                    <Link to={`/flows/${flow.flow_id}`}>
                      {flow.title}
                    </Link>

                    {flow.summary && <p>{flow.summary}</p>}
                  </article>
                ))}
              </div>
            </section>
          )}

          {result.evidences.length > 0 && (
            <section className="search-result-section">
              <h2>Evidence</h2>

              <div className="search-result-list">
                {result.evidences.map((evidence) => (
                  <article
                    className="search-result-card"
                    key={evidence.evidence_id}
                  >
                    <div>
                      <span>{evidence.source}</span>
                      <span>{evidence.target_asset}</span>
                    </div>

                    <h3>{evidence.title}</h3>

                    {evidence.content_summary && (
                      <p>{evidence.content_summary}</p>
                    )}

                    <div className="search-result-card__links">
                      <Link to={`/flows/${evidence.flow_id}`}>
                        {evidence.flow_title}
                      </Link>

                      {evidence.url && (
                        <a
                          href={evidence.url}
                          target="_blank"
                          rel="noreferrer"
                        >
                          원문 보기
                        </a>
                      )}
                    </div>
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