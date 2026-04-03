const dateTimeFormatter = new Intl.DateTimeFormat('zh-CN', {
  dateStyle: 'medium',
  timeStyle: 'short',
})

export function formatTimestamp(value: string): string {
  return dateTimeFormatter.format(new Date(value))
}
