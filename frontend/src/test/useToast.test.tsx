import { describe, it, expect } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useToast } from '../hooks/useToast'

describe('useToast', () => {
  it('should initialize with null toast', () => {
    const { result } = renderHook(() => useToast())
    expect(result.current.toast).toBeNull()
  })

  it('should show toast with message and type', () => {
    const { result } = renderHook(() => useToast())
    
    act(() => {
      result.current.showToast('Test message', 'success')
    })
    
    expect(result.current.toast).toEqual({
      message: 'Test message',
      type: 'success'
    })
  })

  it('should hide toast', () => {
    const { result } = renderHook(() => useToast())
    
    act(() => {
      result.current.showToast('Test', 'error')
    })
    expect(result.current.toast).not.toBeNull()
    
    act(() => {
      result.current.hideToast()
    })
    expect(result.current.toast).toBeNull()
  })

  it('should default to info type', () => {
    const { result } = renderHook(() => useToast())
    
    act(() => {
      result.current.showToast('Test')
    })
    
    expect(result.current.toast?.type).toBe('info')
  })
})
