const API_BASE = '/api'
const DEFAULT_TIMEOUT_MS = 60000
const DEFAULT_TOP_K = 5

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
  top_k: number
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

class AbortError extends Error {
  constructor() {
    super('Request aborted')
    this.name = 'AbortError'
  }
}

interface RequestOptions extends Omit<RequestInit, 'signal'> {
  signal?: AbortSignal
}

function withJsonBody(body: unknown, options?: RequestOptions): RequestOptions {
  return {
    ...options,
    body: JSON.stringify(body),
  }
}

function composeSignals(signal?: AbortSignal): AbortController {
  const controller = new AbortController()

  if (!signal) {
    return controller
  }

  if (signal.aborted) {
    controller.abort(signal.reason)
    return controller
  }

  signal.addEventListener('abort', () => controller.abort(signal.reason), { once: true })
  return controller
}

async function readErrorMessage(response: Response): Promise<string> {
  const fallbackMessage = `HTTP ${response.status}`
  const error = await response.json().catch(() => ({ detail: 'Request failed' }))
  if (typeof error?.detail === 'string' && error.detail.trim()) {
    return error.detail
  }
  return fallbackMessage
}

async function fetchApi<T>(
  endpoint: string,
  options?: RequestOptions,
  timeoutMs: number = DEFAULT_TIMEOUT_MS
): Promise<T> {
  const controller = composeSignals(options?.signal)
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs)
  const headers = {
    'Content-Type': 'application/json',
    ...options?.headers,
  }

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
      signal: controller.signal,
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      throw new Error(await readErrorMessage(response))
    }

    return response.json()
  } catch (error) {
    clearTimeout(timeoutId)
    if (
      typeof error === 'object' &&
      error !== null &&
      'name' in error &&
      error.name === 'AbortError'
    ) {
      throw new AbortError()
    }
    throw error
  }
}

export const api = {
  createDocument: (fileContent: string, fileName: string, options?: RequestOptions) =>
    fetchApi<Document>('/documents', withJsonBody({ file_content: fileContent, file_name: fileName }, {
      ...options,
      method: 'POST',
    })),

  getDocuments: (options?: RequestOptions) =>
    fetchApi<{ documents: Document[]; total: number }>('/documents', {
      ...options,
      method: 'GET',
    }),

  getDocument: (id: string, options?: RequestOptions) =>
    fetchApi<DocumentDetail>(`/documents/${id}`, {
      ...options,
      method: 'GET',
    }),

  deleteDocument: (id: string, options?: RequestOptions) =>
    fetchApi<{ message: string; id: string }>(`/documents/${id}`, {
      ...options,
      method: 'DELETE',
    }),

  query: (question: string, topK: number = DEFAULT_TOP_K, options?: RequestOptions) =>
    fetchApi<QueryResponse>('/query', withJsonBody({ question, top_k: topK } as QueryRequest, {
      ...options,
      method: 'POST',
    })),

  health: (options?: RequestOptions) =>
    fetchApi<{ status: string; timestamp: string }>('/health', options),
}

export type { Document, DocumentDetail, QueryResponse, SourceDocument }
export { AbortError }
