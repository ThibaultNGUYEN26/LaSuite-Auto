import type { ChatMessage } from '../types'

const BACKEND_URL = import.meta.env.BACKEND_URL ?? 'http://127.0.0.1:8000'

export async function sendChatMessage(messages: ChatMessage[]): Promise<string> {
  const response = await fetch(`${BACKEND_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages: messages.map(({ role, content }) => ({ role, content })) })
  })

  if (!response.ok) {
    const error = await response.text()
    throw new Error(`backend responded with ${response.status}${error ? `: ${error}` : ''}`)
  }

  const data = (await response.json()) as { reply: string }
  return data.reply
}
