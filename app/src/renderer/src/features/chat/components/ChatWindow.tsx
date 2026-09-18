import { VariantType } from '@gouvfr-lasuite/cunningham-react'
import { Alert, Icon, IconSize } from '@gouvfr-lasuite/ui-kit'
import { FormEvent, useEffect, useRef, useState } from 'react'
import { streamChatMessage } from '../api/streamChatMessage'
import { applyStreamEvent } from '../utils/applyStreamEvent'
import type { ChatMessage, StreamEvent, WorkflowDraft } from '../types'
import { draftWorkflow, type Workflow } from '../../workflows/api/workflows'
import {
  generateConversationTitle,
  type SavedConversation
} from '../../left-panel/api/conversations'
import SaveWorkflowModal from '../../workflows/components/SaveWorkflowModal'
import './ChatWindow.css'
import Composer from './Composer'
import MessageList from './MessageList'

function seedMessages(workflow: Workflow | undefined): ChatMessage[] {
  if (!workflow) return []
  return [
    {
      id: crypto.randomUUID(),
      role: 'user',
      content: workflow.instructions,
      createdAt: Date.now(),
      hidden: true
    }
  ]
}

type ChatWindowProps = {
  initialConversation?: SavedConversation
  workflow?: Workflow
  onConversationSaved?: () => void
  onWorkflowSaved?: () => void
}

function ChatWindow({
  initialConversation,
  workflow,
  onConversationSaved,
  onWorkflowSaved
}: ChatWindowProps): React.JSX.Element {
  const [chatId] = useState(
    () => initialConversation?.id ?? crypto.randomUUID().replaceAll('-', '')
  )
  const [messages, setMessages] = useState<ChatMessage[]>(() => {
    if (!initialConversation) return seedMessages(workflow)
    // Per-message timestamps aren't persisted, so approximate them by
    // spacing messages backward from when the conversation was last saved -
    // anchoring to Date.now() would show every reopened message as "Just now".
    const savedAt = new Date(initialConversation.updated_at).getTime()
    return initialConversation.messages.map((message, index) => ({
      ...message,
      id: `${initialConversation.id}-${index}`,
      createdAt: savedAt - (initialConversation.messages.length - 1 - index) * 1000
    }))
  })
  const [input, setInput] = useState(() =>
    initialConversation ? '' : (workflow?.input_question ?? '')
  )
  const [isSending, setIsSending] = useState(false)
  const [suggestion, setSuggestion] = useState<WorkflowDraft | null>(null)
  const [draftForSave, setDraftForSave] = useState<WorkflowDraft | null>(null)
  const [isDraftingManually, setIsDraftingManually] = useState(false)
  const abortControllerRef = useRef<AbortController | null>(null)
  const pendingEventsRef = useRef<StreamEvent[]>([])
  const flushHandleRef = useRef<number | null>(null)
  // Existing conversations already have a title; only generate one for a brand-new chat's
  // first exchange, and only once, even if the effect/handler re-runs.
  const titleGeneratedRef = useRef(Boolean(initialConversation))

  useEffect(() => {
    return () => {
      abortControllerRef.current?.abort()
      if (flushHandleRef.current !== null) cancelAnimationFrame(flushHandleRef.current)
    }
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
    setSuggestion(null)

    const askedAt = Date.now()

    // Streams can emit many `token` events per second. Applying each one as its own
    // setState causes a render (and a markdown re-parse + scroll) per token, which is
    // what produces the laggy, jumping-around appearance. Buffer events and apply them
    // in one batch per animation frame instead.
    const flushPendingEvents = (): void => {
      flushHandleRef.current = null
      const events = pendingEventsRef.current
      pendingEventsRef.current = []
      if (events.length === 0) return
      setMessages((current) =>
        current.map((m) =>
          m.id === assistantMessage.id
            ? events.reduce((msg, event) => applyStreamEvent(msg, event, askedAt), m)
            : m
        )
      )
    }

    const onEvent = (event: StreamEvent): void => {
      if (event.type === 'workflow_suggested') {
        setSuggestion(event.data)
        return
      }
      if (event.type === 'final') {
        onConversationSaved?.()
        if (!titleGeneratedRef.current) {
          titleGeneratedRef.current = true
          generateConversationTitle(chatId, userMessage.content, event.data.content)
            .then(() => onConversationSaved?.())
            .catch(() => {
              // Title generation is a nicety; the fallback (first-message) title still works.
            })
        }
      }

      pendingEventsRef.current.push(event)

      // Terminal events should land immediately rather than waiting a frame.
      if (event.type === 'final' || event.type === 'error') {
        if (flushHandleRef.current !== null) cancelAnimationFrame(flushHandleRef.current)
        flushPendingEvents()
        return
      }

      if (flushHandleRef.current === null) {
        flushHandleRef.current = requestAnimationFrame(flushPendingEvents)
      }
    }

    try {
      await streamChatMessage(chatId, nextMessages, onEvent, controller.signal)
    } catch (error) {
      if (flushHandleRef.current !== null) {
        cancelAnimationFrame(flushHandleRef.current)
        flushHandleRef.current = null
      }
      if ((error as Error).name === 'AbortError') {
        // Flush whatever tokens had already streamed in so the stopped reply
        // stays visible instead of vanishing, and stop the "Thinking…" spinner.
        // The backend persists this same partial content on its disconnect path,
        // so it survives a reload of the conversation too.
        flushPendingEvents()
        patchMessage(assistantMessage.id, {
          status: undefined,
          streaming: false,
          thinkingMs: Date.now() - askedAt
        })
        return
      }
      pendingEventsRef.current = []
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

  const handleStop = (): void => {
    abortControllerRef.current?.abort()
  }

  const handleSaveAsWorkflow = async (): Promise<void> => {
    if (messages.length === 0 || isDraftingManually) return
    setIsDraftingManually(true)
    try {
      const draft = await draftWorkflow(messages)
      setDraftForSave(draft)
    } catch {
      // Drafting is a convenience; a failure here shouldn't interrupt the chat.
    } finally {
      setIsDraftingManually(false)
    }
  }

  return (
    <div className="chat-wrapper">
      <div className="chat">
        {workflow ? (
          <Alert
            className="workflow-active-banner"
            type={VariantType.INFO}
            icon={<Icon name="bolt" size={IconSize.SMALL} />}
          >
            Running workflow: <strong>{workflow.name}</strong>
          </Alert>
        ) : null}
        <MessageList messages={messages} isSending={isSending} />
        {suggestion ? (
          <Alert
            className="workflow-suggestion"
            type={VariantType.INFO}
            canClose
            onClose={() => setSuggestion(null)}
            primaryLabel="Save"
            primaryOnClick={() => {
              setDraftForSave(suggestion)
              setSuggestion(null)
            }}
            tertiaryLabel="Dismiss"
            tertiaryOnClick={() => setSuggestion(null)}
          >
            <strong>Save this as a workflow?</strong> {suggestion.name} — {suggestion.description}
          </Alert>
        ) : null}
        <Composer
          value={input}
          onChange={setInput}
          onSubmit={handleSubmit}
          canSubmit={canSubmit}
          isSending={isSending}
          onStop={handleStop}
          onSaveAsWorkflow={messages.length > 0 ? handleSaveAsWorkflow : undefined}
          isSavingWorkflow={isDraftingManually}
        />
      </div>
      {draftForSave ? (
        <SaveWorkflowModal
          draft={draftForSave}
          onClose={() => setDraftForSave(null)}
          onSaved={() => {
            setDraftForSave(null)
            onWorkflowSaved?.()
          }}
        />
      ) : null}
    </div>
  )
}

export default ChatWindow
