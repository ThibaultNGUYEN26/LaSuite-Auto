const MINUTE = 60 * 1000
const HOUR = 60 * MINUTE
const DAY = 24 * HOUR

export function formatRelativeTime(createdAt: number, now: number = Date.now()): string {
  const diff = Math.max(0, now - createdAt)

  if (diff < 10 * 1000) return 'Just now'
  if (diff < MINUTE) {
    const seconds = Math.floor(diff / 1000)
    return `${seconds} second${seconds === 1 ? '' : 's'} ago`
  }
  if (diff < HOUR) {
    const minutes = Math.floor(diff / MINUTE)
    return `${minutes} minute${minutes === 1 ? '' : 's'} ago`
  }
  if (diff < DAY) {
    const hours = Math.floor(diff / HOUR)
    return `${hours} hour${hours === 1 ? '' : 's'} ago`
  }
  if (diff < 7 * DAY) {
    const days = Math.floor(diff / DAY)
    return days === 1 ? 'Yesterday' : `${days} days ago`
  }

  return new Date(createdAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
}
