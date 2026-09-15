export function formatThinkingDuration(thinkingMs: number): string {
  const seconds = Math.max(1, Math.round(thinkingMs / 1000))
  return `Thought for ${seconds} second${seconds === 1 ? '' : 's'}`
}
