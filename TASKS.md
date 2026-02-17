# Task Distribution for Parallel Development

## Objective
Distribute tasks across parallel Claude agents working on isolated git worktrees.

---

## Current Open Issues

| Issue | Agent | Title | Labels |
|-------|-------|-------|--------|
| #18 | Frontend Dev 1 | UI5 App Shell & Base Structure | track-a, ready |
| #19 | Frontend Dev 2 | Voice AI Panel Component | track-a, ready |
| #20 | Backend Dev 1 | FastAPI App & GET /api/radar Endpoint | track-b, ready |

---

## Completed Issues (Historical)

| Issue | Title | Status |
|-------|-------|--------|
| #1 | [Track A] Set up SAPUI5 project structure | CLOSED |
| #2 | [Track A] Implement RadarView with 3 focus area cards | CLOSED |
| #3 | [Track A] Add mock data and JSON model binding | CLOSED |
| #4 | [Track B] Set up FastAPI project structure | CLOSED |
| #5 | [Track B] Implement /api/radar endpoints | CLOSED |
| #6 | [Track B] Integrate LiteLLM with xAI/Grok | CLOSED |
| #7 | [Track C] Create Voice AI prompt template | CLOSED |
| #8 | [Track C] Create Agent Orchestration prompt template | CLOSED |
| #9 | [Track C] Create Durable Runtime prompt template | CLOSED |

---

## Agent Structure

| Agent | Worktree | Branch | Focus | Current Issue |
|-------|----------|--------|-------|---------------|
| **Orchestrator** | demo2 | main | PR merging, coordination | - |
| **Frontend Dev 1** | demo2-fe1 | feature/frontend-dev-1 | UI5 components | #18 |
| **Frontend Dev 2** | demo2-fe2 | feature/frontend-dev-2 | UI5 views/styling | #19 |
| **Backend Dev 1** | demo2-be1 | feature/backend-dev-1 | API endpoints | #20 |
| **Backend Dev 2** | demo2-be2 | feature/backend-dev-2 | Database/models | - |
| **Prompt Engineer** | demo2-prompt | feature/prompt-engineer | AI prompts | - |
| **Problem Finder (QA)** | demo2-qa | feature/problem-finder | Testing/QA | - |
| **DevOps** | demo2-devops | feature/devops | CI/CD pipeline | - |

---

## Issue Details

### #18 - [Frontend Dev 1] UI5 App Shell & Base Structure

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

### #19 - [Frontend Dev 2] Voice AI Panel Component

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

### #20 - [Backend Dev 1] FastAPI App & GET /api/radar Endpoint

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
- Current: Issue #18 - UI5 App Shell & Base Structure

### Frontend Dev 2
**Stack:** SAP UI5 1.120+, XML views, CSS
**Files:** `webapp/view/*`, `webapp/css/*`, `webapp/i18n/*`
- Current: Issue #19 - Voice AI Panel Component

### Backend Dev 1
**Stack:** Python 3.11+, FastAPI
**Files:** `backend/app/api/*`, `backend/app/services/*`
- Current: Issue #20 - FastAPI App & GET /api/radar Endpoint

### Backend Dev 2
**Stack:** Python 3.11+, SQLAlchemy, SQLite
**Files:** `backend/app/models.py`, `backend/app/database.py`
- Waiting for new issues

### Prompt Engineer
**Stack:** Grok prompts, JSON schema
**Files:** `prompts/*`
- Waiting for new issues

### Problem Finder (QA)
**Focus:** Testing, bug discovery, code review
- Waiting for new issues

### DevOps Agent
**Stack:** GitHub Actions, Docker
**Files:** `.github/workflows/*`, `Dockerfile`, `docker-compose.yml`
- Waiting for new issues

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
