import type { ReactNode } from 'react'

type MessageTone = 'success' | 'error' | 'info'

interface StatusCardProps {
  message: string
  tone?: 'neutral' | 'error'
  action?: ReactNode
}

const toneClasses = {
  neutral: 'text-gray-500',
  error: 'text-red-600',
}

export function StatusCard({ message, tone = 'neutral', action }: StatusCardProps) {
  return (
    <div className="text-center py-12">
      <p className={`${toneClasses[tone]} mb-4`}>{message}</p>
      {action}
    </div>
  )
}

interface LoadingStateProps {
  message?: string
}

export function LoadingState({ message = '加载中...' }: LoadingStateProps) {
  return (
    <div className="flex items-center justify-center py-12">
      <div className="text-gray-500">{message}</div>
    </div>
  )
}

interface MessageBannerProps {
  message: string
  tone: MessageTone
}

const messageToneClasses: Record<MessageTone, string> = {
  success: 'bg-green-50 text-green-700 border-green-200',
  error: 'bg-red-50 text-red-700 border-red-200',
  info: 'bg-blue-50 text-blue-700 border-blue-200',
}

export function MessageBanner({ message, tone }: MessageBannerProps) {
  return (
    <div className={`mb-6 rounded-lg border p-4 ${messageToneClasses[tone]}`}>
      {message}
    </div>
  )
}
