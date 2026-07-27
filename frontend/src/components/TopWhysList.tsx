import type { TopWhy } from '../types/home'

interface TopWhysListProps {
  flows: TopWhy[]
}

function TopWhysList({ flows }: TopWhysListProps) {
  return (
    <section className="top-whys">
      <div className="section-heading">
        <div>
          <p className="section-label">TOP FLOWS</p>
          <h2>주요 시장 흐름</h2>
        </div>

        <span>{flows.length}개</span>
      </div>

      {flows.length === 0 ? (
        <div className="empty-state">
          추가로 감지된 주요 시장 흐름이 없습니다.
        </div>
      ) : (
        <div className="top-whys__list">
          {flows.map((flow, index) => (
            <article className="top-why-card" key={flow.flow_id}>
              <span className="top-why-card__rank">{index + 2}</span>

              <div className="top-why-card__content">
                <div className="top-why-card__meta">
                  <span>{flow.target_asset}</span>
                  <span>중요도 {Math.round(flow.score * 100)}점</span>
                </div>

                <h3>{flow.title}</h3>

                <time dateTime={flow.created_at}>
                  {new Intl.DateTimeFormat('ko-KR', {
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                  }).format(new Date(flow.created_at))}
                </time>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  )
}

export default TopWhysList