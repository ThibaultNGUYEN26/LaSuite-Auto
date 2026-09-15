import '@gouvfr-lasuite/ui-kit/style'
import '@gouvfr-lasuite/ui-kit/fonts/Marianne'
import { CunninghamProvider } from '@gouvfr-lasuite/ui-kit'

function App(): React.JSX.Element {
  const ipcHandle = (): void => window.electron.ipcRenderer.send('ping')

  return (
    <CunninghamProvider theme="dsfr-light">
      <main style={{ padding: 'var(--c--globals--spacings--lg)' }}>
        <h1>Auto says hi</h1>
      </main>
    </CunninghamProvider>
  )
}

export default App
