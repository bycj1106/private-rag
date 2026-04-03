import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { describe, expect, it, vi, beforeEach } from 'vitest'

import UploadPage from '../pages/UploadPage'
import { api } from '../services/api'

vi.mock('../services/api', async () => {
  const actual = await vi.importActual<typeof import('../services/api')>('../services/api')
  return {
    ...actual,
    api: {
      ...actual.api,
      createDocument: vi.fn(),
    },
  }
})

const mockedCreateDocument = vi.mocked(api.createDocument)

describe('UploadPage', () => {
  beforeEach(() => {
    mockedCreateDocument.mockReset()
  })

  it('shows validation message for empty form', async () => {
    render(<UploadPage />)

    fireEvent.click(screen.getByRole('button', { name: '上传文档' }))

    expect(await screen.findByText('请填写文档内容和文件名')).toBeInTheDocument()
  })

  it('shows success message and resets form after upload', async () => {
    mockedCreateDocument.mockResolvedValueOnce({
      id: '1',
      file_name: 'test.md',
      chunk_count: 2,
      created_at: '2024-01-01T00:00:00Z',
    })

    render(<UploadPage />)

    fireEvent.change(screen.getByLabelText(/文件名/), { target: { value: 'test.md' } })
    fireEvent.change(screen.getByLabelText(/文档内容/), { target: { value: '# Hello' } })
    fireEvent.click(screen.getByRole('button', { name: '上传文档' }))

    expect(await screen.findByText('文档 "test.md" 上传成功！生成了 2 个片段。')).toBeInTheDocument()
    await waitFor(() => {
      expect(screen.getByLabelText(/文件名/)).toHaveValue('')
      expect(screen.getByLabelText(/文档内容/)).toHaveValue('')
    })
  })

  it('shows error message when upload fails', async () => {
    mockedCreateDocument.mockRejectedValueOnce(new Error('上传失败了'))

    render(<UploadPage />)

    fireEvent.change(screen.getByLabelText(/文件名/), { target: { value: 'test.md' } })
    fireEvent.change(screen.getByLabelText(/文档内容/), { target: { value: '# Hello' } })
    fireEvent.click(screen.getByRole('button', { name: '上传文档' }))

    expect(await screen.findByText('上传失败了')).toBeInTheDocument()
  })
})
