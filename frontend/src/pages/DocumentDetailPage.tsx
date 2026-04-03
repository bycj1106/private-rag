import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeSanitize from 'rehype-sanitize'

import { LoadingState, StatusCard } from '../components/Feedback'
import { api } from '../services/api'
import type { DocumentDetail } from '../services/api'
import { formatTimestamp } from '../utils/format'


const markdownRemarkPlugins = [remarkGfm]
const markdownRehypePlugins = [rehypeSanitize]

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

    const controller = new AbortController()
    setLoading(true)
    setError(null)
    setDocument(null)

    const load = async () => {
      try {
        const doc = await api.getDocument(id, { signal: controller.signal })
        setDocument(doc)
      } catch (err) {
        if (controller.signal.aborted) {
          return
        }
        setError(err instanceof Error ? err.message : '获取文档失败')
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false)
        }
      }
    }

    void load()

    return () => controller.abort()
  }, [id])

  if (loading) {
    return <LoadingState />
  }

  if (error) {
    return (
      <StatusCard
        message={error}
        tone="error"
        action={<Link to="/documents" className="btn btn-secondary">返回文档列表</Link>}
      />
    )
  }

  if (!document) {
    return (
      <StatusCard
        message="文档不存在"
        action={<Link to="/documents" className="btn btn-secondary">返回文档列表</Link>}
      />
    )
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
            {document.chunk_count} 个片段 · {formatTimestamp(document.created_at)}
          </p>
        </div>

        <div className="prose prose-gray max-w-none">
          <ReactMarkdown remarkPlugins={markdownRemarkPlugins} rehypePlugins={markdownRehypePlugins}>
            {document.content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
