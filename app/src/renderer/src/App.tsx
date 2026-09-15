import { CunninghamProvider, MainLayout } from '@gouvfr-lasuite/ui-kit'
import { useState } from 'react'
import ChatWindow from './features/chat/components/ChatWindow'
import ConversationList from './features/left-panel/components/ConversationList'
import appIcon from './assets/appIcon'

function App(): React.JSX.Element {
  const [conversationKey, setConversationKey] = useState(0)

  return (
    <CunninghamProvider theme="dsfr-light">
      <MainLayout
        icon={
          <span className="app-logo">
            <img src={appIcon} alt="" className="app-logo__icon" />
            Auto
          </span>
        }
        leftPanelContent={
          <ConversationList onNewConversation={() => setConversationKey((key) => key + 1)} />
        }
      >
        <ChatWindow key={conversationKey} />
      </MainLayout>
    </CunninghamProvider>
  )
}

export default App
