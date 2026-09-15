# auto

An Electron application with React and TypeScript

## Recommended IDE Setup

- [VSCode](https://code.visualstudio.com/) + [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) + [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)

## Project Setup

### Install

```bash
$ export PATH="$PWD/.node/bin:$PATH"  # project-local Node.js/npm
$ npm install
```

### Development

```bash
$ cp .env.example .env
$ npm run dev
```

The renderer sends chat history as a JSON `POST` to
`VITE_BACKEND_URL/api/chat`. Start the backend on port 8000 before launching
Electron. The default backend URL is `http://127.0.0.1:8000`.

### Build

```bash
# For windows
$ npm run build:win

# For macOS
$ npm run build:mac

# For Linux
$ npm run build:linux
```
