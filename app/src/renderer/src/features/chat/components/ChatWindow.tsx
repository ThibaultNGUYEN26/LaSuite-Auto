import { FormEvent, useEffect, useRef, useState } from 'react'
import { streamChatMessage } from '../api/streamChatMessage'
import type { ChatMessage, StreamEvent } from '../types'
import './ChatWindow.css'
import Composer from './Composer'
import MessageList from './MessageList'

function ChatWindow(): React.JSX.Element {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const abortControllerRef = useRef<AbortController | null>(null)

  useEffect(() => {
    return () => abortControllerRef.current?.abort()
  }, [])

  const canSubmit = input.trim().length > 0 && !isSending

  const patchMessage = (id: string, patch: Partial<ChatMessage>): void => {
    setMessages((current) => current.map((m) => (m.id === id ? { ...m, ...patch } : m)))
  }

  const handleSubmit = async (e: FormEvent): Promise<void> => {
    e.preventDefault()
    if (!canSubmit) return

    abortControllerRef.current?.abort()
    const controller = new AbortController()
    abortControllerRef.current = controller

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: input.trim(),
      createdAt: Date.now()
    }
    const assistantMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'assistant',
      content: '',
      createdAt: Date.now(),
      status: 'Thinking…',
      streaming: true
    }
    const nextMessages = [...messages, userMessage]
    setMessages([...nextMessages, assistantMessage])
    setInput('')
    setIsSending(true)

    const askedAt = Date.now()

    const onEvent = (event: StreamEvent): void => {
      switch (event.type) {
        case 'step_start':
          patchMessage(assistantMessage.id, {
            status: `Thinking (step ${event.data.step})…`
          })
          break
        case 'token':
          setMessages((current) =>
            current.map((m) =>
              m.id === assistantMessage.id
                ? { ...m, content: m.content + event.data.delta, status: undefined }
                : m
            )
          )
          break
        case 'tool_call_start':
          patchMessage(assistantMessage.id, { status: `Calling ${event.data.name}…` })
          break
        case 'tool_call_result':
        case 'step_complete':
          break
        case 'final':
          patchMessage(assistantMessage.id, {
            content: event.data.content,
            status: undefined,
            streaming: false,
            thinkingMs: Date.now() - askedAt
          })
          break
        case 'error':
          patchMessage(assistantMessage.id, {
            content: `Something went wrong: ${event.data.message}`,
            status: undefined,
            streaming: false,
            thinkingMs: Date.now() - askedAt
          })
          break
      }
    }

    try {
      await streamChatMessage(nextMessages, onEvent, controller.signal)
    } catch (error) {
      if ((error as Error).name === 'AbortError') return
      patchMessage(assistantMessage.id, {
        content: `Something went wrong reaching the backend: ${(error as Error).message}`,
        status: undefined,
        streaming: false,
        thinkingMs: Date.now() - askedAt
      })
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
