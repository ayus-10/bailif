# Client (Vue 3 + Vite — web now, desktop later via Tauri if wanted)

## Setup

```bash
npm install
cp .env.example .env
```

## Run (dev server, hot reload)

```bash
npm run dev
```

Opens at http://localhost:5173 by default. Make sure your FastAPI
backend is running (see ../server/README.md) and reachable at whatever
`VITE_API_BASE_URL` points to in `.env`.

## Build for production (deployable demo)

```bash
npm run build
```

Output lands in `dist/` — a plain static site. Host it anywhere
(S3 + CloudFront, Netlify, Vercel, GitHub Pages) to satisfy the
"functional demo app URL" requirement.

## Desktop later

If you ever want a desktop build without switching frameworks again,
this same Vue/Vite frontend can be wrapped with Tauri (Rust) later —
Tauri just points at your existing `dist/` build, no rewrite needed.
Not set up yet; mentioning it since it was part of the original plan.

## Structure

- `src/services/api.js` — all HTTP + SSE calls live here (single choke point)
- `src/components/AgentBar.vue` — natural language query input + streamed agent response
- `src/components/TaskCard.vue` — single task display
- `src/App.vue` — ties it together: task list + agent bar
