import {
  Button,
  Input,
  Modal,
  ModalSize,
  Radio,
  RadioGroup,
  Switch,
  Tooltip
} from '@gouvfr-lasuite/cunningham-react'
import { Badge, HorizontalSeparator, Icon, IconSize } from '@gouvfr-lasuite/ui-kit'
import { useEffect, useState } from 'react'
import { getAgentSpecializations } from '../api/getAgentSpecializations'
import type { AgentSpecialization } from '../types'
import './AccessSettingsModal.css'

type AccessLevel = 'read_only' | 'read_write' | 'full_access'

// Demo-only teasers: these specializations don't exist yet on the backend.
// They're shown disabled with a "Coming soon" badge to preview the roadmap.
const TEASER_SPECIALIZATIONS: AgentSpecialization[] = [
  {
    id: 'teaser-web-browsing',
    name: 'Web browsing',
    description: 'Browses the internet to research topics, check facts, and pull live information.',
    enabled: false,
    tools: [
      { name: 'web_search', description: 'Search the web for relevant pages' },
      { name: 'fetch_page', description: 'Open and read the content of a web page' }
    ]
  },
  {
    id: 'teaser-email-connector',
    name: 'Email connector',
    description: 'Reads and sends email on your behalf through a connected inbox.',
    enabled: false,
    tools: [
      { name: 'read_inbox', description: 'Search and read messages in a connected mailbox' },
      { name: 'send_email', description: 'Draft and send an email' }
    ]
  },
  {
    id: 'teaser-france-transfert',
    name: 'France Transfert sharing',
    description: 'Generates France Transfert links to share large files securely.',
    enabled: false,
    tools: [
      { name: 'upload_file', description: 'Upload a file to France Transfert' },
      { name: 'create_share_link', description: 'Create a shareable download link' }
    ]
  }
]

type AccessSettingsModalProps = {
  onClose: () => void
}

