// @vitest-environment jsdom
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes, useNavigate } from 'react-router-dom'
import type { FlowTrace, FlowWhyAnalysis, FlowWhyTrail } from '../types/flow'
import { ApiError } from '../api/client'
import FlowDetailPage from './FlowDetailPage'
import { getFlowTrace, getFlowWhy, getFlowTrail } from '../api/flows'

vi.mock('../api/flows', () => ({
    getFlowTrace: vi.fn(),
    getFlowWhy: vi.fn(),
    getFlowTrail: vi.fn(),
}))

vi.mock('../components/WhyAnalysis', () => ({
    default: () => <div>Why Analysis Component</div>,
}))

vi.mock('../components/WhyTrail', () => ({
    default: () => <div>Why Trail Component</div>,
}))

vi.mock('../components/AskFlow', () => ({
    default: () => <div>Ask Flow Component</div>,
}))

vi.mock('../components/EvidenceBreakdown', () => ({
    default: () => <div>Evidence Breakdown Component</div>,
}))

vi.mock('../components/ConfidenceBreakdown', () => ({
    default: () => <div>Confidence Breakdown Component</div>,
}))

vi.mock('../components/CauseRanking', () => ({
    default: () => <div>Cause Ranking Component</div>,
}))

const traceMock = vi.mocked(getFlowTrace)
const whyMock = vi.mocked(getFlowWhy)
const trailMock = vi.mocked(getFlowTrail)

function createData(id: number) {
    const trace: FlowTrace = {
        id,
        title: `Flow ${id}`,
        target_asset: 'KOSPI',
        summary: `Flow ${id} summary`,
        nodes: [],
    }

    const why = {
        flow_id: id,
        title: trace.title,
        target_asset: 'KOSPI',
        summary: '분석 결과',
        confidence_score: 0.7,
        confidence_level: 'medium',
        primary_cause: null,
        causes: [],
        external_causes: [],
        evidence_breakdowns: [],
        confidence_breakdown: {
            quality_score: 0.7,
            coverage_score: 0.6,
            quality_weight: 0.85,
            coverage_weight: 0.15,
            evidence_count: 3,
            raw_score: 0.685,
            confidence_cap: 0.79,
            confidence_score: 0.685,
            confidence_level: 'medium',
        },
        cause_ranking: [],
    } satisfies FlowWhyAnalysis

    const trail: FlowWhyTrail = {
        flow_id: id,
        title: trace.title,
        trail_count: 0,
        trail: [],
    }

    return { trace, why, trail }
}

function deferred<T>() {
    let resolve!: (value: T) => void

    const promise = new Promise<T>((done) => {
        resolve = done
    })

    return { promise, resolve }
}

function NavigationButton() {
    const navigate = useNavigate()

    return (
        <button onClick={() => navigate('/flows/32')}>
            다음 Flow
        </button>
    )
}

function renderPage(path = '/flows/31') {
    return render(
        <MemoryRouter initialEntries={[path]}>
            <NavigationButton />
            <Routes>
                <Route path="/flows/:flowId" element={<FlowDetailPage />} />
            </Routes>
        </MemoryRouter>,
    )
}

describe('FlowDetailPage', () => {
    beforeEach(() => {
        vi.clearAllMocks()
    })

    afterEach(() => {
        cleanup()
    })

    it('API 응답 전 로딩 메시지를 표시한다', () => {
        const pending = new Promise<never>(() => {})

        traceMock.mockReturnValue(pending)
        whyMock.mockReturnValue(pending)
        trailMock.mockReturnValue(pending)

        renderPage()

        expect(
            screen.getByText('Flow 상세 데이터를 불러오는 중입니다.'),
        ).toBeTruthy()
    })

    it('정상 응답 시 Flow 상세 정보를 표시한다', async () => {
        const data = createData(31)

        traceMock.mockResolvedValue(data.trace)
        whyMock.mockResolvedValue(data.why)
        trailMock.mockResolvedValue(data.trail)

        renderPage()

        expect(
            await screen.findByRole('heading', { name: 'Flow 31' }),
        ).toBeTruthy()

        expect(
            screen.getByText('Why Analysis Component'),
        ).toBeTruthy()
    })

    it('404 응답 시 Flow 없음 메시지를 표시한다', async () => {
        traceMock.mockRejectedValue(
            new ApiError(404, 'API 요청 실패: 404'),
        )
        whyMock.mockReturnValue(new Promise<never>(() => {}))
        trailMock.mockReturnValue(new Promise<never>(() => {}))

        renderPage('/flows/999999')

        expect(
            await screen.findByText('요청한 Flow를 찾을 수 없습니다.'),
        ).toBeTruthy()
    })

    it('잘못된 Flow ID를 차단한다', () => {
        renderPage('/flows/abc')

        expect(
            screen.getByText('올바르지 않은 Flow ID입니다.'),
        ).toBeTruthy()

        expect(traceMock).not.toHaveBeenCalled()
    })

    it('이전 Flow 응답이 새 화면을 덮어쓰지 않는다', async () => {
        const oldTrace = deferred<FlowTrace>()
        const oldWhy = deferred<FlowWhyAnalysis>()
        const oldTrail = deferred<FlowWhyTrail>()

        const newData = createData(32)

        traceMock.mockImplementation((id) =>
            id === 31 ? oldTrace.promise : Promise.resolve(newData.trace),
        )
        whyMock.mockImplementation((id) =>
            id === 31 ? oldWhy.promise : Promise.resolve(newData.why),
        )
        trailMock.mockImplementation((id) =>
            id === 31 ? oldTrail.promise : Promise.resolve(newData.trail),
        )

        renderPage('/flows/31')

        screen.getByRole('button', { name: '다음 Flow' }).click()

        expect(
            await screen.findByRole('heading', { name: 'Flow 32' }),
        ).toBeTruthy()

        const oldData = createData(31)

        oldTrace.resolve(oldData.trace)
        oldWhy.resolve(oldData.why)
        oldTrail.resolve(oldData.trail)

        await waitFor(() => {
            expect(
                screen.getByRole('heading', { name: 'Flow 32' }),
            ).toBeTruthy()
            expect(
                screen.queryByRole('heading', { name: 'Flow 31' }),
            ).toBeNull()
        })
    })
})