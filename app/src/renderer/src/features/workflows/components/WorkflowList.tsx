import { Icon, IconSize } from '@gouvfr-lasuite/ui-kit'
import { useEffect, useState } from 'react'
import { deleteWorkflow, listWorkflows, type Workflow } from '../api/workflows'

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
    <div className="sidebar-section sidebar-section--workflows">
      <div className="sidebar-heading sidebar-heading--with-icon">
        <Icon name="bolt" size={IconSize.SMALL} />
        <span>Workflows</span>
      </div>
      {workflows.map((workflow) => (
        <div
          key={workflow.id}
          className="sidebar-row sidebar-row--workflow"
          role="button"
          tabIndex={0}
          onClick={() => onLaunch(workflow)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') onLaunch(workflow)
          }}
        >
          <span className="sidebar-row-icon sidebar-row-icon--workflow">
            <Icon name="play_arrow" size={IconSize.SMALL} />
          </span>
          <div className="sidebar-row-text">
            <div className="sidebar-row-title">{workflow.name}</div>
            <div className="sidebar-row-subtitle sidebar-row-subtitle--multiline">
              {workflow.description}
            </div>
          </div>
          <button
            type="button"
            className="sidebar-row-action"
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
  )
}

export default WorkflowList
