import { useState, useEffect } from 'react'
import { api } from '../services/api'
import type { Document } from '../services/api'

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [deletingId, setDeletingId] = useState<string | null>(null)

  const fetchDocuments = async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await api.getDocuments()
      setDocuments(result.documents)
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取文档列表失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDocuments()
  }, [])

  const handleDelete = async (id: string) => {
    setDeletingId(id)
    try {
      await api.deleteDocument(id)
      setDocuments((prev) => prev.filter((doc) => doc.id !== id))
    } catch (err) {
      alert(err instanceof Error ? err.message : '删除失败')
    } finally {
      setDeletingId(null)
    }
  }

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
        <button onClick={fetchDocuments} className="btn btn-secondary">
          重试
        </button>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">文档列表</h2>
        <span className="text-sm text-gray-500">共 {documents.length} 个文档</span>
      </div>

      {documents.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          暂无文档，请先上传文档
        </div>
      ) : (
        <div className="space-y-4">
          {documents.map((doc) => (
            <div key={doc.id} className="card flex items-center justify-between">
              <div>
                <h3 className="font-medium text-gray-900">{doc.file_name}</h3>
                <p className="text-sm text-gray-500 mt-1">
                  {doc.chunk_count} 个片段 · {new Date(doc.created_at).toLocaleString()}
                </p>
              </div>
              <button
                onClick={() => handleDelete(doc.id)}
                disabled={deletingId === doc.id}
                className="btn btn-secondary text-red-600 hover:bg-red-50 disabled:opacity-50"
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
