import { Loader } from '@gouvfr-lasuite/cunningham-react'
import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { appIconMarkup } from '../../../assets/appIcon'
import type { ChatMessage, TraceEntry } from '../types'
import { formatRelativeTime } from '../utils/formatRelativeTime'
import { formatThinkingDuration } from '../utils/formatThinkingDuration'
import './MessageList.css'

type MessageListProps = {
  messages: ChatMessage[]
  isSending: boolean
}

function formatTraceValue(value: unknown): string {
  return typeof value === 'string' ? value : JSON.stringify(value, null, 2)
}

function TraceValue({
  value,
  kind
}: {
  value: unknown
  kind?: 'result'
}): React.JSX.Element {
  const preRef = useRef<HTMLPreElement>(null)
  const [expanded, setExpanded] = useState(false)
  const [isClamped, setIsClamped] = useState(false)
  const text = formatTraceValue(value)

  useLayoutEffect(() => {
    const el = preRef.current
    if (!el) return
    setIsClamped(el.scrollHeight > el.clientHeight + 1)
  }, [text])

  return (
    <div className="chat-trace-value">
      <pre
        ref={preRef}
        className="chat-trace-entry__value"
        data-kind={kind}
        data-expanded={expanded}
      >
        {text}
      </pre>
      {isClamped || expanded ? (
        <button
          type="button"
          className="chat-trace-value__toggle"
          onClick={() => setExpanded((current) => !current)}
        >
          {expanded ? 'Show less' : 'Show more'}
        </button>
      ) : null}
    </div>
  )
}

function ChatTrace({ trace }: { trace: TraceEntry[] }): React.JSX.Element {
  return (
    <ol className="chat-trace-list">
      {trace.map((entry, index) =>
        entry.type === 'step' ? (
          <li key={`step-${entry.step}-${index}`} className="chat-trace-entry" data-kind="step">
            Step {entry.step}
          </li>
        ) : (
          <li key={entry.toolCallId} className="chat-trace-entry" data-kind="tool-call">
            <div className="chat-trace-entry__name">{entry.name}</div>
            <TraceValue value={entry.arguments} />
            {entry.result !== undefined ? <TraceValue value={entry.result} kind="result" /> : null}
          </li>
        )
      )}
    </ol>
  )
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

  const visibleMessages = messages.filter((message) => !message.hidden)

  if (visibleMessages.length === 0 && !isSending) {
    return (
      <div className="chat-messages">
        <div className="chat-empty-state">
          <div
            className="chat-empty-state__icon"
            dangerouslySetInnerHTML={{ __html: appIconMarkup }}
            aria-hidden="true"
          />
          <h2>What is on your mind?</h2>
          <p>Ask your La Suite companion anything to get started.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="chat-messages">
      {visibleMessages.map((message) => (
        <div key={message.id} className="chat-message-row" data-role={message.role}>
          <div className="chat-message-group">
            <span className="chat-message-time">
              {message.role === 'assistant' && message.thinkingMs !== undefined
                ? formatThinkingDuration(message.thinkingMs)
                : formatRelativeTime(message.createdAt, now)}
            </span>
            <div className="chat-message" data-role={message.role}>
              {message.role === 'assistant' ? (
                <>
                  {message.trace && message.trace.length > 0 ? (
                    <details className="chat-trace">
                      <summary className="chat-trace-summary">
                        <svg
                          className="chat-trace-summary__arrow"
                          width="10"
                          height="10"
                          viewBox="0 0 10 10"
                          aria-hidden="true"
                        >
                          <path d="M2 1 L8 5 L2 9" fill="none" stroke="currentColor" strokeWidth="1.5" />
                        </svg>
                        {message.status ? (
                          <span className="chat-message-status">
                            <Loader size="small" />
                            {message.status}
                          </span>
                        ) : (
                          <span>View trace</span>
                        )}
                      </summary>
                      <ChatTrace trace={message.trace} />
                    </details>
                  ) : message.status ? (
                    <span className="chat-message-status">
                      <Loader size="small" />
                      {message.status}
                    </span>
                  ) : null}
                  {message.content ? (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
                  ) : null}
                </>
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
