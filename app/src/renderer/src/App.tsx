import { CunninghamProvider, MainLayout } from '@gouvfr-lasuite/ui-kit'
import ChatWindow from './features/chat/components/ChatWindow'
import ConversationList from './features/left-panel/components/ConversationList'
import appIcon from './assets/appIcon'

function App(): React.JSX.Element {
  return (
    <CunninghamProvider theme="dsfr-light">
      <MainLayout
        icon={
          <span className="app-logo">
            <img src={appIcon} alt="" className="app-logo__icon" />
            Auto
          </span>
        }
        leftPanelContent={<ConversationList />}
      >
        <ChatWindow />
      </MainLayout>
    </CunninghamProvider>
  )
}

export default App
