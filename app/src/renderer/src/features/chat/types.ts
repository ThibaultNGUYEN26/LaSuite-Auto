export type TraceEntry =
  | { type: 'step'; step: number }
  | {
      type: 'tool_call'
      toolCallId: string
      step: number
      name: string
      arguments: unknown
      result?: unknown
    }

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
  /** Ordered log of steps/tool calls performed while producing this message, shown in a trace dropdown. */
  trace?: TraceEntry[]
  /** Sent to the backend as conversation context but not rendered (e.g. a workflow's instructions). */
  hidden?: boolean
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
  | { type: 'workflow_suggested'; data: WorkflowDraft }

export type WorkflowDraft = {
  name: string
  description: string
  instructions: string
  input_question: string
}
