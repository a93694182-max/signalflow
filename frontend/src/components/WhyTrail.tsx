import { Link } from 'react-router-dom'

import type { FlowWhyTrail } from '../types/flow'

interface WhyTrailProps {
  trail: FlowWhyTrail
}

function WhyTrail({ trail }: WhyTrailProps) {
  return (
    <section className="why-trail">
      <div className="section-heading">
        <div>
          <p className="section-label">WHY TRAIL</p>
          <h2>연결된 외부 원인</h2>
        </div>

        <span>{trail.trail_count}개 연결</span>
      </div>

      {trail.trail.length === 0 ? (
        <div className="empty-state">
          연결된 외부 원인 Flow가 없습니다.
        </div>
      ) : (
        <div className="why-trail__list">
          {trail.trail.map((step) => (
            <article
              className="why-trail-card"
              key={`${step.source_flow_id}-${step.target_flow_id}`}
            >
              <div className="why-trail-card__top">
                <span>{step.relation_type}</span>
                <strong>{Math.round(step.score * 100)}점</strong>
              </div>

              <Link to={`/flows/${step.source_flow_id}`}>
                {step.source_title}
              </Link>

              <p>{step.reason}</p>

              <small>
                {step.source_title} → {step.target_title}
              </small>
            </article>
          ))}
        </div>
      )}
    </section>
  )
}

export default WhyTrail