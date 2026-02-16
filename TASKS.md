# Task Distribution for 9-Agent Parallel Development

## Objective
Distribute tasks across 9 parallel Claude agents working on isolated git worktrees.

---

## Agent Structure (9 Agents)

| Agent | Worktree | Branch | Focus | Issues |
|-------|----------|--------|-------|--------|
| **Scaffolding** | demo2-scaffold | feature/scaffolding | Project foundation | #15 (COMPLETE) |
| **Orchestrator** | demo2 | main | PR merging, coordination | #13 |
| **Frontend Dev 1** | demo2-fe1 | feature/frontend-dev-1 | UI5 components | #1, #7 |
| **Frontend Dev 2** | demo2-fe2 | feature/frontend-dev-2 | UI5 views/styling | #2, #8 |
| **Backend Dev 1** | demo2-be1 | feature/backend-dev-1 | API endpoints | #3, #9 |
| **Backend Dev 2** | demo2-be2 | feature/backend-dev-2 | Database/models | #4, #10 |
| **Prompt Engineer** | demo2-prompt | feature/prompt-engineer | AI prompts | #5, #11 |
| **Problem Finder (QA)** | demo2-qa | feature/problem-finder | Testing/QA | #6, #12 |
| **DevOps** | demo2-devops | feature/devops | CI/CD pipeline | #14 |

---

## Execution Phases

### Phase 0: Scaffolding (COMPLETE)
- **Agent:** Scaffolding
- **Issue:** #15
- **Status:** ✅ Merged to main

### Phase 1: First Issues (Parallel)
All 8 remaining agents work on their first issue simultaneously:

| Agent | Issue | Title |
|-------|-------|-------|
| Orchestrator | #13 | Coordination and PR management |
| Frontend Dev 1 | #1 | UI5 project skeleton and Component.js |
| Frontend Dev 2 | #2 | RadarView layout and panels |
| Backend Dev 1 | #3 | FastAPI app and API endpoints |
| Backend Dev 2 | #4 | SQLite models and database setup |
| Prompt Engineer | #5 | Base prompt templates |
| Problem Finder | #6 | Initial QA review and test plan |
| DevOps | #14 | CI/CD pipeline setup |

### Phase 2: Second Issues (After Phase 1)
Agents complete second issues after dependencies merge:

| Agent | Issue | Title | Blocked By |
|-------|-------|-------|------------|
| Frontend Dev 1 | #7 | Signal/noise formatters and styling | #1 |
| Frontend Dev 2 | #8 | i18n translations and accessibility | #2 |
| Backend Dev 1 | #9 | Grok service integration | #3, #5 |
| Backend Dev 2 | #10 | Error handling and caching | #4 |
| Prompt Engineer | #11 | Prompt optimization and testing | #5 |
| Problem Finder | #12 | End-to-end testing | #6 |

---

## Issue Dependencies

```
Phase 0 (Scaffolding):
#15 ─────────────────────────────────────────────────────────────
                              │
                              ▼
Phase 1 (Parallel):
#1  #2  #3  #4  #5  #6  #13  #14
│   │   │   │   │   │
▼   ▼   ▼   ▼   ▼   ▼
Phase 2 (After dependencies):
#7  #8  #9  #10 #11 #12
        │
        └── #9 also blocked by #5
```

---

## Agent Responsibilities

### Scaffolding Agent (COMPLETE)
- ✅ Verify project structure
- ✅ Ensure all files in place
- ✅ Test frontend and backend start correctly
- ✅ Merge to main

### Orchestrator Agent
- Monitor PR status across all agents
- Merge PRs when ready (squash merge)
- Resolve merge conflicts if needed
- Coordinate cross-agent dependencies
- Keep main branch stable

### Frontend Dev 1
**Stack:** SAP UI5 1.120+, JavaScript ES6+
**Files:** `webapp/Component.js`, `webapp/controller/*`, `webapp/model/*`
- Issue #1: Create UI5 project skeleton
- Issue #7: Add formatters for signal/noise display

### Frontend Dev 2
**Stack:** SAP UI5 1.120+, XML views, CSS
**Files:** `webapp/view/*`, `webapp/css/*`, `webapp/i18n/*`
- Issue #2: Implement RadarView with 3-panel layout
- Issue #8: Create i18n translations

### Backend Dev 1
**Stack:** Python 3.11+, FastAPI
**Files:** `backend/app/api/*`, `backend/app/services/*`
- Issue #3: Implement API endpoints
- Issue #9: Integrate Grok service with LiteLLM

### Backend Dev 2
**Stack:** Python 3.11+, SQLAlchemy, SQLite
**Files:** `backend/app/models.py`, `backend/app/database.py`
- Issue #4: Implement SQLite models
- Issue #10: Add error handling and caching

### Prompt Engineer
**Stack:** Grok prompts, JSON schema
**Files:** `prompts/*`
- Issue #5: Create base prompt templates
- Issue #11: Optimize prompts for accuracy

### Problem Finder (QA)
**Focus:** Testing, bug discovery, code review
- Issue #6: Initial QA review and test plan
- Issue #12: End-to-end testing

### DevOps Agent
**Stack:** GitHub Actions, Docker
**Files:** `.github/workflows/*`, `Dockerfile`, `docker-compose.yml`
- Issue #14: CI/CD pipeline setup

---

## Starting an Agent

Each agent runs in its own terminal:

```bash
# Scaffolding (COMPLETE - no longer needed)
cd /Users/I769068/projects/scaling-productivity/demo2-scaffold && claude --dangerously-skip-permissions

# Orchestrator
cd /Users/I769068/projects/scaling-productivity/demo2 && claude --dangerously-skip-permissions

# Frontend Dev 1
cd /Users/I769068/projects/scaling-productivity/demo2-fe1 && claude --dangerously-skip-permissions

# Frontend Dev 2
cd /Users/I769068/projects/scaling-productivity/demo2-fe2 && claude --dangerously-skip-permissions

# Backend Dev 1
cd /Users/I769068/projects/scaling-productivity/demo2-be1 && claude --dangerously-skip-permissions

# Backend Dev 2
cd /Users/I769068/projects/scaling-productivity/demo2-be2 && claude --dangerously-skip-permissions

# Prompt Engineer
cd /Users/I769068/projects/scaling-productivity/demo2-prompt && claude --dangerously-skip-permissions

# Problem Finder (QA)
cd /Users/I769068/projects/scaling-productivity/demo2-qa && claude --dangerously-skip-permissions

# DevOps
cd /Users/I769068/projects/scaling-productivity/demo2-devops && claude --dangerously-skip-permissions
```

---

## Workflow Rules

1. **One issue at a time** - Complete full cycle before starting next
2. **Test before commit** - Run linters and tests
3. **Use Playwright MCP** - For all UI testing
4. **Update CHANGELOG.md** - Document changes
5. **Squash merge PRs** - Keep history clean
6. **Sync before starting** - `git fetch origin main && git rebase origin/main`

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
