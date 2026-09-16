import { Icon, IconSize, UserAvatar } from '@gouvfr-lasuite/ui-kit'
import { useState } from 'react'
import AccessSettingsModal from './AccessSettingsModal'
import './UserFooter.css'

type UserFooterProps = {
  fullName: string
  email: string
  onOpenSettings?: () => void
}

function UserFooter({ fullName, email, onOpenSettings }: UserFooterProps): React.JSX.Element {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false)

  return (
    <>
      <button
        type="button"
        className="user-footer"
        aria-label="Open access & security settings"
        onClick={() => {
          setIsSettingsOpen(true)
          onOpenSettings?.()
        }}
      >
        <UserAvatar fullName={fullName} size="small" />
        <span className="user-footer__text">
          <span className="user-footer__name">{fullName}</span>
          <span className="user-footer__email">{email}</span>
        </span>
        <Icon name="settings" size={IconSize.SMALL} className="user-footer__icon" />
      </button>
      {isSettingsOpen ? <AccessSettingsModal onClose={() => setIsSettingsOpen(false)} /> : null}
    </>
  )
}

export default UserFooter
