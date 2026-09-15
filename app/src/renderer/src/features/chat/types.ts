export type ChatMessage = {
  id: string
  role: 'user' | 'assistant'
  content: string
  createdAt: number
  /** How long the assistant took to reply, in milliseconds. Only set for assistant messages. */
  thinkingMs?: number
  /** Transient live-progress text (e.g. "Calling drive_list_items…") while a reply is streaming in. */
  status?: string
  /** True while this assistant message is still receiving stream events. */
  streaming?: boolean
}

export type StreamEvent =
  | { type: 'step_start'; data: { step: number; max_steps: number } }
  | { type: 'token'; data: { step: number; delta: string } }
  | {
      type: 'tool_call_start'
      data: { step: number; tool_call_id: string; name: string; arguments: unknown }
    }
  | {
      type: 'tool_call_result'
      data: { step: number; tool_call_id: string; name: string; result: unknown }
    }
  | {
      type: 'step_complete'
      data: { step: number; content: string | null; tool_calls: unknown[] }
    }
  | { type: 'final'; data: { content: string } }
  | { type: 'error'; data: { message: string; error_type: string } }
