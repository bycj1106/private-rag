import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../services/api'
import type { Document } from '../services/api'
import { LoadingState, StatusCard } from '../components/Feedback'
import { Toast } from '../components/Toast'
import { useToast } from '../hooks/useToast'
import { formatTimestamp } from '../utils/format'

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [deletingId, setDeletingId] = useState<string | null>(null)
  const { toast, showToast, hideToast } = useToast()

  const fetchDocuments = async (signal?: AbortSignal) => {
    setLoading(true)
    setError(null)
    try {
      const result = await api.getDocuments({ signal })
      setDocuments(result.documents)
    } catch (err) {
      if (signal?.aborted) {
        return
      }
      setError(err instanceof Error ? err.message : '获取文档列表失败')
    } finally {
      if (!signal?.aborted) {
        setLoading(false)
      }
    }
  }

  useEffect(() => {
    const controller = new AbortController()
    fetchDocuments(controller.signal)
    return () => controller.abort()
  }, [])

  const handleDelete = async (id: string) => {
    setDeletingId(id)
    try {
      await api.deleteDocument(id)
      setDocuments((prev) => prev.filter((doc) => doc.id !== id))
      showToast('文档删除成功', 'success')
    } catch (err) {
      showToast(err instanceof Error ? err.message : '删除失败', 'error')
    } finally {
      setDeletingId(null)
    }
  }

  if (loading) {
    return <LoadingState />
  }

  if (error) {
    return (
      <StatusCard
        message={error}
        tone="error"
        action={
          <button onClick={() => void fetchDocuments()} className="btn btn-secondary">
            重试
          </button>
        }
      />
    )
  }

  return (
    <div>
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={hideToast}
        />
      )}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">文档列表</h2>
        <span className="text-sm text-gray-500">共 {documents.length} 个文档</span>
      </div>

      {documents.length === 0 ? (
        <StatusCard message="暂无文档，请先上传文档" />
      ) : (
        <div className="space-y-4">
          {documents.map((doc) => (
            <div key={doc.id} className="card flex items-center justify-between">
              <Link
                to={`/documents/${doc.id}`}
                className="flex-1 hover:bg-gray-50 -m-4 p-4 rounded-lg transition-colors"
              >
                <h3 className="font-medium text-gray-900">{doc.file_name}</h3>
                <p className="text-sm text-gray-500 mt-1">
                  {doc.chunk_count} 个片段 · {formatTimestamp(doc.created_at)}
                </p>
              </Link>
              <button
                onClick={() => handleDelete(doc.id)}
                disabled={deletingId === doc.id}
                className="btn btn-secondary text-red-600 hover:bg-red-50 disabled:opacity-50 ml-4"
              >
                {deletingId === doc.id ? '删除中...' : '删除'}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
