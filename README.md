# Todo App

This repository is a demo Todo application. It contains a backend API built with NestJS (`todo-be/`) and a frontend built with Next.js (`todo-fe/`).

This README provides instructions for local setup, development, testing, and troubleshooting.

Main sections:
- Project overview (backend + frontend)
- Quick start (install, env, run)
- Development guide (run both services, debug, test)
- Extras (linting, deployment notes, common issues)

## Prerequisites

- Node.js 20+ (use the latest LTS if possible)
- pnpm
- MongoDB (**remote** or local)

macOS example (install helpers):

```bash
# Install pnpm if you don't have it
npm install -g pnpm
```

## Install dependencies

Install dependencies per project. From the repository root run:

```bash
# Backend
cd todo-be
pnpm install
```

```bash
# In a new terminal, Frontend
cd todo-fe
pnpm install
```

## Environment variables


The backend needs a MongoDB connection string. Create a `.env` file inside `todo-be/` (or provide environment variables in your preferred way):

```
MONGODB_URI=mongodb://localhost:27017/todo-dev
PORT=3001
```

## Run (development)


Run backend and frontend in separate terminals.

- Start the backend (NestJS):

```bash
cd todo-be
pnpm install # if not already installed
pnpm start:dev
```

- Start the frontend (Next.js):

```bash
cd todo-fe
pnpm install # if not already installed
pnpm dev
```

Open the frontend in a browser (typically `http://localhost:3001`). The frontend will call the backend API (default `http://localhost:3000`), so ensure the backend is running and connected to MongoDB.

## Run (production)

Run scripts inside each project directory (check each `package.json` for exact script names):

- Backend (`todo-be`):
	- `pnpm build` — build backend
	- `pnpm start:prod` — run built backend

- Frontend (`todo-fe`):
	- `pnpm build` — build frontend
	- `pnpm start` — run built frontend

Open the frontend in a browser (`http://localhost:3002`). The frontend will call the backend API (default `http://localhost:3000`), so ensure the backend is running and connected to MongoDB.


## Testing & quality

- Backend unit tests (Jest):

```bash
cd todo-be
pnpm test
```

- Backend e2e test (Supertest):

```bash
pnpm test
```

- Frontend tests (Vitest):

```bash
cd todo-fe
pnpm test
```


## Project structure (high-level)

- `todo-be/` — NestJS backend
	- `src/` — source code
	- `src/todos/` — todo module, DTOs, schemas
	- tests in `test/` or `src/**/*.spec.ts`

- `todo-fe/` — Next.js frontend
	- `app/` — Next App Router
	- `components/` — reusable components
	- `__tests__/` — frontend tests
