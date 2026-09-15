import { Loader } from '@gouvfr-lasuite/cunningham-react'
import { useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { ChatMessage } from '../types'
import './MessageList.css'

type MessageListProps = {
  messages: ChatMessage[]
  isSending: boolean
}

function MessageList({ messages, isSending }: MessageListProps): React.JSX.Element {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isSending])

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
          <div className="chat-message" data-role={message.role}>
            {message.role === 'assistant' ? (
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
            ) : (
              message.content
            )}
          </div>
        </div>
      ))}
      {isSending && (
        <div className="chat-message-row" data-role="assistant">
          <div className="chat-message" data-role="assistant">
            <Loader size="small" />
          </div>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  )
}

export default MessageList
