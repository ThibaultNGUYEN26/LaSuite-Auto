import { CunninghamProvider, MainLayout } from '@gouvfr-lasuite/ui-kit'
import { useState } from 'react'
import ChatWindow from './features/chat/components/ChatWindow'
import ConversationList from './features/left-panel/components/ConversationList'
import WorkflowList from './features/workflows/components/WorkflowList'
import type { Workflow } from './features/workflows/api/workflows'
import appIcon from './assets/appIcon'

function App(): React.JSX.Element {
  const [conversationKey, setConversationKey] = useState(0)
  const [workflowsVersion, setWorkflowsVersion] = useState(0)
  const [activeWorkflow, setActiveWorkflow] = useState<Workflow | null>(null)

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
          <>
            <ConversationList
              onNewConversation={() => {
                setActiveWorkflow(null)
                setConversationKey((key) => key + 1)
              }}
            />
            <WorkflowList
              refreshKey={workflowsVersion}
              onLaunch={(workflow) => {
                setActiveWorkflow(workflow)
                setConversationKey((key) => key + 1)
              }}
            />
          </>
        }
      >
        <ChatWindow
          key={conversationKey}
          workflow={activeWorkflow ?? undefined}
          onWorkflowSaved={() => setWorkflowsVersion((v) => v + 1)}
        />
      </MainLayout>
    </CunninghamProvider>
  )
}

export default App
