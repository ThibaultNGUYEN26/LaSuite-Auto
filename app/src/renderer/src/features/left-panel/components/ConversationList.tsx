import { HorizontalSeparator, Icon, IconSize } from '@gouvfr-lasuite/ui-kit'
import { useEffect, useState } from 'react'
import { createConversation } from '../api/createConversation'
import { listConversations, type SavedConversation } from '../api/conversations'

type ConversationListProps = {
  refreshKey: number
  onNewConversation: () => void
  onSelectConversation: (conversation: SavedConversation) => void
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(new Date(value))
}

function ConversationList({
  refreshKey,
  onNewConversation,
  onSelectConversation
}: ConversationListProps): React.JSX.Element {
  const [isCreating, setIsCreating] = useState(false)
  const [conversations, setConversations] = useState<SavedConversation[]>([])

  const refreshConversations = (): void => {
    listConversations().then(setConversations).catch(() => setConversations([]))
  }

  useEffect(() => {
    refreshConversations()
  }, [refreshKey])

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
      <div className="conversation-list-items">
        {conversations.map((conversation) => (
          <button
            key={conversation.id}
            type="button"
            className="conversation-list-item"
            onClick={() => onSelectConversation(conversation)}
          >
            <div className="conversation-list-item-title">{conversation.title}</div>
            <div className="conversation-list-item-subtitle">
              {formatDate(conversation.updated_at)}
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}

export default ConversationList
