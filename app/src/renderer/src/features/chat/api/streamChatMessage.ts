import type { ChatMessage, StreamEvent } from '../types'

const BACKEND_URL = import.meta.env.BACKEND_URL ?? 'http://127.0.0.1:8000'

export async function streamChatMessage(
  chatId: string,
  messages: ChatMessage[],
  onEvent: (event: StreamEvent) => void,
  signal: AbortSignal
): Promise<void> {
  const response = await fetch(`${BACKEND_URL}/api/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      messages: messages.map(({ role, content }) => ({ role, content }))
    }),
    signal
  })

  if (!response.ok || !response.body) {
    const error = await response.text().catch(() => '')
    throw new Error(`backend responded with ${response.status}${error ? `: ${error}` : ''}`)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  for (;;) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const frames = buffer.split('\n\n')
    buffer = frames.pop() ?? ''

    for (const frame of frames) {
      const lines = frame.split('\n')
      const eventLine = lines.find((line) => line.startsWith('event: '))
      const dataLine = lines.find((line) => line.startsWith('data: '))
      if (!eventLine || !dataLine) continue

      const type = eventLine.slice('event: '.length)
      const data = JSON.parse(dataLine.slice('data: '.length))
      onEvent({ type, data } as StreamEvent)
    }
  }
}
