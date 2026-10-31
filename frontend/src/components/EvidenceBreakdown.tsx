import type { EvidenceScoreBreakdown } from '../types/flow'

interface EvidenceBreakdownProps {
  evidences: EvidenceScoreBreakdown[]
}

const scoreLabels = {
  relation: '관련성',
  impact: '영향도',
  time: '시간',
  reliability: '출처 신뢰도',
} as const

const scoreKeys = [
  'relation',
  'impact',
  'time',
  'reliability',
] as const

function EvidenceBreakdown({ evidences }: EvidenceBreakdownProps) {
  return (
    <section className="evidence-breakdown">
      <div className="section-heading">
        <div>
          <p className="section-label">EVIDENCE BREAKDOWN</p>
          <h2>근거 점수 분석</h2>
        </div>
      </div>

      {evidences.length === 0 ? (
        <p className="empty-state">분석 가능한 근거가 없습니다.</p>
      ) : (
        <div className="evidence-breakdown__list">
          {evidences.map((evidence) => (
            <article
              className="evidence-breakdown__card"
              key={evidence.evidence_id}
            >
              <div className="evidence-breakdown__header">
                <h3>{evidence.title}</h3>
                <strong>{Math.round(evidence.total_score * 100)}점</strong>
              </div>

              {scoreKeys.map((key) => {
                const score = evidence.scores[key]
                const weight = evidence.weights[key]
                const contribution = evidence.weighted_scores[key]

                return (
                  <div className="score-row" key={key}>
                    <div className="score-row__label">
                      <span>{scoreLabels[key]}</span>
                      <span>
                        {Math.round(score * 100)}점 · 가중치{' '}
                        {Math.round(weight * 100)}%
                      </span>
                    </div>

                    <div
                      className="score-row__track"
                      role="progressbar"
                      aria-label={`${evidence.title} ${scoreLabels[key]}`}
                      aria-valuenow={score * 100}
                      aria-valuemin={0}
                      aria-valuemax={100}
                    >
                      <div
                        className="score-row__fill"
                        style={{ width: `${Math.max(0, Math.min(score * 100, 100))}%` }}
                      />
                    </div>

                    <p className="score-row__contribution">
                      최종 점수 기여도: {(contribution * 100).toFixed(1)}점
                    </p>
                  </div>
                )
              })}
            </article>
          ))}
        </div>
      )}
    </section>
  )
}

export default EvidenceBreakdown