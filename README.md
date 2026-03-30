<div align="center">

# Todo App

**A full-stack Todo application with NestJS backend and Next.js frontend**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Backend](https://img.shields.io/badge/backend-v0.0.9-green.svg)
![Frontend](https://img.shields.io/badge/frontend-v0.1.7-green.svg)

[Features](#features) • [Quick Start](#quick-start) • [Development](#run-development) • [Testing](#testing--quality) • [CI/CD Pipeline](#cicd-pipeline)

</div>

---

## Overview

This is a demo Todo application showcasing a modern full-stack architecture:

- **Backend** (`todo-be/`): RESTful API built with NestJS, MongoDB, and Swagger documentation
- **Frontend** (`todo-fe/`): Responsive UI built with Next.js 16, React 19, Ant Design, and TanStack Query

## Features

✅ Create, read, update, and delete todos
✅ RESTful API with Swagger documentation
✅ MongoDB integration with Mongoose
✅ Modern React UI with Ant Design components
✅ Server-side rendering with Next.js App Router
✅ API health checks and monitoring
✅ Comprehensive test coverage (Jest + Vitest)
✅ TypeScript throughout for type safety

## Tech Stack

### Backend
- **Framework**: NestJS 11
- **Database**: MongoDB with Mongoose
- **API Documentation**: Swagger/OpenAPI
- **Testing**: Jest, Supertest
- **Validation**: class-validator, class-transformer

### Frontend
- **Framework**: Next.js 16 (App Router)
- **UI Library**: Ant Design 6
- **State Management**: TanStack Query (React Query)
- **Styling**: Tailwind CSS 4
- **Testing**: Vitest, Testing Library

## Quick Start

### Prerequisites

- Node.js 20+ (use the latest LTS if possible)
- pnpm
- MongoDB (**remote** or local)

macOS example (install helpers):

```bash
# Install pnpm if you don't have it
npm install -g pnpm
```

### Install dependencies

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

### Environment variables


The backend needs a MongoDB connection string. Create a `.env` file inside `todo-be/` (or provide environment variables in your preferred way):

```
MONGO_URI=<your connection string>
```

## Run (development)

### Start both services


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

Open the frontend in a browser at **http://localhost:3001**. The frontend will call the backend API at **http://localhost:3000**, so ensure the backend is running and connected to MongoDB.

**API Documentation**: Once the backend is running, visit **http://localhost:3000/api** for interactive Swagger documentation.

## Run (production)

### Build and run for production

**Backend** (`todo-be`):
```bash
cd todo-be
pnpm build
pnpm start:prod
```

**Frontend** (`todo-fe`):
```bash
cd todo-fe
pnpm build
pnpm start
```

The production frontend runs on **http://localhost:3002**. Ensure the backend is running on **http://localhost:3000** and connected to MongoDB.

## Testing & quality

### Backend tests (Jest)

```bash
cd todo-be
pnpm test              # Run unit tests
pnpm test:watch        # Watch mode
pnpm test:cov          # With coverage
pnpm test:e2e          # End-to-end tests
```

### Frontend tests (Vitest)

```bash
cd todo-fe
pnpm test              # Run tests
pnpm test:watch        # Watch mode
```

### Code quality

```bash
# Backend linting & formatting
cd todo-be
pnpm lint              # ESLint
pnpm format            # Prettier

# Frontend linting
cd todo-fe
pnpm lint              # ESLint
```


## CI/CD Pipeline

The project uses **GitHub Actions** for automated continuous integration and deployment.

### Backend CI/CD ([`.github/workflows/backend.yml`](.github/workflows/backend.yml))

**Trigger Conditions:**
- Push to `main` or `master` branch with changes in `todo-be/**`
- Pull requests affecting `todo-be/**`
- Manual trigger via `workflow_dispatch`

**Pipeline Steps:**
1. **Setup Environment** - Node.js 24, pnpm 9, checkout code
2. **Install Dependencies** - `pnpm install --frozen-lockfile`
3. **Lint** - ESLint validation for code quality
4. **Type Check** - TypeScript compilation check
5. **Unit Tests** - Jest unit tests
6. **E2E Tests** - Jest e2e tests with supertest
7. **Build** - Production build
8. **Version Bump** - Auto-increment patch version on main branch
9. **Deploy to VPS** - Deploy via SSH using PM2 process manager

**Deployment Details:**
- Uses `appleboy/ssh-action` to connect to VPS
- Pulls latest code and rebuilds on server
- Manages NestJS process with PM2 (auto-restart on failure)
- Zero-downtime deployment with `pm2 restart`

**Required Secrets:**
```
VPS_HOST         - Your VPS hostname/IP
VPS_USER         - SSH username
VPS_PRIVATE_KEY  - SSH private key for authentication
VPS_PORT         - SSH port (usually 22)
```

### Frontend CI/CD ([`.github/workflows/frontend.yml`](.github/workflows/frontend.yml))

**Trigger Conditions:**
- Push to `main` or `master` branch with changes in `todo-fe/**`
- Pull requests affecting `todo-fe/**`
- Manual trigger via `workflow_dispatch`

**Pipeline Steps:**
1. **Setup Environment** - Node.js 24, pnpm 9, checkout code
2. **Install Dependencies** - `pnpm install --frozen-lockfile`
3. **Lint** - ESLint validation
4. **Type Check** - TypeScript compilation check
5. **Test** - Vitest unit/integration tests
6. **Build** - Next.js production build
7. **Version Bump** - Auto-increment patch version on main branch

**Deployment:**
- Frontend is deployed to **Vercel** automatically via **Vercel Git Integration**
- Vercel monitors the GitHub repository and triggers deployment when:
  - Code is pushed to main branch (production deployment)
  - Pull requests are created (preview deployments)
- Deployment happens **after** version bump is committed by GitHub Actions
- No manual deployment configuration needed in GitHub Actions workflow

### CI/CD Features

- ✅ **Path-based triggers** - Only runs when relevant files change
- ✅ **Concurrency control** - Cancels outdated runs to save resources
- ✅ **Automated testing** - Every push/PR is validated
- ✅ **Type safety** - TypeScript validation in CI
- ✅ **Automatic versioning** - Patch version bump on main branch
- ✅ **Parallel execution** - Frontend and backend workflows run independently
- ✅ **Manual triggers** - Can be run manually via GitHub Actions UI

### Setting Up CI/CD

#### Backend Setup (VPS Deployment)

1. **Fork/clone** the repository to your GitHub account
2. **Add VPS secrets** to GitHub Settings → Secrets and variables → Actions:
   - `VPS_HOST` - Your VPS hostname or IP address
   - `VPS_USER` - SSH username for VPS access
   - `VPS_PRIVATE_KEY` - SSH private key for authentication
   - `VPS_PORT` - SSH port (usually 22)
3. **Ensure PM2 is installed** on your VPS: `npm install -g pm2`
4. **Clone the repository** on your VPS in `~/todo`
5. **Push to main** to trigger the deployment

#### Frontend Setup (Vercel Deployment)

1. **Create a Vercel account** at https://vercel.com
2. **Import your project** to Vercel:
   - Go to Vercel Dashboard → Add New Project
   - Import your GitHub repository
   - Set root directory to `todo-fe`
   - Configure build settings (auto-detected for Next.js)
3. **Configure environment variables** in Vercel Dashboard:
   - `NEXT_PUBLIC_API_URL` - Your backend API URL (e.g., https://api.yourdomain.com)
4. **Enable Git Integration** (enabled by default):
   - Vercel will automatically monitor the repository
   - Deployments triggered on push to main branch
   - Preview deployments created for pull requests
5. **Push to main** - GitHub Actions runs CI and bumps version, then Vercel auto-deploys

#### Testing the Workflows

- **Pull requests** will run tests and checks without deploying
  - Backend: No VPS deployment
  - Frontend: Vercel creates preview deployment automatically
- **Push to main** will run full pipeline:
  - Backend: Tests → Build → Version bump → Deploy to VPS
  - Frontend: Tests → Build → Version bump (then Vercel auto-deploys)
- **Manual trigger** via GitHub Actions tab for on-demand testing/deployment



## Project structure (high-level)

```
todo/
├── todo-be/              # NestJS backend
│   ├── src/
│   │   ├── main.ts       # Application entry point
│   │   ├── app.module.ts # Root module
│   │   └── todos/        # Todo module
│   │       ├── todos.controller.ts
│   │       ├── todos.service.ts
│   │       ├── todos.module.ts
│   │       ├── schemas/  # MongoDB schemas
│   │       └── dto/      # Data Transfer Objects
│   ├── test/             # E2E tests
│   └── src/**/*.spec.ts  # Unit tests
│
└── todo-fe/              # Next.js frontend
    ├── app/              # Next.js App Router
    │   ├── page.tsx      # Home page
    │   └── layout.tsx    # Root layout
    ├── components/       # React components
    └── __tests__/        # Frontend tests
```

## Architecture

```
┌─────────────┐      HTTP/REST      ┌─────────────┐      Mongoose      ┌─────────────┐
│   Next.js   │ ──────────────────> │   NestJS    │ ─────────────────> │   MongoDB   │
│  Frontend   │ <────────────────── │   Backend   │ <───────────────── │  Database   │
│ (Port 3001) │      JSON           │ (Port 3000) │     Documents      │             │
└─────────────┘                     └─────────────┘                    └─────────────┘
     │                                     │
     │                                     │
     └─── React Query                     └─── Swagger API Docs
          (State & Cache)                      (http://localhost:3000/api)
```

## API Documentation

The backend provides interactive API documentation via Swagger/OpenAPI:

- **Development**: http://localhost:3000/api
- **Production**: Configure based on your deployment

API features:
- Full CRUD operations for todos
- Health check endpoint (`/health`)
- Request/response validation
- Automatic API documentation

## Contributing

Contributions are welcome! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/my-feature`
3. **Make your changes** and ensure tests pass
4. **Commit your changes**: `git commit -m 'Add some feature'`
5. **Push to the branch**: `git push origin feature/my-feature`
6. **Open a Pull Request**

Please ensure your code:
- Passes all tests (`pnpm test`)
- Follows the existing code style (`pnpm lint`)
- Includes appropriate test coverage

## Troubleshooting

### Common issues

**MongoDB connection errors**
- Verify your `MONGO_URI` in `.env` is correct
- Ensure your MongoDB instance is running and accessible
- Check network connectivity and firewall settings

**Port already in use**
- Backend (3000): Change port in `todo-be/src/main.ts`
- Frontend dev (3001): Use `next dev -p <port>`
- Frontend prod (3002): Use `next start -p <port>`

**Module not found errors**
- Run `pnpm install` in the respective directory
- Delete `node_modules` and reinstall if issues persist

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using NestJS and Next.js**

[Report Bug](../../issues) • [Request Feature](../../issues)

</div>
