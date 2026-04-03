import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { describe, expect, it, vi, beforeEach } from 'vitest'

import QueryPage from '../pages/QueryPage'
import { AbortError, api } from '../services/api'

vi.mock('../services/api', async () => {
  const actual = await vi.importActual<typeof import('../services/api')>('../services/api')
  return {
    ...actual,
    api: {
      ...actual.api,
      query: vi.fn(),
    },
  }
})

const mockedQuery = vi.mocked(api.query)

describe('QueryPage', () => {
  beforeEach(() => {
    mockedQuery.mockReset()
  })

  it('shows validation error for empty question', async () => {
    render(<QueryPage />)

    fireEvent.click(screen.getByRole('button', { name: '提问' }))

    expect(await screen.findByText('请输入问题')).toBeInTheDocument()
  })

  it('renders answer and sources after successful query', async () => {
    mockedQuery.mockResolvedValueOnce({
      answer: 'Answer text',
      sources: [{ content: 'Source content', file_name: 'doc.md', relevance_score: 0.9 }],
    })

    render(<QueryPage />)

    fireEvent.change(screen.getByPlaceholderText('输入你的问题...'), {
      target: { value: 'What is RAG?' },
    })
    fireEvent.click(screen.getByRole('button', { name: '提问' }))

    expect(await screen.findByText('Answer text')).toBeInTheDocument()
    expect(screen.getByText('doc.md')).toBeInTheDocument()
  })

  it('renders empty-result answer without source list', async () => {
    mockedQuery.mockResolvedValueOnce({
      answer: '知识库为空，请先上传文档',
      sources: [],
    })

    render(<QueryPage />)

    fireEvent.change(screen.getByPlaceholderText('输入你的问题...'), {
      target: { value: 'What is RAG?' },
    })
    fireEvent.click(screen.getByRole('button', { name: '提问' }))

    expect(await screen.findByText('知识库为空，请先上传文档')).toBeInTheDocument()
    expect(screen.queryByText('参考来源')).not.toBeInTheDocument()
  })

  it('shows timeout message when request aborts', async () => {
    mockedQuery.mockRejectedValueOnce(new AbortError())

    render(<QueryPage />)

    fireEvent.change(screen.getByPlaceholderText('输入你的问题...'), {
      target: { value: 'timeout?' },
    })
    fireEvent.click(screen.getByRole('button', { name: '提问' }))

    await waitFor(() => {
      expect(screen.getByText('请求超时，请稍后重试')).toBeInTheDocument()
    })
  })
})
