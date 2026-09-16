import { HorizontalSeparator, Icon, IconSize } from '@gouvfr-lasuite/ui-kit'
import { useState } from 'react'
import { createConversation } from '../api/createConversation'

const PLACEHOLDER_CONVERSATIONS = [
  { id: '1', title: 'Trip planning ideas', subtitle: 'Yesterday' },
  { id: '2', title: 'Debugging the API client', subtitle: '2 days ago' },
  { id: '3', title: 'Draft project README', subtitle: 'Last week' }
]

type ConversationListProps = {
  onNewConversation: () => void
}

function ConversationList({ onNewConversation }: ConversationListProps): React.JSX.Element {
  const [isCreating, setIsCreating] = useState(false)

  const handleNewConversation = async (): Promise<void> => {
    setIsCreating(true)
    try {
      await createConversation()
    } catch {
      // Chat history lives client-side, so a failed acknowledgment doesn't
      // block starting a fresh conversation locally.
    } finally {
      setIsCreating(false)
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
      <div className="sidebar-divider">
        <HorizontalSeparator />
      </div>
      {PLACEHOLDER_CONVERSATIONS.map((conversation) => (
        <div key={conversation.id} className="sidebar-row">
          <div className="sidebar-row-text">
            <div className="sidebar-row-title">{conversation.title}</div>
            <div className="sidebar-row-subtitle">{conversation.subtitle}</div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default ConversationList
