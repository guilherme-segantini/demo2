# Task Distribution for Parallel Development

## Objective
Distribute tasks across parallel Claude agents working on isolated git worktrees.

---

## Current Open Issues

### Phase 1 (Ready to Start)

| Issue | Agent | Title | Labels |
|-------|-------|-------|--------|
| #1 | Frontend Dev 1 | UI5 App Shell & Base Structure | track-a, ready |
| #2 | Frontend Dev 2 | Voice AI Panel with Signal/Noise Display | track-a, ready |
| #3 | Backend Dev 1 | FastAPI App & GET /api/radar Endpoint | track-b, ready |
| #4 | Backend Dev 2 | SQLite Database & Models | track-b, ready |
| #5 | Prompt Engineer | Grok Service & Voice AI Prompt | track-c, ready |
| #6 | Problem Finder | Project Verification & Documentation | qa, ready |
| #13 | Orchestrator | Review, Merge PRs & Coordinate Development | integration, ready |
| #14 | DevOps | CI/CD Pipeline, Docker & Deployment Setup | ready |

### Phase 2 (After Phase 1 Completes)

| Issue | Agent | Title | Blocked By |
|-------|-------|-------|------------|
| #7 | Frontend Dev 1 | Agent Orchestration Panel | #1 |
| #8 | Frontend Dev 2 | Durable Runtime Panel | #2 |
| #9 | Backend Dev 1 | POST /api/radar/refresh Endpoint | #3, #5 |
| #10 | Backend Dev 2 | Database Query Functions & Historical Data | #4 |
| #11 | Prompt Engineer | Agent Orchestration & Durable Runtime Prompts | #5 |
| #12 | Problem Finder | Integration Testing & Bug Fixes | #6 |

---

## Agent Structure

| Agent | Worktree | Branch | Focus | Phase 1 Issue | Phase 2 Issue |
|-------|----------|--------|-------|---------------|---------------|
| **Orchestrator** | demo2 | main | PR merging, coordination | #13 | - |
| **Frontend Dev 1** | demo2-fe1 | feature/frontend-dev-1 | UI5 components | #1 | #7 |
| **Frontend Dev 2** | demo2-fe2 | feature/frontend-dev-2 | UI5 views/styling | #2 | #8 |
| **Backend Dev 1** | demo2-be1 | feature/backend-dev-1 | API endpoints | #3 | #9 |
| **Backend Dev 2** | demo2-be2 | feature/backend-dev-2 | Database/models | #4 | #10 |
| **Prompt Engineer** | demo2-prompt | feature/prompt-engineer | AI prompts | #5 | #11 |
| **Problem Finder** | demo2-qa | feature/problem-finder | Testing/QA | #6 | #12 |
| **DevOps** | demo2-devops | feature/devops | CI/CD pipeline | #14 | - |

---

## Issue Details

### #1 - [Frontend Dev 1] UI5 App Shell & Base Structure

**Agent:** Frontend Dev 1
**Labels:** track-a, ready

**Description:**
Create the foundational UI5 application structure including Component.js, manifest.json, index.html, and base configuration.

**Acceptance Criteria:**
- [ ] `webapp/Component.js` - Root UI5 component
- [ ] `webapp/manifest.json` - App configuration with routing
- [ ] `webapp/index.html` - Entry point with async loading
- [ ] `webapp/view/App.view.xml` - App shell view
- [ ] `webapp/controller/BaseController.js` - Shared controller utilities
- [ ] `package.json` - npm scripts (start, build, lint)
- [ ] `ui5.yaml` - UI5 tooling configuration
- [ ] App loads without errors at localhost:8080
- [ ] `npm run lint` passes with 0 errors

**Test Verification:**
```bash
npm install && npm start
# Browser opens at localhost:8080, app shell renders
npm run lint  # 0 errors
```

---

### #2 - [Frontend Dev 2] Voice AI Panel with Signal/Noise Display

**Agent:** Frontend Dev 2
**Labels:** track-a, ready

**Description:**
Create the Voice AI panel component for the RadarView, displaying signal and noise items with proper styling.

