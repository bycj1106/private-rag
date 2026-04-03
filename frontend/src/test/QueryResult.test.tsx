import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { AnswerCard, SourceList } from '../components/QueryResult'

describe('QueryResult components', () => {
  it('renders answer card', () => {
    render(<AnswerCard answer="这是回答" />)

    expect(screen.getByText('这是回答')).toBeInTheDocument()
  })

  it('renders source list items', () => {
    render(
      <SourceList
        sources={[
          { content: '来源内容', file_name: 'doc.md', relevance_score: 0.9345 },
        ]}
      />
    )

    expect(screen.getByText('参考来源')).toBeInTheDocument()
    expect(screen.getByText('doc.md')).toBeInTheDocument()
    expect(screen.getByText('相似度: 0.93')).toBeInTheDocument()
  })

  it('renders nothing for empty sources', () => {
    const { container } = render(<SourceList sources={[]} />)

    expect(container).toBeEmptyDOMElement()
  })
})
