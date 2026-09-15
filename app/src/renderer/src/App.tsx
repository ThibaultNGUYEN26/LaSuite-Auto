import { CunninghamProvider, MainLayout } from '@gouvfr-lasuite/ui-kit'
import ChatWindow from './features/chat/components/ChatWindow'
import ConversationList from './features/left-panel/components/ConversationList'

function App(): React.JSX.Element {
  return (
    <CunninghamProvider theme="dsfr-light">
      <MainLayout
        icon={<span className="app-logo">Auto</span>}
        leftPanelContent={<ConversationList />}
      >
        <ChatWindow />
      </MainLayout>
    </CunninghamProvider>
  )
}

export default App
