import { FormEvent, useState } from 'react'
import { sendChatMessage } from '../api/sendChatMessage'
import type { ChatMessage } from '../types'
import './ChatWindow.css'
import Composer from './Composer'
import MessageList from './MessageList'

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

  return (
    <div className="chat-wrapper">
      <div className="chat">
        <MessageList messages={messages} isSending={isSending} />
        <Composer value={input} onChange={setInput} onSubmit={handleSubmit} canSubmit={canSubmit} />
      </div>
    </div>
  )
}

export default ChatWindow
