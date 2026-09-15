import { Button } from '@gouvfr-lasuite/cunningham-react'
import { Icon, IconSize } from '@gouvfr-lasuite/ui-kit'
import { FormEvent, KeyboardEvent } from 'react'
import './Composer.css'

type ComposerProps = {
  value: string
  onChange: (value: string) => void
  onSubmit: (e: FormEvent) => void
  canSubmit: boolean
}

function Composer({ value, onChange, onSubmit, canSubmit }: ComposerProps): React.JSX.Element {
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>): void => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      onSubmit(e as unknown as FormEvent)
    }
  }

  return (
    <div className="chat-composer">
      <form onSubmit={onSubmit}>
        <div className="chat-composer-box">
          <textarea
            className="chat-composer-textarea"
            aria-label="Message"
            placeholder="Write a message…"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <div className="chat-composer-actions">
            <Button
              type="submit"
              variant="primary"
              size="small"
              className="chat-composer-send c__button--send"
              disabled={!canSubmit}
              icon={<Icon name="arrow_upward" size={IconSize.SMALL} />}
              aria-label="Send message"
            />
          </div>
        </div>
      </form>
      <p className="chat-composer-disclaimer">
        The assistant can make mistakes. Verify important information.
      </p>
    </div>
  )
}

export default Composer
