import { Loader } from '@gouvfr-lasuite/cunningham-react'
import { useEffect, useRef, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { ChatMessage } from '../types'
import { formatRelativeTime } from '../utils/formatRelativeTime'
import { formatThinkingDuration } from '../utils/formatThinkingDuration'
import './MessageList.css'

type MessageListProps = {
  messages: ChatMessage[]
  isSending: boolean
}

function MessageList({ messages, isSending }: MessageListProps): React.JSX.Element {
  const bottomRef = useRef<HTMLDivElement>(null)
  const [now, setNow] = useState(() => Date.now())

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isSending])

  useEffect(() => {
    const interval = setInterval(() => setNow(Date.now()), 30 * 1000)
    return () => clearInterval(interval)
  }, [])

  if (messages.length === 0 && !isSending) {
    return (
      <div className="chat-messages">
        <div className="chat-empty-state">
          <h2>What is on your mind?</h2>
          <p>Ask your La Suite companion anything to get started.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="chat-messages">
      {messages.map((message) => (
        <div key={message.id} className="chat-message-row" data-role={message.role}>
          <div className="chat-message-group">
            <span className="chat-message-time">
              {message.role === 'assistant' && message.thinkingMs !== undefined
                ? formatThinkingDuration(message.thinkingMs)
                : formatRelativeTime(message.createdAt, now)}
            </span>
            <div className="chat-message" data-role={message.role}>
              {message.role === 'assistant' && message.status ? (
                <span className="chat-message-status">
                  <Loader size="small" />
                  {message.status}
                </span>
              ) : message.role === 'assistant' ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
              ) : (
                message.content
              )}
            </div>
          </div>
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  )
}

export default MessageList
