# CodeScale Research Radar - Execution Plan

## Executive Summary

**Goal:** Build a Signal vs Noise classification dashboard for engineering teams to separate technically substantive tools from marketing hype.

**Architecture:** `Grok (Discovery + Classification) → SQLite → FastAPI → SAP UI5 Dashboard`

**Development Model:** Parallel Claude agents working on isolated git worktrees.

---

## Current Status

### Phase 1 Issues (Ready to Start)

| Issue | Agent | Title | Status |
|-------|-------|-------|--------|
| #1 | Frontend Dev 1 | UI5 App Shell & Base Structure | Ready |
| #2 | Frontend Dev 2 | Voice AI Panel with Signal/Noise Display | Ready |
| #3 | Backend Dev 1 | FastAPI App & GET /api/radar Endpoint | Ready |
| #4 | Backend Dev 2 | SQLite Database & Models | Ready |
| #5 | Prompt Engineer | Grok Service & Voice AI Prompt | Ready |
| #6 | Problem Finder | Project Verification & Documentation | Ready |
| #13 | Orchestrator | Review, Merge PRs & Coordinate Development | Ready |
| #14 | DevOps | CI/CD Pipeline, Docker & Deployment Setup | Ready |

### Phase 2 Issues (Blocked by Phase 1)

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

| Agent | Worktree | Branch | Focus | Phase 1 | Phase 2 |
|-------|----------|--------|-------|---------|---------|
| Orchestrator | demo2 | main | PR merging, coordination | #13 | - |
| Frontend Dev 1 | demo2-fe1 | feature/frontend-dev-1 | UI5 components | #1 | #7 |
| Frontend Dev 2 | demo2-fe2 | feature/frontend-dev-2 | UI5 views/styling | #2 | #8 |
| Backend Dev 1 | demo2-be1 | feature/backend-dev-1 | API endpoints | #3 | #9 |
| Backend Dev 2 | demo2-be2 | feature/backend-dev-2 | Database/models | #4 | #10 |
| Prompt Engineer | demo2-prompt | feature/prompt-engineer | AI prompts | #5 | #11 |
| Problem Finder | demo2-qa | feature/problem-finder | Testing/QA | #6 | #12 |
| DevOps | demo2-devops | feature/devops | CI/CD pipeline | #14 | - |

---

## Project Structure

```
demo2/
├── webapp/                    # SAP UI5 Frontend
│   ├── Component.js           # Root component
│   ├── manifest.json          # App configuration
│   ├── index.html             # Entry point
│   ├── controller/            # View controllers
│   ├── view/                  # XML views
│   ├── model/                 # Formatters and models
│   ├── i18n/                  # Internationalization
│   ├── css/                   # Styles
│   └── localService/          # Mock data
├── backend/                   # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── database.py        # DB connection
│   │   ├── api/               # API routes
│   │   └── services/          # Business logic (Grok)
│   ├── tests/                 # Backend tests
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment template
├── prompts/                   # AI prompt templates
│   ├── voice_ai_prompt.md
│   ├── agent_orchestration_prompt.md
│   └── durable_runtime_prompt.md
├── .github/workflows/         # CI/CD (DevOps)
├── package.json               # npm configuration
├── ui5.yaml                   # UI5 tooling config
├── .mcp.json                  # Playwright MCP config
├── PRD.md                     # Product requirements
├── PLAN.md                    # This file
├── TASKS.md                   # Task distribution
├── CHANGELOG.md               # Change log
└── CLAUDE.md                  # Agent instructions
```

---

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | SAP UI5 | 1.120+ |
| Backend | FastAPI | 0.109+ |
| Database | SQLite | 3.x |
| AI | LiteLLM + xAI/Grok | Latest |
| Testing | Playwright MCP | Latest |
| CI/CD | GitHub Actions | - |
| Python Env | uv | Latest |

---

## Golden Contract (API Schema)

All components communicate using this JSON schema:

```json
{
  "radar_date": "2026-01-30",
  "trends": [
    {
      "focus_area": "voice_ai_ux",
      "tool_name": "LiveKit Agents",
      "classification": "signal",
      "confidence_score": 92,
      "technical_insight": "Sub-200ms voice-to-voice latency...",
      "signal_evidence": ["Published benchmarks", "Production case studies"],
      "noise_indicators": [],
      "architectural_verdict": true,
      "timestamp": "2026-01-30T08:00:00Z"
    }
  ]
}
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/radar | Returns latest radar analysis |
| GET | /api/radar?date=YYYY-MM-DD | Returns historical data |
| POST | /api/radar/refresh | Triggers new Grok analysis |

---

## Database Schema

```sql
CREATE TABLE trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    radar_date TEXT NOT NULL,
    focus_area TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    classification TEXT NOT NULL CHECK(classification IN ('signal', 'noise')),
    confidence_score INTEGER NOT NULL,
    technical_insight TEXT NOT NULL,
    signal_evidence TEXT,
    noise_indicators TEXT,
    architectural_verdict INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    UNIQUE(radar_date, focus_area, tool_name)
);
```

---

## Focus Areas

| Area | Signal Indicators | Noise Indicators |
|------|-------------------|------------------|
| Voice AI UX | Latency benchmarks, VAD specs | "Revolutionary AI", no data |
| Agent Orchestration | State persistence, tool chaining | "Autonomous agents", hype |
| Durable Runtime | SLAs, cold-start benchmarks | "Infinite scale", no details |

---

## Verification Plan

### Frontend Verification
```bash
npm install
npm start           # Opens localhost:8080
npm run lint        # 0 errors
```

### Backend Verification
```bash
cd backend
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
pytest              # All tests pass
uvicorn app.main:app --reload
curl http://localhost:8000/api/radar
```

### UI Testing (Playwright MCP)
- Use Playwright MCP for all UI testing
- Take screenshots for verification
- Test user flows end-to-end

### Integration Verification
1. Start backend on port 8000
2. Start frontend on port 8080
3. Verify API calls in Network tab
4. Test manual refresh flow

---

## Success Criteria

| Track | Criterion | Status |
|-------|-----------|--------|
| Frontend | 3 cards render with signal/noise distinction | ☐ |
| Frontend | Green badges for signal, gray for noise | ☐ |
| Backend | /api/radar returns valid JSON in <200ms | ☐ |
| Backend | Historical data queryable by date | ☐ |
| AI | Signal classifications include evidence | ☐ |
| AI | Noise classifications identify hype patterns | ☐ |
| Integration | End-to-end: Grok → DB → API → UI | ☐ |
| DevOps | CI/CD pipeline runs on PR | ☐ |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Frontend blocked by backend | Use mock data (provided) |
| Grok API fails | Use cached example response |
| Schema changes | Golden Contract prevents this |
| Merge conflicts | Git worktrees isolate work |
| Agent coordination | Orchestrator manages PRs |

---

## Starting the Agents

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

## Decisions Made

- Parallel agent development with git worktrees
- One task at a time per agent
- Squash merge for all PRs
- Playwright MCP for UI testing
- xAI/Grok via LiteLLM for AI provider
- Daily batch refresh (not 30-minute)
- **uv for Python environment management** (not venv/pip)
- **Mandatory testing before commits**
- **PR required for every task**
