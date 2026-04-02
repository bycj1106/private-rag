import { describe, it, expect, vi, beforeEach } from 'vitest'
import { api, AbortError } from '../services/api'

global.fetch = vi.fn()

const mockFetch = global.fetch as ReturnType<typeof vi.fn>

describe('api service', () => {
  beforeEach(() => {
    mockFetch.mockClear()
  })

  describe('createDocument', () => {
    it('should call createDocument with correct params', async () => {
      const mockResponse = {
        id: '123',
        file_name: 'test.md',
        chunk_count: 1,
        created_at: '2024-01-01'
      }
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      })

      const result = await api.createDocument('# Test', 'test.md')

      expect(mockFetch).toHaveBeenCalledWith('/api/documents', expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_content: '# Test', file_name: 'test.md' })
      }))
      expect(result).toEqual(mockResponse)
    })

    it('should throw error on failure', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: () => Promise.resolve({ detail: 'Bad request' })
      })

      await expect(api.createDocument('', '')).rejects.toThrow('Bad request')
    })
  })

  describe('getDocuments', () => {
    it('should return documents list', async () => {
      const mockResponse = {
        documents: [{ id: '1', file_name: 'doc.md', chunk_count: 1, created_at: '2024-01-01' }],
        total: 1
      }
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      })

      const result = await api.getDocuments()

      expect(mockFetch).toHaveBeenCalledWith('/api/documents', expect.any(Object))
      expect(result).toEqual(mockResponse)
    })
  })

  describe('getDocument', () => {
    it('should return document detail', async () => {
      const mockResponse = {
        id: '123',
        file_name: 'test.md',
        content: '# Test content',
        chunk_count: 1,
        created_at: '2024-01-01'
      }
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      })

      const result = await api.getDocument('123')

      expect(mockFetch).toHaveBeenCalledWith('/api/documents/123', expect.any(Object))
      expect(result).toEqual(mockResponse)
    })

    it('should throw 404 error for non-existent document', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: () => Promise.resolve({ detail: 'Document not found' })
      })

      await expect(api.getDocument('nonexistent')).rejects.toThrow('Document not found')
    })
  })

  describe('deleteDocument', () => {
    it('should delete document successfully', async () => {
      const mockResponse = { message: 'Document deleted successfully', id: '123' }
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      })

      const result = await api.deleteDocument('123')

      expect(mockFetch).toHaveBeenCalledWith('/api/documents/123', expect.objectContaining({ method: 'DELETE' }))
      expect(result).toEqual(mockResponse)
    })
  })

  describe('query', () => {
    it('should return query response', async () => {
      const mockResponse = {
        answer: 'Test answer',
        sources: [{ content: 'source content', file_name: 'doc.md', relevance_score: 0.9 }]
      }
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      })

      const result = await api.query('What is test?')

      expect(mockFetch).toHaveBeenCalledWith('/api/query', expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ question: 'What is test?', top_k: undefined })
      }))
      expect(result).toEqual(mockResponse)
    })

    it('should pass topK parameter', async () => {
      const mockResponse = { answer: 'Answer', sources: [] }
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      })

      await api.query('Test question', 5)

      expect(mockFetch).toHaveBeenCalledWith('/api/query', expect.objectContaining({
        body: JSON.stringify({ question: 'Test question', top_k: 5 })
      }))
    })
  })

  describe('health', () => {
    it('should return health status', async () => {
      const mockResponse = { status: 'ok', timestamp: '2024-01-01T00:00:00Z' }
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      })

      const result = await api.health()

      expect(mockFetch).toHaveBeenCalledWith('/api/health', expect.any(Object))
      expect(result).toEqual(mockResponse)
    })
  })

  describe('AbortError', () => {
    it('should create AbortError with correct name', () => {
      const error = new AbortError()
      expect(error.name).toBe('AbortError')
      expect(error.message).toBe('Request aborted')
    })
  })
})