**Acceptance Criteria:**
- [ ] `webapp/view/RadarView.view.xml` - Voice AI panel section
- [ ] `webapp/controller/RadarView.controller.js` - Panel controller logic
- [ ] `webapp/model/mock_radar.json` - Mock data from PRD
- [ ] `webapp/model/formatter.js` - Signal/noise formatting
- [ ] `webapp/i18n/i18n.properties` - Voice AI translations
- [ ] `webapp/css/style.css` - Signal (green) and noise (gray) styling
- [ ] Panel displays Voice AI items from mock data
- [ ] Signal items show green badge with evidence list
- [ ] Noise items show gray badge with noise indicators
- [ ] Confidence score displays correctly

**Test Verification:**
```bash
npm start
# Voice AI panel renders with 2 items (LiveKit Agents, VoiceHype AI)
# Signal item has green styling, noise item has gray styling
```

---

### #3 - [Backend Dev 1] FastAPI App & GET /api/radar Endpoint

**Agent:** Backend Dev 1
**Labels:** track-b, ready

**Description:**
Create the FastAPI application with the GET /api/radar endpoint that returns radar data from SQLite.

**Acceptance Criteria:**
- [ ] `backend/app/__init__.py` - Package init
- [ ] `backend/app/main.py` - FastAPI app with CORS middleware
- [ ] `backend/app/api/__init__.py` - API package init
- [ ] `backend/app/api/radar.py` - GET /api/radar endpoint
- [ ] `backend/requirements.txt` - Python dependencies
- [ ] `backend/.env.example` - Environment template
- [ ] GET /api/radar returns JSON matching Golden Contract schema
- [ ] GET /api/radar?date=YYYY-MM-DD filters by date
- [ ] Response time <200ms
- [ ] CORS allows localhost:8080

**Test Verification:**
```bash
cd backend
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload
curl http://localhost:8000/api/radar  # Returns JSON
curl http://localhost:8000/api/radar?date=2026-01-30  # Filtered
```

---

### #4 - [Backend Dev 2] SQLite Database & Models

**Agent:** Backend Dev 2
**Labels:** track-b, ready

**Description:**
Create SQLite database setup, SQLAlchemy models, and database connection utilities.

**Acceptance Criteria:**
- [ ] `backend/app/database.py` - Database connection and session management
- [ ] `backend/app/models.py` - SQLAlchemy Trend model
- [ ] Database schema matches Golden Contract
- [ ] Initial migration/table creation
- [ ] Unit tests for models

**Test Verification:**
```bash
cd backend
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
pytest tests/test_models.py
```

---

### #5 - [Prompt Engineer] Grok Service & Voice AI Prompt

**Agent:** Prompt Engineer
**Labels:** track-c, ready

**Description:**
Create the Grok service integration and Voice AI prompt template.

**Acceptance Criteria:**
- [ ] `backend/app/services/grok_service.py` - LiteLLM integration with xAI/Grok
- [ ] `prompts/voice_ai_prompt.md` - Voice AI discovery + classification prompt
- [ ] Prompt returns JSON matching Golden Contract schema
- [ ] Signal/noise criteria properly defined

**Test Verification:**
```bash
cd backend
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
pytest tests/test_grok_service.py
```

---

### #6 - [Problem Finder] Project Verification & Documentation

**Agent:** Problem Finder
**Labels:** qa, ready

**Description:**
Verify project setup, test all components, and document any issues.

**Acceptance Criteria:**
- [ ] Frontend runs without errors
- [ ] Backend runs without errors
- [ ] All linters pass
- [ ] Document any bugs or issues found
- [ ] Create bug issues for any problems

---

### #13 - [Orchestrator] Review, Merge PRs & Coordinate Development

**Agent:** Orchestrator
**Labels:** integration, ready

**Description:**
Monitor and merge PRs from all agents, coordinate cross-agent dependencies.

**Responsibilities:**
- [ ] Monitor PR status across all agents
- [ ] Review and merge PRs (squash merge)
- [ ] Resolve merge conflicts
- [ ] Coordinate cross-agent dependencies
- [ ] Keep main branch stable

---

### #14 - [DevOps] CI/CD Pipeline, Docker & Deployment Setup

**Agent:** DevOps
**Labels:** ready

**Description:**
Set up CI/CD pipeline, Docker configuration, and deployment automation.

