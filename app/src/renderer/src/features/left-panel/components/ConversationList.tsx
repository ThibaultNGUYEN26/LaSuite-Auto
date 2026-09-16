import { HorizontalSeparator, Icon, IconSize } from '@gouvfr-lasuite/ui-kit'
import { useEffect, useState } from 'react'
import { createConversation } from '../api/createConversation'
import { deleteConversation, listConversations, type SavedConversation } from '../api/conversations'

type ConversationListProps = {
  refreshKey: number
  selectedConversationId: string | null
  onNewConversation: () => void
  onSelectConversation: (conversation: SavedConversation) => void
  onDeleteConversation: (id: string) => void
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(new Date(value))
}

function ConversationList({
  refreshKey,
  selectedConversationId,
  onNewConversation,
  onSelectConversation,
  onDeleteConversation
}: ConversationListProps): React.JSX.Element {
  const [isCreating, setIsCreating] = useState(false)
  const [conversations, setConversations] = useState<SavedConversation[]>([])

  const refreshConversations = (): void => {
    listConversations().then(setConversations).catch(() => setConversations([]))
  }

  useEffect(() => {
    refreshConversations()
  }, [refreshKey])

  const handleDelete = async (id: string): Promise<void> => {
    setConversations((current) => current.filter((c) => c.id !== id))
    onDeleteConversation(id)
    try {
      await deleteConversation(id)
    } catch {
      // Best-effort: if the delete failed the next refresh will restore it.
    }
  }

  const handleNewConversation = async (): Promise<void> => {
    setIsCreating(true)
    try {
      await createConversation()
    } catch {
      // Chat history lives client-side, so a failed acknowledgment doesn't
      // block starting a fresh conversation locally.
    } finally {
      setIsCreating(false)
      refreshConversations()
      onNewConversation()
    }
  }

  return (
    <div className="sidebar-section">
      <button
        type="button"
        className="sidebar-row"
        disabled={isCreating}
        onClick={handleNewConversation}
        aria-label="New conversation"
      >
        <span className="sidebar-row-icon">
          <Icon name="add" size={IconSize.SMALL} />
        </span>
        <span className="sidebar-row-text sidebar-row-title">New conversation</span>
      </button>
      <HorizontalSeparator />
      {conversations.map((conversation) => (
        <div
          key={conversation.id}
          className="sidebar-row"
          role="button"
          tabIndex={0}
          data-active={conversation.id === selectedConversationId}
          onClick={() => onSelectConversation(conversation)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') onSelectConversation(conversation)
          }}
        >
          <span className="sidebar-row-text">
            <span className="sidebar-row-title">{conversation.title}</span>
            <span className="sidebar-row-subtitle">{formatDate(conversation.updated_at)}</span>
          </span>
          <button
            type="button"
            className="sidebar-row-action"
            aria-label={`Delete ${conversation.title}`}
            onClick={(e) => {
              e.stopPropagation()
              void handleDelete(conversation.id)
            }}
          >
            <Icon name="delete" size={IconSize.SMALL} />
          </button>
        </div>
      ))}
    </div>
  )
}

export default ConversationList
