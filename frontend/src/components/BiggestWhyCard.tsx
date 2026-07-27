import type { BiggestWhy } from '../types/home'

interface BiggestWhyCardProps {
  flow: BiggestWhy
}

function BiggestWhyCard({ flow }: BiggestWhyCardProps) {
  const createdAt = new Intl.DateTimeFormat('ko-KR', {
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(flow.created_at))

  return (
    <section className="biggest-why">
      <div className="biggest-why__top">
        <div>
          <p className="section-label">BIGGEST WHY</p>
          <h2>오늘의 가장 중요한 흐름</h2>
        </div>

        <span className="asset-badge">{flow.target_asset}</span>
      </div>

      <h3 className="biggest-why__title">{flow.title}</h3>
      <p className="biggest-why__summary">{flow.summary}</p>

      <div className="biggest-why__metrics">
        <span>중요도 {Math.round(flow.score * 100)}점</span>
        <span>신뢰도 {Math.round(flow.confidence_score * 100)}%</span>
        <span>외부 원인 {flow.external_cause_count}개</span>
        <span>{createdAt}</span>
      </div>
    </section>
  )
}

export default BiggestWhyCard