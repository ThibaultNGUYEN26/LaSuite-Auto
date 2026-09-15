import { Button, Loader, TextArea } from '@gouvfr-lasuite/cunningham-react'
import { FormEvent, KeyboardEvent, useState } from 'react'
import { sendChatMessage } from '../api/sendChatMessage'
import type { ChatMessage } from '../types'

function ChatWindow(): React.JSX.Element {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)

  const canSubmit = input.trim().length > 0 && !isSending

  const handleSubmit = async (e: FormEvent): Promise<void> => {
    e.preventDefault()
    if (!canSubmit) return

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: input.trim()
    }
    const nextMessages = [...messages, userMessage]
    setMessages(nextMessages)
    setInput('')
    setIsSending(true)

    try {
      const reply = await sendChatMessage(nextMessages)
      setMessages([...nextMessages, { id: crypto.randomUUID(), role: 'assistant', content: reply }])
    } catch (error) {
      setMessages([
        ...nextMessages,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: `Something went wrong reaching the backend: ${(error as Error).message}`
        }
      ])
    } finally {
      setIsSending(false)
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>): void => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e as unknown as FormEvent)
    }
  }

  return (
    <div className="chat-wraper">
      <div className="chat">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <p className="chat-empty">Ask your La Suite companion anything to get started.</p>
        ) : (
          messages.map((message) => (
            <div key={message.id} className="chat-message" data-role={message.role}>
              {message.content}
            </div>
          ))
        )}
        {isSending && (
          <div className="chat-message" data-role="assistant">
            <Loader size="small" />
          </div>
        )}
      </div>

      <form className="chat-composer" onSubmit={handleSubmit}>
        <TextArea
          label="Message"
          hideLabel
          placeholder="Write a message…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={2}
        />
        <Button type="submit" disabled={!canSubmit}>
          Send
        </Button>
      </form>
    </div>
    </div>
  )
}

export default ChatWindow
