import { CunninghamProvider, MainLayout } from '@gouvfr-lasuite/ui-kit'
import { useState } from 'react'
import ChatWindow from './features/chat/components/ChatWindow'
import ConversationList from './features/left-panel/components/ConversationList'
import type { SavedConversation } from './features/left-panel/api/conversations'
import WorkflowList from './features/workflows/components/WorkflowList'
import type { Workflow } from './features/workflows/api/workflows'
import UserFooter from './features/user-settings/components/UserFooter'
import appIcon from './assets/appIcon'

function App(): React.JSX.Element {
  const [conversationKey, setConversationKey] = useState(0)
  const [selectedConversation, setSelectedConversation] = useState<SavedConversation | null>(null)
  const [conversationsVersion, setConversationsVersion] = useState(0)
  const [workflowsVersion, setWorkflowsVersion] = useState(0)
  const [activeWorkflow, setActiveWorkflow] = useState<Workflow | null>(null)
  // Controlled so navigation actions can close the panel on compact/mobile
  // layouts, where it overlays the main window until dismissed.
  const [isLeftPanelOpen, setIsLeftPanelOpen] = useState(false)

  return (
    <CunninghamProvider theme="dsfr-light">
      <MainLayout
        icon={
          <span className="app-logo">
            <img src={appIcon} alt="" className="app-logo__icon" />
            Auto
          </span>
        }
        isLeftPanelOpen={isLeftPanelOpen}
        setIsLeftPanelOpen={setIsLeftPanelOpen}
        enableResize
        leftPanelContent={
          <>
            <ConversationList
              refreshKey={conversationsVersion}
              selectedConversationId={selectedConversation?.id ?? null}
              onNewConversation={() => {
                setSelectedConversation(null)
                setActiveWorkflow(null)
                setConversationKey((key) => key + 1)
                setIsLeftPanelOpen(false)
              }}
              onSelectConversation={(conversation) => {
                setSelectedConversation(conversation)
                setActiveWorkflow(null)
              }}
            />
            <WorkflowList
              refreshKey={workflowsVersion}
              onLaunch={(workflow) => {
                setSelectedConversation(null)
                setActiveWorkflow(workflow)
                setConversationKey((key) => key + 1)
                setIsLeftPanelOpen(false)
              }}
            />
          </>
        }
        leftPanelFooter={
          <UserFooter
            fullName="Jane Doe"
            email="jane.doe@example.com"
            onOpenSettings={() => setIsLeftPanelOpen(false)}
          />
        }
      >
        <ChatWindow
          key={selectedConversation?.id ?? conversationKey}
          initialConversation={selectedConversation ?? undefined}
          workflow={activeWorkflow ?? undefined}
          onConversationSaved={() => setConversationsVersion((version) => version + 1)}
          onWorkflowSaved={() => setWorkflowsVersion((v) => v + 1)}
        />
      </MainLayout>
    </CunninghamProvider>
  )
}

export default App
