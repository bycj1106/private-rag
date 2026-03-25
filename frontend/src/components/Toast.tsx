import { useEffect } from 'react'

interface ToastProps {
  message: string
  type: 'success' | 'error' | 'info'
  onClose: () => void
  duration?: number
}

export function Toast({ message, type, onClose, duration = 3000 }: ToastProps) {
  useEffect(() => {
    const timer = setTimeout(onClose, duration)
    return () => clearTimeout(timer)
  }, [onClose, duration])

  const bgClasses = {
    success: 'bg-green-50 text-green-700 border-green-200',
    error: 'bg-red-50 text-red-700 border-red-200',
    info: 'bg-blue-50 text-blue-700 border-blue-200',
  }

  return (
    <div
      className={`fixed bottom-4 right-4 px-6 py-4 rounded-lg border shadow-lg ${bgClasses[type]} animate-slide-up`}
      role="alert"
    >
      <div className="flex items-center gap-3">
        <span>{message}</span>
        <button
          onClick={onClose}
          className="text-current opacity-50 hover:opacity-100"
          aria-label="关闭"
        >
          ×
        </button>
      </div>
    </div>
  )
}
