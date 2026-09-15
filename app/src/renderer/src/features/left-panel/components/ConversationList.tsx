import { Button } from '@gouvfr-lasuite/cunningham-react'
import { HorizontalSeparator } from '@gouvfr-lasuite/ui-kit'
import './ConversationList.css'

const PLACEHOLDER_CONVERSATIONS = [
  { id: '1', title: 'Trip planning ideas', subtitle: 'Yesterday' },
  { id: '2', title: 'Debugging the API client', subtitle: '2 days ago' },
  { id: '3', title: 'Draft project README', subtitle: 'Last week' }
]

function ConversationList(): React.JSX.Element {
  return (
    <div className="conversation-list">
      <Button className="conversation-list-new-button" color="brand">
        New conversation
      </Button>
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
