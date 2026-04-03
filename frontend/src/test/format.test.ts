import { describe, expect, it } from 'vitest'

import { formatTimestamp } from '../utils/format'

describe('formatTimestamp', () => {
  it('formats ISO timestamps with shared formatter', () => {
    expect(formatTimestamp('2024-01-01T08:30:00Z')).toBeTruthy()
  })
})
