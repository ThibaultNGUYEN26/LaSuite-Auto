import { HorizontalSeparator, Icon, IconSize } from '@gouvfr-lasuite/ui-kit'
import { useEffect, useState } from 'react'
import { deleteWorkflow, listWorkflows, type Workflow } from '../api/workflows'
import './WorkflowList.css'

type WorkflowListProps = {
  refreshKey: number
  onLaunch: (workflow: Workflow) => void
}

function WorkflowList({ refreshKey, onLaunch }: WorkflowListProps): React.JSX.Element {
  const [workflows, setWorkflows] = useState<Workflow[]>([])

  useEffect(() => {
    let cancelled = false
    listWorkflows()
      .then((result) => {
        if (!cancelled) setWorkflows(result)
      })
      .catch(() => {
        // Left-panel listing is best-effort; an empty list is a safe fallback.
      })
    return () => {
      cancelled = true
    }
  }, [refreshKey])

  const handleDelete = async (id: string): Promise<void> => {
    setWorkflows((current) => current.filter((w) => w.id !== id))
    try {
      await deleteWorkflow(id)
    } catch {
      // Best-effort: if the delete failed the next refresh will restore it.
    }
  }

  if (workflows.length === 0) return <></>

  return (
    <div className="workflow-list">
      <HorizontalSeparator />
      <div className="workflow-list-heading">Workflows</div>
      <div className="workflow-list-items">
        {workflows.map((workflow) => (
          <div
            key={workflow.id}
            className="workflow-list-item"
            role="button"
            tabIndex={0}
            onClick={() => onLaunch(workflow)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') onLaunch(workflow)
            }}
          >
            <div className="workflow-list-item-text">
              <div className="workflow-list-item-title">{workflow.name}</div>
              <div className="workflow-list-item-subtitle">{workflow.description}</div>
            </div>
            <button
              type="button"
              className="workflow-list-item-delete"
              aria-label={`Delete ${workflow.name}`}
              onClick={(e) => {
                e.stopPropagation()
                void handleDelete(workflow.id)
              }}
            >
              <Icon name="delete" size={IconSize.SMALL} />
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default WorkflowList
