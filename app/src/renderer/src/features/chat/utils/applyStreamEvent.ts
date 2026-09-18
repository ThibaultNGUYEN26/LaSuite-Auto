import type { ChatMessage, StreamEvent } from '../types'

/** Pure reducer applying one SSE event to an in-flight assistant message. */
export function applyStreamEvent(
  message: ChatMessage,
  event: StreamEvent,
  askedAt: number
): ChatMessage {
  switch (event.type) {
    case 'step_start':
      return {
        ...message,
        status: `Thinking (step ${event.data.step})…`,
        trace: [
          ...(message.trace ?? []),
          {
            type: 'step',
            step: event.data.step,
            selectionPhase: event.data.selection_phase,
            selectionDurationMs: event.data.selection_duration_ms
          }
        ]
      }
    case 'token':
      return { ...message, content: message.content + event.data.delta, status: undefined }
    case 'tool_call_start':
      return {
        ...message,
        status: `Calling ${event.data.name}…`,
        trace: [
          ...(message.trace ?? []),
          {
            type: 'tool_call',
            toolCallId: event.data.tool_call_id,
            step: event.data.step,
            name: event.data.name,
            arguments: event.data.arguments
          }
        ]
      }
    case 'tool_call_result':
      return {
        ...message,
        trace: (message.trace ?? []).map((entry) =>
          entry.type === 'tool_call' && entry.toolCallId === event.data.tool_call_id
            ? { ...entry, result: event.data.result, durationMs: event.data.duration_ms }
            : entry
        )
      }
    case 'final':
      return {
        ...message,
        content: event.data.content,
        status: undefined,
        streaming: false,
        thinkingMs: Date.now() - askedAt,
        trace:
          event.data.total_duration_ms === undefined
            ? message.trace
            : [
                ...(message.trace ?? []),
                { type: 'total', durationMs: event.data.total_duration_ms }
              ]
      }
    case 'error':
      return {
        ...message,
        content: `Something went wrong: ${event.data.message}`,
        status: undefined,
        streaming: false,
        thinkingMs: Date.now() - askedAt
      }
    case 'step_complete':
      return {
        ...message,
        trace: (message.trace ?? []).map((entry) =>
          entry.type === 'step' && entry.step === event.data.step
            ? {
                ...entry,
                modelDurationMs: event.data.model_duration_ms,
                firstResponseMs: event.data.first_response_ms
              }
            : entry
        )
      }
    case 'workflow_suggested':
      return message
  }
}
