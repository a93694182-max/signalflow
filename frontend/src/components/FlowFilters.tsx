export interface FlowFilterValues {
  target_asset: string
  include_news: boolean
  query: string
  from_date: string
  to_date: string
  sort: 'latest' | 'score'
}

interface FlowFiltersProps {
  values: FlowFilterValues
  onChange: (values: FlowFilterValues) => void
  onSubmit: () => void
  onReset: () => void
}

function FlowFilters({
  values,
  onChange,
  onSubmit,
  onReset,
}: FlowFiltersProps) {
  function updateFilter<K extends keyof FlowFilterValues>(
    key: K,
    value: FlowFilterValues[K],
  ) {
    onChange({
      ...values,
      [key]: value,
    })
  }

  return (
    <form
      className="flow-filters"
      onSubmit={(event) => {
        event.preventDefault()
        onSubmit()
      }}
    >
      <input
        type="search"
        placeholder="제목 또는 내용 검색"
        value={values.query}
        onChange={(event) => updateFilter('query', event.target.value)}
      />

      <select
        value={values.target_asset}
        onChange={(event) =>
          updateFilter('target_asset', event.target.value)
        }
      >
        <option value="">전체 자산</option>
        <option value="^KS11">KOSPI</option>
        <option value="^KQ11">KOSDAQ</option>
        <option value="KRW=X">원/달러 환율</option>
        <option value="BTC-USD">비트코인</option>
        <option value="GC=F">금</option>
        <option value="CL=F">WTI 원유</option>
      </select>

      <select
        value={values.sort}
        onChange={(event) =>
          updateFilter(
            'sort',
            event.target.value as FlowFilterValues['sort'],
          )
        }
      >
        <option value="latest">최신순</option>
        <option value="score">중요도순</option>
      </select>

      <label className="flow-filters__checkbox">
        <input
          type="checkbox"
          checked={values.include_news}
          onChange={(event) =>
            updateFilter('include_news', event.target.checked)
          }
        />
        뉴스 포함
      </label>

      <input
        type="date"
        aria-label="시작 날짜"
        value={values.from_date}
        onChange={(event) =>
          updateFilter('from_date', event.target.value)
        }
      />

      <input
        type="date"
        aria-label="종료 날짜"
        value={values.to_date}
        onChange={(event) =>
          updateFilter('to_date', event.target.value)
        }
      />

      <button type="submit">적용</button>
      <button type="button" className="button-secondary" onClick={onReset}>
        초기화
      </button>
    </form>
  )
}

export default FlowFilters