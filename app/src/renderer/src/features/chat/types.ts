export type ChatMessage = {
  id: string
  role: 'user' | 'assistant'
  content: string
  createdAt: number
  /** How long the assistant took to reply, in milliseconds. Only set for assistant messages. */
  thinkingMs?: number
}
