interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

const sizeClasses = {
  sm: 'w-4 h-4',
  md: 'w-8 h-8',
  lg: 'w-12 h-12',
}

export function Spinner({ size = 'md', className = '' }: SpinnerProps) {
  return (
    <div
      className={`animate-spin rounded-full border-2 border-gray-200 border-t-blue-600 ${sizeClasses[size]} ${className}`}
      role="status"
      aria-label="加载中"
    >
      <span className="sr-only">加载中...</span>
    </div>
  )
}

interface LoadingProps {
  text?: string
  size?: 'sm' | 'md' | 'lg'
}

export function Loading({ text = '加载中...', size = 'md' }: LoadingProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 gap-4">
      <Spinner size={size} />
      <p className="text-gray-500 text-sm">{text}</p>
    </div>
  )
}
