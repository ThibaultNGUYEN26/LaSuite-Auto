import { Button, Input, Modal, ModalSize, TextArea } from '@gouvfr-lasuite/cunningham-react'
import { useState } from 'react'
import type { WorkflowDraft } from '../../chat/types'
import { saveWorkflow } from '../api/workflows'
import './SaveWorkflowModal.css'

type SaveWorkflowModalProps = {
  draft: WorkflowDraft
  onClose: () => void
  onSaved: () => void
}

function SaveWorkflowModal({ draft, onClose, onSaved }: SaveWorkflowModalProps): React.JSX.Element {
  const [form, setForm] = useState<WorkflowDraft>(draft)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSave = async (): Promise<void> => {
    if (!form.name.trim() || isSaving) return
    setIsSaving(true)
    setError(null)
    try {
      await saveWorkflow(form)
      onSaved()
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <Modal
      isOpen
      size={ModalSize.LARGE}
      onClose={onClose}
      title="Save as workflow"
      rightActions={
        <>
          <Button color="neutral" onClick={onClose} disabled={isSaving}>
            Cancel
          </Button>
          <Button onClick={handleSave} disabled={!form.name.trim() || isSaving}>
            Save workflow
          </Button>
        </>
      }
    >
      <div className="save-workflow-form">
        <Input
          label="Name"
          value={form.name}
          onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
        />
        <Input
          label="Description"
          value={form.description}
          onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
        />
        <TextArea
          label="Instructions"
          value={form.instructions}
          onChange={(e) => setForm((f) => ({ ...f, instructions: e.target.value }))}
          rows={6}
        />
        <Input
          label="Question to ask when launching this workflow"
          value={form.input_question}
          onChange={(e) => setForm((f) => ({ ...f, input_question: e.target.value }))}
        />
        {error ? <p className="save-workflow-form__error">{error}</p> : null}
      </div>
    </Modal>
  )
}

export default SaveWorkflowModal