function AccessSettingsModal({ onClose }: AccessSettingsModalProps): React.JSX.Element {
  const [accessLevel, setAccessLevel] = useState<AccessLevel>('full_access')
  const [localFilesRoot, setLocalFilesRoot] = useState('~/')

  const [specializations, setSpecializations] = useState<AgentSpecialization[]>([])
  const [specializationsError, setSpecializationsError] = useState<string | null>(null)
  const [isLoadingSpecializations, setIsLoadingSpecializations] = useState(true)

  useEffect(() => {
    let cancelled = false
    getAgentSpecializations()
      .then((result) => {
        if (!cancelled) setSpecializations(result)
      })
      .catch((err) => {
        if (!cancelled) setSpecializationsError((err as Error).message)
      })
      .finally(() => {
        if (!cancelled) setIsLoadingSpecializations(false)
      })
    return () => {
      cancelled = true
    }
  }, [])

  const toggleSpecialization = (id: string): void => {
    setSpecializations((current) =>
      current.map((spec) => (spec.id === id ? { ...spec, enabled: !spec.enabled } : spec))
    )
  }

  return (
    <Modal
      isOpen
      size={ModalSize.LARGE}
      onClose={onClose}
      title="Access & security settings"
      subtitle="Preview of the controls that will govern what this agent can see and do."
      rightActions={
        <Button color="neutral" onClick={onClose}>
          Close
        </Button>
      }
    >
      <div className="access-settings">
        <section className="access-settings__section">
          <h3 className="access-settings__heading">Access rights</h3>
          <p className="access-settings__hint">
            Decorative for now — the agent does not yet enforce this restriction.
          </p>
          <RadioGroup>
            <Radio
              label="Read only — the agent can look things up but never change or create files"
              name="access-level"
              checked={accessLevel === 'read_only'}
              onChange={() => setAccessLevel('read_only')}
            />
            <Radio
              label="Read &amp; write — the agent can create and edit files it has access to"
              name="access-level"
              checked={accessLevel === 'read_write'}
              onChange={() => setAccessLevel('read_write')}
            />
            <Radio
              label="Full access — the agent can also run code and delegate to every specialist"
              name="access-level"
              checked={accessLevel === 'full_access'}
              onChange={() => setAccessLevel('full_access')}
            />
          </RadioGroup>
        </section>

        <HorizontalSeparator />

        <section className="access-settings__section">
          <h3 className="access-settings__heading">Local file search root</h3>
          <p className="access-settings__hint">
            The folder the local-files specialist is allowed to search and read from. Changing this
            here does not take effect yet — it currently requires setting{' '}
            <code>LOCAL_FILES_ROOT</code> on the backend.
          </p>
          <div className="access-settings__root-folder">
            <Input
              label="Root folder"
              value={localFilesRoot}
              onChange={(e) => setLocalFilesRoot(e.target.value)}
            />
            <Button variant="secondary" color="neutral" disabled>
              Save
            </Button>
          </div>
        </section>

        <HorizontalSeparator />

        <section className="access-settings__section">
          <div className="access-settings__section-header">
            <h3 className="access-settings__heading">Agent specializations</h3>
            <Tooltip content="Browse and add more specializations from a store — coming soon">
              <span>
                <Button
                  variant="tertiary"
                  color="neutral"
                  size="small"
                  icon={<Icon name="add" size={IconSize.SMALL} />}
                  disabled
                >
                  Add community tools
                </Button>
              </span>
            </Tooltip>
          </div>
          <p className="access-settings__hint">
            Specialists the agent can currently delegate to. Hover a row to disable it for this
            user.
          </p>

          {isLoadingSpecializations ? <p className="access-settings__hint">Loading…</p> : null}
          {specializationsError ? (
            <p className="access-settings__error">
              Could not reach the backend: {specializationsError}
            </p>
          ) : null}

          <ul className="specialization-list">
            {specializations.map((spec) => (
              <li key={spec.id} className="specialization-row" data-enabled={spec.enabled}>
                <div className="specialization-row__icon">
                  <Icon name="smart_toy" size={IconSize.SMALL} />
                </div>
                <div className="specialization-row__text">
                  <div className="specialization-row__title">{spec.name}</div>
                  <div className="specialization-row__subtitle">{spec.description}</div>
                  <div className="specialization-row__tools">
                    {spec.tools.map((tool) => (
                      <span
                        key={tool.name}
                        className="specialization-row__tool"
                        title={tool.description}
                      >
                        {tool.name}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="specialization-row__action">
                  <Switch
                    label={spec.enabled ? 'Enabled' : 'Disabled'}
                    checked={spec.enabled}
                    onChange={() => toggleSpecialization(spec.id)}
                  />
                </div>
              </li>
            ))}
          </ul>
        </section>

        <HorizontalSeparator />

        <section className="access-settings__section">
          <div className="access-settings__section-header">
            <h3 className="access-settings__heading">Coming soon</h3>
            <Badge type="info">Preview</Badge>
          </div>
          <p className="access-settings__hint">
            Specializations on the roadmap. They&apos;re shown here for preview only — nothing is
            wired up on the backend yet.
          </p>

          <ul className="specialization-list">
            {TEASER_SPECIALIZATIONS.map((spec) => (
              <li key={spec.id} className="specialization-row" data-enabled="false" data-teaser>
                <div className="specialization-row__icon">
                  <Icon name="smart_toy" size={IconSize.SMALL} />
                </div>
                <div className="specialization-row__text">
                  <div className="specialization-row__title">
                    {spec.name} <Badge type="neutral">Coming soon</Badge>
                  </div>
                  <div className="specialization-row__subtitle">{spec.description}</div>
                  <div className="specialization-row__tools">
                    {spec.tools.map((tool) => (
                      <span
                        key={tool.name}
                        className="specialization-row__tool"
                        title={tool.description}
                      >
                        {tool.name}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="specialization-row__action">
                  <Tooltip content="Not available yet">
                    <span>
                      <Switch label="Disabled" checked={false} disabled onChange={() => {}} />
                    </span>
                  </Tooltip>
                </div>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </Modal>
  )
}

export default AccessSettingsModal
