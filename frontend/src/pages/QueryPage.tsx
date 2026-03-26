import { useState } from 'react'
import { api, AbortError } from '../services/api'
import type { SourceDocument } from '../services/api'

export default function QueryPage() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [answer, setAnswer] = useState<string | null>(null)
  const [sources, setSources] = useState<SourceDocument[]>([])
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim()) {
      setError('请输入问题')
      return
    }

    setLoading(true)
    setError(null)
    setAnswer(null)
    setSources([])

    try {
      const result = await api.query(question)
      setAnswer(result.answer)
      setSources(result.sources)
    } catch (err) {
      if (err instanceof AbortError) {
        setError('请求超时，请稍后重试')
      } else {
        setError(err instanceof Error ? err.message : '查询失败')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-900 mb-6">知识问答</h2>

      <form onSubmit={handleSubmit} className="mb-8">
        <div className="flex gap-4">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="输入你的问题..."
            className="input flex-1"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
          >
            {loading ? '查询中...' : '提问'}
          </button>
        </div>
      </form>

      {error && (
        <div className="mb-6 p-4 bg-red-50 text-red-700 border border-red-200 rounded-lg">
          {error}
        </div>
      )}

      {loading && (
        <div className="flex items-center justify-center py-12">
          <div className="text-gray-500">正在思考...</div>
        </div>
      )}

      {answer && !loading && (
        <div className="space-y-6">
          <div className="card">
            <h3 className="font-medium text-gray-900 mb-2">回答</h3>
            <p className="text-gray-700 whitespace-pre-wrap">{answer}</p>
          </div>

          {sources.length > 0 && (
            <div>
              <h3 className="font-medium text-gray-900 mb-4">参考来源</h3>
              <div className="space-y-3">
                {sources.map((source, index) => (
                  <div key={index} className="card">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-gray-800">{source.file_name}</span>
                      <span className="text-xs text-gray-400">
                        相似度: {source.relevance_score.toFixed(2)}
                      </span>
                    </div>
                    <p className="text-gray-600 text-sm">{source.content}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {!answer && !loading && !error && (
        <div className="text-center py-12 text-gray-500">
          输入问题开始问答
        </div>
      )}
    </div>
  )
}
