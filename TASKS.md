# Plan: Restructure GitHub Issues for 3-Developer Parallel Work

## Objective
Break down the 7 existing issues into granular, track-specific tasks so 3 developers can work independently without blocking each other.

---

## Current Issues (to be restructured)
| # | Title | Action |
|---|-------|--------|
| 1 | Initialize git repository and create project structure | Keep (shared) |
| 2 | Update PRD.md with database schema and CORS config | Move to Track B |
| 3 | Create SETUP.md with environment setup guide | Split by track |
| 4 | Scaffold backend FastAPI application | Move to Track B |
| 5 | Scaffold frontend SAPUI5 application | Move to Track A |
| 6 | Create AI prompt templates | Move to Track C |
| 7 | Update project_instructions.md | Keep (shared) |

---

## Proposed Issue Structure (18 issues total)

### Phase 0: Shared Foundation (2 issues) - Any Developer
| # | Title | Labels | Blocks |
|---|-------|--------|--------|
| 1 | ✅ Initialize git repository and create project structure | chore | All tracks |
| 7 | Update project_instructions.md with task and git guidelines | docs | None |

### Track A: Frontend (5 issues) - Developer A
| New # | Title | Labels | Dependencies |
|-------|-------|--------|--------------|
| 8 | [Track A] Create UI5 project skeleton | feature, track-a | #1 |
| 9 | [Track A] Implement RadarView with 3-panel layout | feature, track-a | #8 |
| 10 | [Track A] Add mock data and JSON model binding | feature, track-a | #8 |
| 11 | [Track A] Create i18n translations | feature, track-a | #8 |
| 12 | [Track A] Add formatter and styling for signal/noise | feature, track-a | #9, #10 |

### Track B: Backend (6 issues) - Developer B
| New # | Title | Labels | Dependencies |
|-------|-------|--------|--------------|
| 2 | ✅ Update PRD.md with database schema and CORS config | docs, track-b | None |
| 3 | Create SETUP.md for backend (xAI API, Python setup) | docs, track-b | None |
| 4 | ✅ Scaffold backend FastAPI application | feature, track-b | #1 |
| 13 | [Track B] Implement SQLite models and database setup | feature, track-b | #4 |
| 14 | [Track B] Implement GET /api/radar endpoint | feature, track-b | #13 |
| 15 | [Track B] Implement POST /api/radar/refresh with Grok integration | feature, track-b | #14, #6 |

### Track C: AI/Prompts (4 issues) - Developer C
| New # | Title | Labels | Dependencies |
|-------|-------|--------|--------------|
| 6 | ✅ Create AI prompt templates | feature, track-c | None |
| 16 | [Track C] Design voice_ai classification prompt | feature, track-c | #6 |
| 17 | [Track C] Design agent_orchestration classification prompt | feature, track-c | #6 |
| 18 | [Track C] Design durable_runtime classification prompt | feature, track-c | #6 |

### Phase 2: Integration (3 issues) - All Developers
| New # | Title | Labels | Dependencies |
|-------|-------|--------|--------------|
| 19 | [Integration] Connect frontend to backend API | feature, integration | #12, #14 |
| 20 | [Integration] End-to-end test: Grok → DB → API → UI | feature, integration | #15, #19 |
| 21 | [Integration] Update SETUP.md with full integration guide | docs, integration | #19, #20 |

---

## Implementation Steps

### Step 1: Create Track Labels
```bash
gh label create "track-a" --description "Frontend (SAPUI5)" --color "1D76DB"
gh label create "track-b" --description "Backend (FastAPI)" --color "D93F0B"
gh label create "track-c" --description "AI/Prompts" --color "0E8A16"
gh label create "integration" --description "Cross-track integration" --color "FBCA04"
```

### Step 2: Update Existing Issues
- Add track labels to issues #2, #3, #4, #5, #6
- Update issue #3 title to focus on backend setup only

### Step 3: Create New Track-Specific Issues

**Track A (Frontend):**
- #8: Create UI5 project skeleton (Component.js, manifest.json, index.html, package.json, ui5.yaml)
- #9: Implement RadarView with 3-panel layout (sap.f.GridList, sap.m.Panel for each focus area)
- #10: Add mock data and JSON model binding (mock_radar.json, model setup in manifest)
- #11: Create i18n translations (all user-facing text)
- #12: Add formatter and styling for signal/noise (confidence display, color coding)

**Track B (Backend):**
- #13: Implement SQLite models and database setup (Trend model, init_db function)
- #14: Implement GET /api/radar endpoint (return trends, optional date filter)
- #15: Implement POST /api/radar/refresh with Grok integration (call LiteLLM, persist results)

**Track C (AI/Prompts):**
- #16: Design voice_ai classification prompt (latency benchmarks, VAD specs criteria)
- #17: Design agent_orchestration classification prompt (BKG integration, state persistence criteria)
- #18: Design durable_runtime classification prompt (SLAs, cold-start benchmarks criteria)

**Integration:**
- #19: Connect frontend to backend API (switch dataSource, handle CORS)
- #20: End-to-end test: Grok → DB → API → UI (manual refresh flow)
- #21: Update SETUP.md with full integration guide

### Step 4: Set Up Dependencies (blockedBy)
Use GitHub issue references in descriptions to indicate dependencies.

---

## Developer Assignment Overview

### Developer A (Frontend - Track A)
**Backlog:** #8 → #9, #10, #11 (parallel) → #12 → #19 (with Dev B)
**Stack:** Node.js, SAPUI5 1.120+, JavaScript ES6+
**Can start immediately:** Yes (uses mock data)

### Developer B (Backend - Track B)
**Backlog:** #2 → #4 → #13 → #14 → #15 (needs #6 from Dev C) → #19, #20
**Stack:** Python 3.10+, FastAPI, SQLite, LiteLLM
**Can start immediately:** Yes (mock Grok responses until prompts ready)

### Developer C (AI/Prompts - Track C)
**Backlog:** #6 → #16, #17, #18 (parallel) → #20
**Stack:** Grok playground, JSON schema validation
**Can start immediately:** Yes (iterate in playground)

---

## Verification Plan

### Track A Verification
```bash
cd webapp && npm install && npm start
# Browser at http://localhost:8080 shows 3 panels with mock data
npm run lint  # 0 errors
```

### Track B Verification
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest  # All tests pass
uvicorn app.main:app --reload
curl http://localhost:8000/api/radar  # Returns JSON
```

### Track C Verification
- Test each prompt in Grok playground
- Validate output against Golden Contract JSON schema
- Confirm signal items have evidence, noise items have indicators

### Integration Verification
```bash
# Terminal 1: Start backend
cd backend && uvicorn app.main:app --reload

# Terminal 2: Start frontend
npm start

# Browser: http://localhost:8080
# 1. Should show live data from backend
# 2. Network tab shows calls to localhost:8000
# 3. Manual refresh: curl -X POST http://localhost:8000/api/radar/refresh
# 4. UI updates with new data
```

---

## Files to Create/Modify

### New Labels (4)
- `track-a`, `track-b`, `track-c`, `integration`

### New Issues (14)
- #8-#12 (Track A)
- #13-#15 (Track B)
- #16-#18 (Track C)
- #19-#21 (Integration)

### Updated Issues (5)
- #2, #3, #4, #5, #6 (add track labels)
