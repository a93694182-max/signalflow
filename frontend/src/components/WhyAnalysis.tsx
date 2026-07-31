import type { FlowWhyAnalysis } from '../types/flow'

interface WhyAnalysisProps {
  analysis: FlowWhyAnalysis
}

function WhyAnalysis({ analysis }: WhyAnalysisProps) {
  const secondaryCauses = analysis.causes.filter(
    (cause) => cause.node_id !== analysis.primary_cause?.node_id,
  )

  return (
    <section className="why-analysis">
      <div className="section-heading">
        <div>
          <p className="section-label">WHY ANALYSIS</p>
          <h2>왜 발생했을까?</h2>
        </div>
      </div>

      {analysis.primary_cause ? (
        <article className="primary-cause">
          <div className="primary-cause__top">
            <span>핵심 원인</span>
            <strong>
              {Math.round(analysis.primary_cause.score * 100)}점
            </strong>
          </div>

          <h3>{analysis.primary_cause.title}</h3>
          <p>{analysis.primary_cause.description}</p>

          <div className="primary-cause__meta">
            <span>{analysis.primary_cause.category}</span>
            <span>
              근거 {analysis.primary_cause.evidence_count}개
            </span>
          </div>
        </article>
      ) : (
        <p className="empty-state">분석된 핵심 원인이 없습니다.</p>
      )}

      {secondaryCauses.length > 0 && (
        <div className="cause-list">
          <h3>추가 원인</h3>

          {secondaryCauses.map((cause) => (
            <article className="cause-card" key={cause.node_id}>
              <div>
                <span>{cause.category}</span>
                <strong>{cause.title}</strong>
                <p>{cause.description}</p>
              </div>

              <b>{Math.round(cause.score * 100)}점</b>
            </article>
          ))}
        </div>
      )}
    </section>
  )
}

export default WhyAnalysis