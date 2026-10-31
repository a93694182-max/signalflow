import type { CauseRankingItem } from '../types/flow'

interface CauseRankingProps {
  causes: CauseRankingItem[]
}

function CauseRanking({ causes }: CauseRankingProps) {
  return (
    <section className="cause-ranking">
      <div className="section-heading">
        <div>
          <p className="section-label">CAUSE RANKING</p>
          <h2>원인 후보 순위</h2>
        </div>
      </div>

      {causes.length === 0 ? (
        <p className="empty-state">분석된 원인 후보가 없습니다.</p>
      ) : (
        <div className="cause-ranking__list">
          {causes.map((cause) => (
            <article className="cause-ranking__card" key={cause.node_id}>
              <div className="cause-ranking__header">
                <span className="cause-ranking__rank">
                  {cause.rank}위
                </span>

                <strong>{Math.round(cause.score * 100)}점</strong>
              </div>

              <h3>{cause.title}</h3>

              <p className="cause-ranking__reason">
                {cause.reason}
              </p>

              <div className="cause-ranking__meta">
                <span>근거 {cause.evidence_count}개</span>

                {cause.rank === 1 && cause.evidence_count > 0 && (
                  <span className="cause-ranking__primary">
                    핵심 원인 후보
                  </span>
                )}
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  )
}

export default CauseRanking