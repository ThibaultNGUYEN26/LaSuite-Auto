import { Button } from '@gouvfr-lasuite/cunningham-react'
import { DropdownMenu, Icon, IconSize } from '@gouvfr-lasuite/ui-kit'
import { FormEvent, KeyboardEvent, useState } from 'react'
import './Composer.css'

type ComposerProps = {
  value: string
  onChange: (value: string) => void
  onSubmit: (e: FormEvent) => void
  canSubmit: boolean
  isSending?: boolean
  onStop?: () => void
  onSaveAsWorkflow?: () => void
  isSavingWorkflow?: boolean
}

function Composer({
  value,
  onChange,
  onSubmit,
  canSubmit,
  isSending,
  onStop,
  onSaveAsWorkflow,
  isSavingWorkflow
}: ComposerProps): React.JSX.Element {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

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
            {onSaveAsWorkflow ? (
              <DropdownMenu
                isOpen={isMenuOpen}
                onOpenChange={setIsMenuOpen}
                options={[
                  {
                    label: 'Save as workflow',
                    isDisabled: isSavingWorkflow,
                    callback: () => {
                      setIsMenuOpen(false)
                      onSaveAsWorkflow()
                    }
                  }
                ]}
              >
                <Button
                  type="button"
                  variant="tertiary"
                  size="small"
                  className="chat-composer-more"
                  icon={<Icon name="more_horiz" size={IconSize.SMALL} />}
                  aria-label="More actions"
                  onClick={() => setIsMenuOpen((open) => !open)}
                />
              </DropdownMenu>
            ) : null}
            {isSending ? (
              <Button
                type="button"
                variant="primary"
                size="small"
                className="chat-composer-send chat-composer-stop"
                onClick={onStop}
                icon={<Icon name="stop" size={IconSize.SMALL} />}
                aria-label="Stop generating"
              />
            ) : (
              <Button
                type="submit"
                variant="primary"
                size="small"
                className="chat-composer-send c__button--send"
                disabled={!canSubmit}
                icon={<Icon name="arrow_upward" size={IconSize.SMALL} />}
                aria-label="Send message"
              />
            )}
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
