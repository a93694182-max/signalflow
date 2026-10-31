import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ApiError } from '../api/client'

import {
    getFlowTrace,
    getFlowTrail,
    getFlowWhy,
} from '../api/flows'
import WhyAnalysis from '../components/WhyAnalysis'
import WhyTrail from '../components/WhyTrail'
import AskFlow from '../components/AskFlow'
import EvidenceBreakdown from '../components/EvidenceBreakdown'
import ConfidenceBreakdown from '../components/ConfidenceBreakdown'
import CauseRanking from '../components/CauseRanking'
import type {
    FlowTrace,
    FlowWhyAnalysis,
    FlowWhyTrail,
} from '../types/flow'

type FlowDetailState =
    | { status: 'loading'; flowId: number }
    | {
          status: 'success'
          flowId: number
          flow: FlowTrace
          whyAnalysis: FlowWhyAnalysis
          whyTrail: FlowWhyTrail
      }
    | {
          status: 'error'
          flowId: number
          message: string
      }

function FlowDetailPage() {
    const { flowId } = useParams()
    const [detailState, setDetailState] = useState<FlowDetailState>({
        status: 'loading',
        flowId: -1,
    })

    const id = Number(flowId)
    const isInvalidFlowId = !Number.isInteger(id) || id <= 0

    useEffect(() => {
        if (isInvalidFlowId) {
            return
        }

        let isActive = true

        Promise.all([
            getFlowTrace(id),
            getFlowWhy(id),
            getFlowTrail(id),
        ])
            .then(([traceData, whyData, trailData]) => {
                if (!isActive) return

                setDetailState({
                    status: 'success',
                    flowId: id,
                    flow: traceData,
                    whyAnalysis: whyData,
                    whyTrail: trailData,
                })
            })
            .catch((error: unknown) => {
                if (!isActive) return

                let message: string

                if (error instanceof ApiError) {
                    if (error.status === 404) {
                        message = '요청한 Flow를 찾을 수 없습니다.'
                    } else if (error.status >= 500) {
                        message = '서버 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.'
                    } else {
                        message = `Flow 데이터를 불러오지 못했습니다. (${error.status})`
                    }
                } else {
                    message = '서버에 연결할 수 없습니다. 네트워크 상태를 확인해 주세요.'
                }

                setDetailState({
                    status: 'error',
                    flowId: id,
                    message,
                })
            })

        return () => {
            isActive = false
        }
    }, [id, isInvalidFlowId])

    if (isInvalidFlowId) {
        return (
            <section>
                <Link to="/">← 홈으로</Link>
                <p>올바르지 않은 Flow ID입니다.</p>
            </section>
        )
    }

    if (detailState.flowId !== id || detailState.status === 'loading') {
        return <p>Flow 상세 데이터를 불러오는 중입니다.</p>
    }

    if (detailState.status === 'error') {
        return (
            <section>
                <Link to="/">← 홈으로</Link>
                <p>{detailState.message}</p>
            </section>
        )
    }

    const {
        flow,
        whyAnalysis,
        whyTrail,
    } = detailState

    return (
        <section className="flow-detail">
            <Link to="/" className="flow-detail__back">
                ← 홈으로
            </Link>

            <header className="flow-detail__header">
                <span className="flow-detail__asset">
                    {flow.target_asset}
                </span>

                <h1>{flow.title}</h1>
                <p>{flow.summary}</p>
            </header>

            <WhyAnalysis analysis={whyAnalysis} />

            {whyAnalysis && (
              <EvidenceBreakdown evidences={whyAnalysis.evidence_breakdowns} />
            )}

            {whyAnalysis && (
              <ConfidenceBreakdown confidence={whyAnalysis.confidence_breakdown} />
            )}

            {whyAnalysis && (
              <CauseRanking causes={whyAnalysis.cause_ranking} />
            )}

            {whyTrail && <WhyTrail trail={whyTrail} />}

            <AskFlow flowId={flow.id} />
            
            <div className="flow-detail__timeline">
                <h2>Flow Timeline</h2>

                {flow.nodes.length === 0 ? (
                    <p>등록된 타임라인이 없습니다.</p>
                ) : (
                    flow.nodes.map((node) => (
                        <article className="flow-node" key={node.id}>
                            <div className="flow-node__order">
                                {node.order_index}
                            </div>

                            <div className="flow-node__content">
                                <div className="flow-node__meta">
                                    <span>{node.category}</span>
                                    <span>{node.evidence_level}</span>

                                    <time dateTime={node.occurred_at}>
                                        {new Date(node.occurred_at).toLocaleString(
                                            'ko-KR',
                                        )}
                                    </time>
                                </div>

                                <h3>{node.title}</h3>
                                <p>{node.description}</p>

                                {node.evidences.length > 0 && (
                                    <div className="flow-node__evidences">
                                        <h4>Evidence</h4>

                                        {node.evidences.map((evidence) => (
                                            <div
                                                className="evidence-card"
                                                key={evidence.id}
                                            >
                                                <strong>{evidence.title}</strong>
                                                <p>{evidence.content_summary}</p>
                                                <span>{evidence.source}</span>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </article>
                    ))
                )}
            </div>
        </section>
    )
}

export default FlowDetailPage