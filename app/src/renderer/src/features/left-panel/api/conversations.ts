const BACKEND_URL = import.meta.env.BACKEND_URL ?? 'http://127.0.0.1:8000'

export type SavedConversation = {
  id: string
  title: string
  created_at: string
  updated_at: string
  messages: Array<{ role: 'user' | 'assistant'; content: string }>
}

export async function listConversations(): Promise<SavedConversation[]> {
  const response = await fetch(`${BACKEND_URL}/api/conversations`)
  if (!response.ok) {
    const error = await response.text().catch(() => '')
    throw new Error(`backend responded with ${response.status}${error ? `: ${error}` : ''}`)
  }
  return response.json() as Promise<SavedConversation[]>
}

export async function deleteConversation(id: string): Promise<void> {
  const response = await fetch(`${BACKEND_URL}/api/conversations/${id}`, { method: 'DELETE' })
  if (!response.ok) {
    const error = await response.text().catch(() => '')
    throw new Error(`backend responded with ${response.status}${error ? `: ${error}` : ''}`)
  }
}