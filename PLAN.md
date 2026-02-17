# CodeScale Research Radar - Execution Plan

## Executive Summary

**Goal:** Build a Signal vs Noise classification dashboard for engineering teams to separate technically substantive tools from marketing hype.

**Architecture:** `Grok (Discovery + Classification) → SQLite → FastAPI → SAP UI5 Dashboard`

**Development Model:** Parallel Claude agents working on isolated git worktrees.

---

## Current Status

### Open Issues

| Issue | Agent | Title | Status |
|-------|-------|-------|--------|
| #18 | Frontend Dev 1 | UI5 App Shell & Base Structure | Ready |
| #19 | Frontend Dev 2 | Voice AI Panel Component | Ready |
| #20 | Backend Dev 1 | FastAPI App & GET /api/radar Endpoint | Ready |

### Completed Issues

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
| Orchestrator | demo2 | main | PR merging, coordination | - |
| Frontend Dev 1 | demo2-fe1 | feature/frontend-dev-1 | UI5 components | #18 |
| Frontend Dev 2 | demo2-fe2 | feature/frontend-dev-2 | UI5 views/styling | #19 |
| Backend Dev 1 | demo2-be1 | feature/backend-dev-1 | API endpoints | #20 |
| Backend Dev 2 | demo2-be2 | feature/backend-dev-2 | Database/models | - |
| Prompt Engineer | demo2-prompt | feature/prompt-engineer | AI prompts | - |
| Problem Finder | demo2-qa | feature/problem-finder | Testing/QA | - |
| DevOps | demo2-devops | feature/devops | CI/CD pipeline | - |

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
| AI | LiteLLM + SAP GenAI Hub | Latest |
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
- SAP Generative AI Hub via LiteLLM (not direct Grok)
- Daily batch refresh (not 30-minute)
- **uv for Python environment management** (not venv/pip)
- **Mandatory testing before commits**
- **PR required for every task**
