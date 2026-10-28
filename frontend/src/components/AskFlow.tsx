import { type FormEvent, useState } from 'react'

import { askFlow } from '../api/ask'
import type { AskResponse } from '../types/ask'

interface AskFlowProps {
  flowId: number
}

function AskFlow({ flowId }: AskFlowProps) {
  const [question, setQuestion] = useState('')
  const [response, setResponse] =
    useState<AskResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  async function submitQuestion(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    const trimmedQuestion = question.trim()

    if (!trimmedQuestion) {
      setError('질문을 입력해 주세요.')
      return
    }

    setIsLoading(true)
    setError('')

    try {
      const data = await askFlow({
        flow_id: flowId,
        question: trimmedQuestion,
      })

      setResponse(data)
    } catch {
      setError('답변을 생성하지 못했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="ask-flow">
      <div className="section-heading">
        <div>
          <p className="section-label">ASK SIGNALFLOW</p>
          <h2>이 흐름에 대해 질문하기</h2>
        </div>
      </div>

      <form className="ask-flow__form" onSubmit={submitQuestion}>
        <textarea
          value={question}
          maxLength={500}
          placeholder="예: 이 시장 흐름이 발생한 가장 중요한 원인은 무엇인가요?"
          onChange={(event) => setQuestion(event.target.value)}
        />

        <div>
          <span>{question.length} / 500</span>

          <button type="submit" disabled={isLoading}>
            {isLoading ? '분석 중...' : '질문하기'}
          </button>
        </div>
      </form>

      {error && <div className="error-state">{error}</div>}

      {response && (
        <article className="ask-flow__answer">
          <div className="ask-flow__answer-meta">
            <span
              className={`ask-flow__source ${response.answer_source === 'openai'
                  ? 'ask-flow__source--ai'
                  : 'ask-flow__source--template'
                }`}
            >
              {response.answer_source === 'openai'
                ? 'AI 분석'
                : '기본 분석'}
            </span>

            <strong>
              분석 신뢰도 {Math.round(response.confidence_score * 100)}점
            </strong>

            <span>{response.confidence_level}</span>
          </div>

          <h3>{response.question}</h3>
          <p>{response.answer}</p>

          {response.primary_cause && (
            <div className="ask-flow__cause">
              <strong>핵심 원인</strong>
              <span>{response.primary_cause}</span>
            </div>
          )}

          {response.flow_path.length > 0 && (
            <div className="ask-flow__path">
              <strong>Flow Path</strong>
              <p>{response.flow_path.join(' → ')}</p>
            </div>
          )}

          {response.why_trail.length > 0 && (
            <div className="ask-flow__path">
              <strong>Why Trail</strong>

              <ul>
                {response.why_trail.map((trail) => (
                  <li key={trail}>{trail}</li>
                ))}
              </ul>
            </div>
          )}

          <small>활용된 근거 {response.evidence_count}개</small>
        </article>
      )}
    </section>
  )
}

export default AskFlow