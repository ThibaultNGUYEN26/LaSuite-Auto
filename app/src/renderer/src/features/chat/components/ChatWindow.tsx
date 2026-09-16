import { VariantType } from '@gouvfr-lasuite/cunningham-react'
import { Alert, Icon, IconSize } from '@gouvfr-lasuite/ui-kit'
import { FormEvent, useEffect, useRef, useState } from 'react'
import { streamChatMessage } from '../api/streamChatMessage'
import { applyStreamEvent } from '../utils/applyStreamEvent'
import type { ChatMessage, StreamEvent, WorkflowDraft } from '../types'
import { draftWorkflow, type Workflow } from '../../workflows/api/workflows'
import type { SavedConversation } from '../../left-panel/api/conversations'
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
    },
    {
      id: crypto.randomUUID(),
      role: 'assistant',
      content: workflow.input_question,
      createdAt: Date.now()
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
  const [messages, setMessages] = useState<ChatMessage[]>(() =>
    initialConversation
      ? initialConversation.messages.map((message, index) => ({
          ...message,
          id: `${initialConversation.id}-${index}`,
          createdAt: Date.now() - (initialConversation.messages.length - index) * 1000
        }))
      : seedMessages(workflow)
  )
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [suggestion, setSuggestion] = useState<WorkflowDraft | null>(null)
  const [draftForSave, setDraftForSave] = useState<WorkflowDraft | null>(null)
  const [isDraftingManually, setIsDraftingManually] = useState(false)
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
    setSuggestion(null)

    const askedAt = Date.now()

    const onEvent = (event: StreamEvent): void => {
      if (event.type === 'workflow_suggested') {
        setSuggestion(event.data)
        return
      }
      if (event.type === 'final') onConversationSaved?.()
      setMessages((current) =>
        current.map((m) => (m.id === assistantMessage.id ? applyStreamEvent(m, event, askedAt) : m))
      )
    }

    try {
      await streamChatMessage(chatId, nextMessages, onEvent, controller.signal)
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
