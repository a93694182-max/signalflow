import type { ConfidenceBreakdown as ConfidenceData } from '../types/flow'

interface ConfidenceBreakdownProps {
  confidence: ConfidenceData
}

function ConfidenceBreakdown({ confidence }: ConfidenceBreakdownProps) {
  const {
    quality_score,
    coverage_score,
    quality_weight,
    coverage_weight,
    evidence_count,
    raw_score,
    confidence_cap,
    confidence_score,
    confidence_level,
  } = confidence

  const levelLabels = {
    high: '높음',
    medium: '보통',
    low: '낮음',
  }

  return (
    <section className="confidence-breakdown">
      <div className="section-heading">
        <div>
          <p className="section-label">CONFIDENCE BREAKDOWN</p>
          <h2>분석 신뢰도</h2>
        </div>
      </div>

      <article className="confidence-breakdown__card">
        <div className="confidence-breakdown__header">
          <strong>{Math.round(confidence_score * 100)}점</strong>
          <span>{levelLabels[confidence_level]}</span>
        </div>

        <div className="confidence-breakdown__formula">
          <p>
            품질 점수 {quality_score.toFixed(3)} × {quality_weight}
          </p>
          <p>
            + 근거 충족도 {coverage_score.toFixed(3)} × {coverage_weight}
          </p>
          <p>= {raw_score.toFixed(3)}</p>
        </div>

        <div className="confidence-breakdown__details">
          <p>분석 근거: {evidence_count}개</p>

          {confidence_cap !== null && (
            <p>
              근거 개수에 따른 신뢰도 상한:{' '}
              {Math.round(confidence_cap * 100)}점
            </p>
          )}
        </div>

        <p className="confidence-breakdown__note">
          신뢰도는 근거 품질과 개수를 기반으로 계산한 분석 점수이며,
          실제 인과관계가 확정되었음을 의미하지 않습니다.
        </p>
      </article>
    </section>
  )
}

export default ConfidenceBreakdown