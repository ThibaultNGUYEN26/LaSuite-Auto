export type SpecialistTool = {
  name: string
  description: string
}

export type AgentSpecialization = {
  id: string
  name: string
  description: string
  enabled: boolean
  tools: SpecialistTool[]
}
