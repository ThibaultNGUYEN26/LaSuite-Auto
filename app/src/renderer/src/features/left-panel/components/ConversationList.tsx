import { HorizontalSeparator, Icon, IconSize } from '@gouvfr-lasuite/ui-kit'
import { useState } from 'react'
import { createConversation } from '../api/createConversation'
import './ConversationList.css'

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
    <div className="conversation-list">
      <button
        type="button"
        className="conversation-list-new-button"
        disabled={isCreating}
        onClick={handleNewConversation}
        aria-label="New conversation"
      >
        <span className="conversation-list-new-button-icon">
          <Icon name="add" size={IconSize.SMALL} />
        </span>
        New conversation
      </button>
      <HorizontalSeparator />
      <div className="conversation-list-items">
        {PLACEHOLDER_CONVERSATIONS.map((conversation) => (
          <div key={conversation.id} className="conversation-list-item">
            <div className="conversation-list-item-title">{conversation.title}</div>
            <div className="conversation-list-item-subtitle">{conversation.subtitle}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ConversationList
