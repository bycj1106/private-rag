import { useEffect, useRef, useState } from 'react'

import { LoadingState, MessageBanner, StatusCard } from '../components/Feedback'
import { AnswerCard, SourceList } from '../components/QueryResult'
import { api, AbortError } from '../services/api'
import type { SourceDocument } from '../services/api'

export default function QueryPage() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [answer, setAnswer] = useState<string | null>(null)
  const [sources, setSources] = useState<SourceDocument[]>([])
  const [error, setError] = useState<string | null>(null)
  const currentRequestRef = useRef<AbortController | null>(null)

  useEffect(() => {
    return () => currentRequestRef.current?.abort()
  }, [])

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
    currentRequestRef.current?.abort()
    const controller = new AbortController()
    currentRequestRef.current = controller

    try {
      const result = await api.query(question, undefined, { signal: controller.signal })
      setAnswer(result.answer)
      setSources(result.sources)
    } catch (err) {
      if (controller.signal.aborted) {
        return
      }
      if (err instanceof AbortError) {
        setError('请求超时，请稍后重试')
      } else {
        setError(err instanceof Error ? err.message : '查询失败')
      }
    } finally {
      if (currentRequestRef.current === controller) {
        currentRequestRef.current = null
        setLoading(false)
      }
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
        <MessageBanner message={error} tone="error" />
      )}

      {loading && (
        <LoadingState message="正在思考..." />
      )}

      {answer && !loading && (
        <div className="space-y-6">
          <AnswerCard answer={answer} />
          <SourceList sources={sources} />
        </div>
      )}

      {!answer && !loading && !error && (
        <StatusCard message="输入问题开始问答" />
      )}
    </div>
  )
}
