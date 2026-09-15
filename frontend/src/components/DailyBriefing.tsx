import { Link } from 'react-router-dom'

import type { DailyBriefingResponse } from '../types/briefing'

interface DailyBriefingProps {
  briefing: DailyBriefingResponse
}

function DailyBriefing({ briefing }: DailyBriefingProps) {
  return (
    <section className="daily-briefing">
      <div className="daily-briefing__header">
        <div>
          <span className="daily-briefing__label">DAILY BRIEFING</span>
          <h2>{briefing.headline}</h2>
        </div>

        <span className="daily-briefing__date">
          {briefing.date}
        </span>
      </div>

      <p className="daily-briefing__summary">
        {briefing.summary}
      </p>

      {briefing.key_causes.length > 0 && (
        <div className="daily-briefing__causes">
          <strong>Key Causes</strong>

          <ul>
            {briefing.key_causes.map((cause) => (
              <li key={cause}>{cause}</li>
            ))}
          </ul>
        </div>
      )}

      {briefing.top_flows.length > 0 && (
        <div className="daily-briefing__flows">
          <strong>Top Flows</strong>

          <div className="daily-briefing__flow-list">
            {briefing.top_flows.map((flow) => (
              <Link
                key={flow.flow_id}
                to={`/flows/${flow.flow_id}`}
                className="daily-briefing__flow"
              >
                <span>{flow.target_asset}</span>
                <p>{flow.title}</p>
                <strong>{flow.score.toFixed(3)}</strong>
              </Link>
            ))}
          </div>
        </div>
      )}
    </section>
  )
}

export default DailyBriefing