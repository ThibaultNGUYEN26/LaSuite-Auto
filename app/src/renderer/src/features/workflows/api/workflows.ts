import type { ChatMessage, WorkflowDraft } from '../../chat/types'

const BACKEND_URL = import.meta.env.BACKEND_URL ?? 'http://127.0.0.1:8000'

export type Workflow = {
  id: string
  name: string
  description: string
  instructions: string
  input_question: string
  created_at: string
  updated_at: string
}

async function parseOrThrow<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.text().catch(() => '')
    throw new Error(`backend responded with ${response.status}${error ? `: ${error}` : ''}`)
  }
  return response.json() as Promise<T>
}

export async function listWorkflows(): Promise<Workflow[]> {
  const response = await fetch(`${BACKEND_URL}/api/workflows`)
  return parseOrThrow<Workflow[]>(response)
}

export async function draftWorkflow(messages: ChatMessage[]): Promise<WorkflowDraft> {
  const response = await fetch(`${BACKEND_URL}/api/workflows/draft`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages: messages.map(({ role, content }) => ({ role, content })) })
  })
  return parseOrThrow<WorkflowDraft>(response)
}

export async function saveWorkflow(draft: WorkflowDraft): Promise<Workflow> {
  const response = await fetch(`${BACKEND_URL}/api/workflows`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(draft)
  })
  return parseOrThrow<Workflow>(response)
}

export async function deleteWorkflow(id: string): Promise<void> {
  const response = await fetch(`${BACKEND_URL}/api/workflows/${id}`, { method: 'DELETE' })
  if (!response.ok) {
    const error = await response.text().catch(() => '')
    throw new Error(`backend responded with ${response.status}${error ? `: ${error}` : ''}`)
  }
}
