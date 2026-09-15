import { CunninghamProvider, MainLayout } from '@gouvfr-lasuite/ui-kit'
import ChatWindow from './features/chat/components/ChatWindow'

function App(): React.JSX.Element {
  return (
    <CunninghamProvider theme="dsfr-light">
      <MainLayout
        icon={<span className="app-logo">Auto</span>}
        leftPanelContent={
          <div className="app-left-panel">
            <h2>Conversations</h2>
            <p className="app-left-panel__hint">History coming soon.</p>
          </div>
        }
      >
        <ChatWindow />
      </MainLayout>
    </CunninghamProvider>
  )
}

export default App
