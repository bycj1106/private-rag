import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { LoadingState, MessageBanner, StatusCard } from '../components/Feedback'

describe('Feedback components', () => {
  it('renders status card with action', () => {
    render(<StatusCard message="出错了" tone="error" action={<button>重试</button>} />)

    expect(screen.getByText('出错了')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: '重试' })).toBeInTheDocument()
  })

  it('renders loading state message', () => {
    render(<LoadingState message="正在加载" />)

    expect(screen.getByText('正在加载')).toBeInTheDocument()
  })

  it('renders message banner tone styles', () => {
    render(<MessageBanner message="成功" tone="success" />)

    expect(screen.getByText('成功')).toBeInTheDocument()
  })
})
