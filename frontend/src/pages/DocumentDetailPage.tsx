import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { api } from '../services/api'
import type { DocumentDetail } from '../services/api'

export default function DocumentDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [document, setDocument] = useState<DocumentDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) {
      setError('文档 ID 不存在')
      setLoading(false)
      return
    }

    const fetchDocument = async () => {
      setLoading(true)
      setError(null)
      try {
        const doc = await api.getDocument(id)
        setDocument(doc)
      } catch (err) {
        setError(err instanceof Error ? err.message : '获取文档失败')
      } finally {
        setLoading(false)
      }
    }

    fetchDocument()
  }, [id])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-gray-500">加载中...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600 mb-4">{error}</p>
        <Link to="/documents" className="btn btn-secondary">
          返回文档列表
        </Link>
      </div>
    )
  }

  if (!document) {
    return null
  }

  return (
    <div>
      <div className="mb-6">
        <Link
          to="/documents"
          className="text-blue-600 hover:text-blue-700 text-sm flex items-center gap-1"
        >
          ← 返回文档列表
        </Link>
      </div>

      <div className="card">
        <div className="mb-6 pb-4 border-b border-gray-200">
          <h1 className="text-2xl font-semibold text-gray-900 mb-2">
            {document.file_name}
          </h1>
          <p className="text-sm text-gray-500">
            {document.chunk_count} 个片段 · {new Date(document.created_at).toLocaleString()}
          </p>
        </div>

        <div className="prose prose-gray max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {document.content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
