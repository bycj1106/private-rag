const API_BASE = '/api'

interface Document {
  id: string
  file_name: string
  chunk_count: number
  created_at: string
}

interface DocumentDetail extends Document {
  content: string
}

interface QueryRequest {
  question: string
  top_k?: number
}

interface SourceDocument {
  content: string
  file_name: string
  relevance_score: number
}

interface QueryResponse {
  answer: string
  sources: SourceDocument[]
}

async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(error.detail || `HTTP ${response.status}`)
  }

  return response.json()
}

export const api = {
  createDocument: (fileContent: string, fileName: string) =>
    fetchApi<Document>('/documents', {
      method: 'POST',
      body: JSON.stringify({ file_content: fileContent, file_name: fileName }),
    }),

  getDocuments: () =>
    fetchApi<{ documents: Document[]; total: number }>('/documents', {
      method: 'GET',
    }),

  getDocument: (id: string) =>
    fetchApi<DocumentDetail>(`/documents/${id}`, {
      method: 'GET',
    }),

  deleteDocument: (id: string) =>
    fetchApi<{ message: string; id: string }>(`/documents/${id}`, {
      method: 'DELETE',
    }),

  query: (question: string, topK?: number) =>
    fetchApi<QueryResponse>('/query', {
      method: 'POST',
      body: JSON.stringify({ question, top_k: topK } as QueryRequest),
    }),

  health: () => fetchApi<{ status: string; timestamp: string }>('/health'),
}

export type { Document, DocumentDetail, QueryResponse, SourceDocument }