**Acceptance Criteria:**
- [ ] `.github/workflows/ci.yml` - CI pipeline (lint, test)
- [ ] `Dockerfile` - Backend container
- [ ] `docker-compose.yml` - Full stack setup
- [ ] Pipeline runs on PR

---

## Agent Responsibilities

### Orchestrator Agent
- Monitor PR status across all agents
- Merge PRs when ready (squash merge)
- Resolve merge conflicts if needed
- Coordinate cross-agent dependencies
- Keep main branch stable

### Frontend Dev 1
**Stack:** SAP UI5 1.120+, JavaScript ES6+
**Files:** `webapp/Component.js`, `webapp/controller/*`, `webapp/model/*`
- Phase 1: Issue #1 - UI5 App Shell & Base Structure
- Phase 2: Issue #7 - Agent Orchestration Panel

### Frontend Dev 2
**Stack:** SAP UI5 1.120+, XML views, CSS
**Files:** `webapp/view/*`, `webapp/css/*`, `webapp/i18n/*`
- Phase 1: Issue #2 - Voice AI Panel with Signal/Noise Display
- Phase 2: Issue #8 - Durable Runtime Panel

### Backend Dev 1
**Stack:** Python 3.11+, FastAPI
**Files:** `backend/app/api/*`, `backend/app/services/*`
- Phase 1: Issue #3 - FastAPI App & GET /api/radar Endpoint
- Phase 2: Issue #9 - POST /api/radar/refresh Endpoint

### Backend Dev 2
**Stack:** Python 3.11+, SQLAlchemy, SQLite
**Files:** `backend/app/models.py`, `backend/app/database.py`
- Phase 1: Issue #4 - SQLite Database & Models
- Phase 2: Issue #10 - Database Query Functions & Historical Data

### Prompt Engineer
**Stack:** Grok prompts, JSON schema
**Files:** `prompts/*`, `backend/app/services/grok_service.py`
- Phase 1: Issue #5 - Grok Service & Voice AI Prompt
- Phase 2: Issue #11 - Agent Orchestration & Durable Runtime Prompts

### Problem Finder (QA)
**Focus:** Testing, bug discovery, code review
- Phase 1: Issue #6 - Project Verification & Documentation
- Phase 2: Issue #12 - Integration Testing & Bug Fixes

### DevOps Agent
**Stack:** GitHub Actions, Docker
**Files:** `.github/workflows/*`, `Dockerfile`, `docker-compose.yml`
- Phase 1: Issue #14 - CI/CD Pipeline, Docker & Deployment Setup

---

## Starting an Agent

Each agent runs in its own terminal:

```bash
# Orchestrator
cd /Users/I769068/projects/scaling-productivity/demo2 && claude

# Frontend Dev 1
cd /Users/I769068/projects/scaling-productivity/demo2-fe1 && claude

# Frontend Dev 2
cd /Users/I769068/projects/scaling-productivity/demo2-fe2 && claude

# Backend Dev 1
cd /Users/I769068/projects/scaling-productivity/demo2-be1 && claude

# Backend Dev 2
cd /Users/I769068/projects/scaling-productivity/demo2-be2 && claude

# Prompt Engineer
cd /Users/I769068/projects/scaling-productivity/demo2-prompt && claude

# Problem Finder (QA)
cd /Users/I769068/projects/scaling-productivity/demo2-qa && claude

# DevOps
cd /Users/I769068/projects/scaling-productivity/demo2-devops && claude
```

---

## Workflow Rules

1. **One issue at a time** - Complete full cycle before starting next
2. **Test before commit** - Run linters and tests (MANDATORY)
3. **Use Playwright MCP** - For all UI testing
4. **Update CHANGELOG.md** - Document changes
5. **Squash merge PRs** - Keep history clean
6. **Sync before starting** - `git fetch origin main && git rebase origin/main`
7. **Use uv only** - Never use pip/venv directly

---

## Verification Checklist

Before marking any issue complete:
- [ ] App runs without console errors
- [ ] `npm run lint` passes (frontend)
- [ ] `pytest` passes (backend)
- [ ] UI tested with Playwright MCP
- [ ] i18n used for all text
- [ ] No hardcoded URLs or secrets
- [ ] CHANGELOG.md updated
- [ ] PR created and merged
