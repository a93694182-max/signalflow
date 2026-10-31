import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.stubEnv('VITE_API_BASE_URL', 'http://localhost:8000')

import { ApiError, apiGet, apiPost } from './client'

const fetchMock = vi.fn<typeof fetch>()

describe('API Client', () => {
    beforeEach(() => {
        fetchMock.mockReset()
        vi.stubGlobal('fetch', fetchMock)
    })

    it('GET 요청 성공 시 JSON 데이터를 반환한다', async () => {
        const data = { id: 1, title: 'Test Flow' }

        fetchMock.mockResolvedValue(
            new Response(JSON.stringify(data), {
                status: 200,
                headers: {
                    'Content-Type': 'application/json',
                },
            }),
        )

        const result = await apiGet<typeof data>('/api/flows/1')

        expect(result).toEqual(data)
        expect(fetchMock).toHaveBeenCalledWith(
            'http://localhost:8000/api/flows/1',
        )
    })

    it('POST 요청 시 JSON 본문을 전달한다', async () => {
        const body = { question: '시장 상승 원인은?' }
        const data = { answer: '분석 결과' }

        fetchMock.mockResolvedValue(
            new Response(JSON.stringify(data), {
                status: 200,
            }),
        )

        const result = await apiPost<typeof data>('/api/ask', body)

        expect(result).toEqual(data)
        expect(fetchMock).toHaveBeenCalledWith(
            'http://localhost:8000/api/ask',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body),
            },
        )
    })

    it('404 응답 시 ApiError를 발생시킨다', async () => {
        fetchMock.mockResolvedValue(
            new Response(null, { status: 404 }),
        )

        await expect(
            apiGet('/api/flows/999999'),
        ).rejects.toMatchObject({
            name: 'ApiError',
            status: 404,
        })
    })

    it('500 응답 시 ApiError를 발생시킨다', async () => {
        fetchMock.mockResolvedValue(
            new Response(null, { status: 500 }),
        )

        await expect(
            apiGet('/api/flows/1'),
        ).rejects.toBeInstanceOf(ApiError)

        await expect(
            apiGet('/api/flows/1'),
        ).rejects.toMatchObject({
            status: 500,
        })
    })

    it('네트워크 오류를 호출자에게 전달한다', async () => {
        fetchMock.mockRejectedValue(
            new TypeError('Failed to fetch'),
        )

        await expect(
            apiGet('/api/flows/1'),
        ).rejects.toThrow('Failed to fetch')
    })
})