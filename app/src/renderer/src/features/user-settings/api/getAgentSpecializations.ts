import type { AgentSpecialization } from '../types'

const BACKEND_URL = import.meta.env.BACKEND_URL ?? 'http://127.0.0.1:8000'

export async function getAgentSpecializations(): Promise<AgentSpecialization[]> {
  const response = await fetch(`${BACKEND_URL}/api/agent/specializations`)
  if (!response.ok) {
    const error = await response.text().catch(() => '')
    throw new Error(`backend responded with ${response.status}${error ? `: ${error}` : ''}`)
  }
  return response.json() as Promise<AgentSpecialization[]>
}
