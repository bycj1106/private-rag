import type { SourceDocument } from '../services/api'

interface AnswerCardProps {
  answer: string
}

export function AnswerCard({ answer }: AnswerCardProps) {
  return (
    <div className="card">
      <h3 className="mb-2 font-medium text-gray-900">回答</h3>
      <p className="whitespace-pre-wrap text-gray-700">{answer}</p>
    </div>
  )
}

interface SourceListProps {
  sources: SourceDocument[]
}

function getSourceKey(source: SourceDocument): string {
  return `${source.file_name}:${source.content.slice(0, 48)}:${source.relevance_score.toFixed(4)}`
}

export function SourceList({ sources }: SourceListProps) {
  if (sources.length === 0) {
    return null
  }

  return (
    <div>
      <h3 className="mb-4 font-medium text-gray-900">参考来源</h3>
      <div className="space-y-3">
        {sources.map((source) => (
          <div key={getSourceKey(source)} className="card">
            <div className="mb-2 flex items-center justify-between">
              <span className="font-medium text-gray-800">{source.file_name}</span>
              <span className="text-xs text-gray-400">相似度: {source.relevance_score.toFixed(2)}</span>
            </div>
            <p className="text-sm text-gray-600">{source.content}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
