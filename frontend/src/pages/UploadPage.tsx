import { useState } from 'react'
import { api } from '../services/api'

export default function UploadPage() {
  const [content, setContent] = useState('')
  const [fileName, setFileName] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!content.trim() || !fileName.trim()) {
      setMessage({ type: 'error', text: '请填写文档内容和文件名' })
      return
    }

    setLoading(true)
    setMessage(null)

    try {
      const result = await api.createDocument(content, fileName)
      setMessage({
        type: 'success',
        text: `文档 "${result.file_name}" 上传成功！生成了 ${result.chunk_count} 个片段。`,
      })
      setContent('')
      setFileName('')
    } catch (err) {
      setMessage({
        type: 'error',
        text: err instanceof Error ? err.message : '上传失败',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-900 mb-6">上传文档</h2>

      {message && (
        <div
          className={`mb-6 p-4 rounded-lg ${
            message.type === 'success'
              ? 'bg-green-50 text-green-700 border border-green-200'
              : 'bg-red-50 text-red-700 border border-red-200'
          }`}
        >
          {message.text}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="fileName" className="block text-sm font-medium text-gray-700 mb-2">
            文件名 <span className="text-gray-400 text-xs">(最多 255 字符)</span>
          </label>
          <input
            type="text"
            id="fileName"
            value={fileName}
            onChange={(e) => setFileName(e.target.value)}
            placeholder="my-document.md"
            maxLength={255}
            className="input"
            disabled={loading}
          />
        </div>

        <div>
          <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
            文档内容 <span className="text-gray-400 text-xs">(最多 10MB)</span>
          </label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="在此粘贴 Markdown 文档内容..."
            rows={12}
            className="textarea"
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? '上传中...' : '上传文档'}
        </button>
      </form>
    </div>
  )
}
