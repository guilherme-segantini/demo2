# CodeScale Research Radar - PRD Review & Execution Plan

## Executive Summary

**Task:** Review the PRD for parallel development readiness and provide execution recommendations.
f
**Verdict:** ✅ **The PRD is well-structured for parallel development** with minor gaps to address.

**Key Strengths:**
- Golden Contract (JSON Schema) enables true decoupling across tracks
- Clear ownership boundaries (Dev A, B, C)
- Mock data provided for frontend independence
- Explicit success criteria per track

**Gaps Identified:**
1. Missing project structure and file organization
2. xAI API key setup instructions needed
3. Weekly scheduler deferred to manual trigger (per user request)
4. No database schema definition beyond JSON
5. Missing UI5 component structure details

---

## Analysis: Is This PRD Ready for Parallel Development?

### ✅ What Works Well

#### 1. **Golden Contract (Section 2)**
The JSON schema is the foundation for parallel work:
- Frontend can mock this immediately
- Backend knows the exact response structure
- AI team knows the output format

**Strength:** No team is blocked by another.

#### 2. **Track Independence (Section 3)**
Each track has clear deliverables:
- **Track A (UI5):** Mock data → Components → Visual design
- **Track B (FastAPI):** Schema → SQLite → API endpoints
- **Track C (Prompts):** Criteria → Prompt design → Output validation

**Strength:** Teams can work in parallel without coordination overhead.

#### 3. **Signal/Noise Criteria (Section 5)**
Specific, measurable criteria per focus area:
- Voice AI: Latency benchmarks, VAD specs
- Agent Orchestration: BKG integration, state persistence
- Durable Runtime: SLAs, cold-start benchmarks

**Strength:** Clear decision-making framework for classification.

#### 4. **Mock Data (Section 7)**
Complete mock dataset with 6 examples (2 per focus area):
- Shows signal AND noise examples
- Demonstrates confidence scoring
- Includes realistic technical details

**Strength:** Frontend can build and test UI without waiting for backend.

---

### ⚠️ Gaps and Recommendations

#### Gap 1: **Project Structure Not Defined**

**Problem:** PRD doesn't specify folder structure or file organization.

**Impact:** Teams may create conflicting structures.

**Recommendation:**
```
project-template/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── models.py            # SQLite schema
│   │   ├── services/
│   │   │   └── grok_service.py  # LiteLLM integration
│   │   └── api/
│   │       └── radar.py         # API endpoints
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example            # xAI API key template
├── webapp/                      # SAPUI5 app
│   ├── Component.js
│   ├── manifest.json
│   ├── controller/
│   │   └── RadarView.controller.js
│   ├── view/
│   │   └── RadarView.view.xml
│   ├── model/
│   │   ├── formatter.js
│   │   └── mock_radar.json
│   └── i18n/
│       └── i18n.properties
├── prompts/
│   ├── voice_ai_prompt.txt
│   ├── agent_orchestration_prompt.txt
│   └── durable_runtime_prompt.txt
├── PRD.md
├── CLAUDE.md
└── CHANGELOG.md
```

---

#### Gap 2: **xAI API Key Setup Missing**

**Problem:** PRD mentions LiteLLM integration but no setup guide.

**Impact:** Backend developer blocked on authentication.

**Recommendation:** Add to PRD or create separate `SETUP.md`:

```markdown
## xAI API Key Setup

1. Get API key from https://console.x.ai/
2. Install LiteLLM: `pip install litellm`
3. Set environment variable:
   ```bash
   export XAI_API_KEY="your-key-here"
   ```
4. Or use `.env` file:
   ```
   XAI_API_KEY=your-key-here
   ```
5. Test connection:
   ```python
   import litellm
   response = litellm.completion(
       model="xai/grok-beta",
       messages=[{"role": "user", "content": "Hello"}]
   )
   ```
```

**Note:** User confirmed they need setup instructions.

---

#### Gap 3: **Database Schema Underspecified**

**Problem:** PRD shows JSON output but not SQLite table structure.

**Impact:** Backend developer must infer schema design.

**Recommendation:** Add to PRD Section 3 (Track B):

```sql
CREATE TABLE trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    radar_date TEXT NOT NULL,
    focus_area TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    classification TEXT NOT NULL CHECK(classification IN ('signal', 'noise')),
    confidence_score INTEGER NOT NULL CHECK(confidence_score >= 1 AND confidence_score <= 100),
    technical_insight TEXT NOT NULL,
    signal_evidence TEXT,  -- JSON array as TEXT
    noise_indicators TEXT, -- JSON array as TEXT
    architectural_verdict INTEGER NOT NULL, -- 0 or 1 (boolean)
    timestamp TEXT NOT NULL, -- ISO 8601
    UNIQUE(radar_date, focus_area, tool_name)
);

CREATE INDEX idx_radar_date ON trends(radar_date);
CREATE INDEX idx_focus_area ON trends(focus_area);
CREATE INDEX idx_classification ON trends(classification);
```

---

#### Gap 4: **UI5 Component Structure Vague**

**Problem:** Track A says "Fiori-style grid layout with 3 cards" but no UI5-specific details.

**Impact:** Frontend developer must decide on controls without guidance.

**Recommendation:** Specify UI5 controls in Track A deliverables:

```markdown
### Track A: Frontend (SAP UI5) - Detailed Spec

**View Structure:**
- Use `sap.f.GridList` with 3 columns (one per focus area)
- Each focus area = `sap.m.Panel` with title
- Signal items: `sap.m.ObjectStatus` (state=Success, icon=accept)
- Noise items: `sap.m.ObjectStatus` (state=None, icon=decline)

**Data Binding:**
- JSON Model bound to `/trends`
- Filter by `focus_area` for each panel
- Use `sap.ui.model.Filter` for signal/noise separation

**i18n Keys:**
- `radarTitle`: "CodeScale Research Radar"
- `voiceAiTitle`: "Voice AI UX"
- `agentOrchestrationTitle`: "Agent Orchestration"
- `durableRuntimeTitle`: "Durable Runtime"
- `signalLabel`: "Signal"
- `noiseLabel`: "Noise"
- `confidenceLabel`: "Confidence: {0}%"
```

---

#### Gap 5: **Scheduler Decision Documented**

**Status:** ✅ Resolved per user input.

**Original PRD:** Weekly cron job.

**Updated Plan:** Manual trigger first (`POST /api/radar/refresh`), add scheduler later.

**Rationale:** Faster MVP, easier debugging, manual control during testing.

---

#### Gap 6: **Error Handling Not Specified**

**Problem:** What happens when Grok API fails? Or returns invalid JSON?

**Impact:** Backend may crash or show incomplete data.

**Recommendation:** Add error handling requirements to Track B:

```markdown
### Error Handling (Track B)

**Grok API Failures:**
- Retry with exponential backoff (3 attempts)
- Log failure with timestamp
- Return cached data from previous successful run
- Set `stale_data: true` flag in API response

**Invalid JSON from Grok:**
- Log raw response for debugging
- Validate against JSON schema before persisting
- Return empty array for that focus area
- Continue processing other focus areas

**Database Errors:**
- Log error details
- Return HTTP 500 with error message
- Don't persist partial data (use transactions)
```

---

#### Gap 7: **CORS and API Configuration Missing**

**Problem:** UI5 app runs on different port than FastAPI during dev.

**Impact:** CORS errors block frontend from calling backend.

**Recommendation:** Add to Track B setup:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # UI5 dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

And update UI5 `manifest.json` dataSource:
```json
"dataSources": {
  "radarAPI": {
    "uri": "http://localhost:8000/api/radar",
    "type": "JSON"
  }
}
```

---

## Recommendations for PRD Improvements

### Priority 1: Add Before Development Starts

1. **Project Structure** (Gap 1) - Critical for avoiding conflicts
2. **xAI API Setup Guide** (Gap 2) - Blocks backend development
3. **Database Schema** (Gap 3) - Backend needs this immediately

### Priority 2: Add During Sprint 1

4. **UI5 Control Specifications** (Gap 4) - Frontend can infer, but explicit is better
5. **Error Handling Requirements** (Gap 6) - Add before production
6. **CORS Configuration** (Gap 7) - Needed when frontend calls backend

### Priority 3: Nice-to-Have

7. **Performance Benchmarks** - Target response times beyond "sub-200ms"
8. **Accessibility Requirements** - WCAG compliance for UI
9. **Deployment Guide** - Where to host backend/frontend

---

## Critical Files to Create

Based on the PRD, these files must be created:

### Backend (Track B)
- `/backend/.env.example` - xAI API key template
- `/backend/app/main.py` - FastAPI app entry point
- `/backend/app/models.py` - SQLite ORM models
- `/backend/app/services/grok_service.py` - LiteLLM integration
- `/backend/app/api/radar.py` - API endpoints
- `/backend/requirements.txt` - Python dependencies
- `/backend/tests/test_radar_api.py` - API endpoint tests

### Frontend (Track A)
- `/webapp/manifest.json` - App configuration
- `/webapp/Component.js` - Root component
- `/webapp/model/mock_radar.json` - Mock data (from PRD Section 7)
- `/webapp/view/RadarView.view.xml` - Main view
- `/webapp/controller/RadarView.controller.js` - View controller
- `/webapp/i18n/i18n.properties` - Translations
- `/webapp/model/formatter.js` - Data formatters

### AI/Prompts (Track C)
- `/prompts/voice_ai_prompt.txt` - Voice AI discovery + classification prompt
- `/prompts/agent_orchestration_prompt.txt` - Agent orchestration prompt
- `/prompts/durable_runtime_prompt.txt` - Durable runtime prompt
- `/prompts/README.md` - Prompt engineering notes and iteration log

### Shared
- `/mock_radar.json` - Copy of mock data for backend testing
- `/.gitignore` - Exclude .env, node_modules, __pycache__, dist/
- `/SETUP.md` - Setup instructions for all tracks

---

## Verification Plan

### Track A (Frontend) - Verify Independently
1. Run `npm start` → UI5 app loads at `localhost:8080`
2. Check UI renders 3 panels (Voice AI, Agent Orchestration, Durable Runtime)
3. Verify signal items show green badges with evidence list
4. Verify noise items show gray badges with noise indicators
5. Check confidence scores display correctly
6. Verify i18n used for all labels (no hardcoded English)
7. Run `npm run lint` → 0 errors

### Track B (Backend) - Verify Independently
1. Run `python -m pytest` → All tests pass
2. Start FastAPI: `uvicorn app.main:app --reload`
3. Test `GET /api/radar` → Returns mock data in <200ms
4. Test `POST /api/radar/refresh` → Calls Grok, persists to SQLite
5. Test `GET /api/radar?date=2026-01-30` → Returns historical data
6. Check SQLite database has `trends` table with data
7. Verify Grok API integration works (requires xAI API key)

### Track C (AI/Prompts) - Verify with Track B
1. Test prompt with real Grok API
2. Verify JSON output matches Golden Contract schema
3. Check signal items have concrete evidence (benchmarks, case studies)
4. Check noise items have specific hype indicators
5. Validate confidence scores correlate with evidence quality
6. Test all 3 focus areas (voice_ai, agent_orchestration, durable_runtime)

### End-to-End Integration
1. Backend calls Grok → Persists to SQLite → Exposes API
2. Frontend calls backend API → Renders data in UI
3. Refresh flow: Manual trigger → Grok analysis → DB update → UI refresh
4. Historical data: Select date → API call → UI shows past radar

---

## Success Criteria Review

Reviewing PRD Section 6 against parallel development readiness:

| Criterion | Ready for Parallel Dev? | Notes |
|-----------|-------------------------|-------|
| Frontend: 3 cards render | ✅ Yes | Mock data provided |
| Frontend: Signal items with green badge | ✅ Yes | Mock data shows examples |
| Frontend: Noise items with gray badge | ✅ Yes | Mock data shows examples |
| Backend: `/api/radar` in <200ms | ✅ Yes | Schema defined |
| Backend: Weekly scheduler | ⚠️ Changed | Manual trigger first (per user) |
| Backend: Historical data queryable | ✅ Yes | Date parameter in spec |
| AI: Signal with evidence | ✅ Yes | Criteria defined in Section 5 |
| AI: Noise with hype patterns | ✅ Yes | Criteria defined in Section 5 |
| AI: Technical insight specific | ✅ Yes | Examples in mock data |
| Integration: Grok → DB → API → UI | ⚠️ Needs | CORS config + API URLs |

**Overall:** 8/10 criteria ready for parallel development. 2 need minor additions (scheduler change documented, CORS config needed).

---

## Final Verdict: ✅ **Ready with Minor Additions**

The PRD is **solid for parallel development** with these additions:

### Must-Have (Add Now)
1. Project structure diagram
2. xAI API setup guide
3. SQLite schema definition

### Should-Have (Add Sprint 1)
4. CORS configuration
5. Error handling requirements

### Nice-to-Have (Add Later)
6. UI5 control specifications (can be inferred)
7. Deployment guide

---

## Recommended Next Steps

1. **Update PRD** with Gaps 1-3 (structure, API setup, schema)
2. **Create project skeleton** with folder structure
3. **Dev A:** Start frontend with mock data
4. **Dev B:** Setup xAI API key, implement `/api/radar` endpoint
5. **Dev C:** Iterate on prompts using Grok playground
6. **Integration:** Connect frontend to backend once both working independently

**Timeline Estimate:** (Removed per user guidelines - no time estimates)

**Risk Mitigation:**
- Frontend blocked by backend? → Use mock data (already provided)
- Grok API fails? → Use cached example response during dev
- Schema changes? → Golden Contract prevents this with strict spec

---

## User Decisions

1. ✅ **Documentation:** Update PRD + create separate SETUP.md
2. ✅ **Scaffolding:** Yes, generate full project skeleton
3. ✅ **API Route:** `POST /api/radar/refresh`

---

## Execution Plan

### Phase 1: Documentation Updates (Read-Only in Plan Mode)

**Files to Update:**
1. `PRD.md` - Add database schema, project structure diagram, CORS config
2. Create `SETUP.md` - xAI API key setup, environment configuration

### Phase 2: Project Skeleton Generation (After Exiting Plan Mode)

**Create the following structure:**

```
project-template/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── models.py                  # SQLite ORM models
│   │   ├── database.py                # Database connection
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── radar.py               # GET /api/radar, POST /api/radar/refresh
│   │   └── services/
│   │       ├── __init__.py
│   │       └── grok_service.py        # LiteLLM/Grok integration
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_radar_api.py
│   │   └── test_grok_service.py
│   ├── requirements.txt               # Python dependencies
│   ├── .env.example                   # xAI API key template
│   └── README.md                      # Backend setup instructions
├── webapp/
│   ├── Component.js                   # Root UI5 component
│   ├── manifest.json                  # App configuration
│   ├── index.html                     # Entry point
│   ├── controller/
│   │   ├── BaseController.js
│   │   └── RadarView.controller.js
│   ├── view/
│   │   ├── App.view.xml
│   │   └── RadarView.view.xml
│   ├── model/
│   │   ├── formatter.js
│   │   └── mock_radar.json            # Mock data from PRD
│   ├── i18n/
│   │   └── i18n.properties            # Translations
│   ├── css/
│   │   └── style.css
│   └── test/
│       ├── unit/
│       └── integration/
├── prompts/
│   ├── README.md                      # Prompt engineering guide
│   ├── voice_ai_prompt.txt
│   ├── agent_orchestration_prompt.txt
│   └── durable_runtime_prompt.txt
├── .gitignore
├── package.json                       # UI5 dev dependencies
├── ui5.yaml                          # UI5 tooling config
├── SETUP.md                          # Environment setup guide
├── PRD.md                            # Updated with gaps filled
├── CLAUDE.md                         # Existing
├── CHANGELOG.md                      # Existing
└── skills/                           # Existing
```

### Phase 3: File Contents

**Critical files with starter content:**

#### `backend/requirements.txt`
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
litellm==1.17.0
sqlalchemy==2.0.25
pydantic==2.5.3
python-dotenv==1.0.0
pytest==7.4.4
httpx==0.26.0
```

#### `backend/.env.example`
```
XAI_API_KEY=your-xai-api-key-here
DATABASE_URL=sqlite:///./radar.db
CORS_ORIGINS=http://localhost:8080
```

#### `backend/app/models.py`
```python
from sqlalchemy import Column, Integer, String, Boolean, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, autoincrement=True)
    radar_date = Column(String, nullable=False)
    focus_area = Column(String, nullable=False)
    tool_name = Column(String, nullable=False)
    classification = Column(String, nullable=False)  # 'signal' or 'noise'
    confidence_score = Column(Integer, nullable=False)
    technical_insight = Column(Text, nullable=False)
    signal_evidence = Column(Text)  # JSON array as TEXT
    noise_indicators = Column(Text)  # JSON array as TEXT
    architectural_verdict = Column(Boolean, nullable=False)
    timestamp = Column(String, nullable=False)  # ISO 8601
```

#### `webapp/package.json`
```json
{
  "name": "codescale-radar",
  "version": "1.0.0",
  "scripts": {
    "start": "ui5 serve --open index.html",
    "build": "ui5 build --clean-dest --all",
    "lint": "ui5lint"
  },
  "devDependencies": {
    "@ui5/cli": "^3.9.0",
    "@ui5/linter": "^0.1.0"
  }
}
```

#### `webapp/manifest.json` (abbreviated)
```json
{
  "sap.app": {
    "id": "com.codescale.radar",
    "type": "application",
    "title": "CodeScale Research Radar",
    "applicationVersion": {
      "version": "1.0.0"
    },
    "dataSources": {
      "radarAPI": {
        "uri": "http://localhost:8000/api/radar",
        "type": "JSON"
      },
      "mockData": {
        "uri": "model/mock_radar.json",
        "type": "JSON"
      }
    }
  },
  "sap.ui5": {
    "models": {
      "": {
        "dataSource": "mockData",
        "preload": true
      },
      "i18n": {
        "type": "sap.ui.model.resource.ResourceModel",
        "uri": "i18n/i18n.properties"
      }
    },
    "routing": {
      "config": {
        "routerClass": "sap.m.routing.Router",
        "controlId": "app",
        "controlAggregation": "pages"
      },
      "routes": [
        {
          "name": "radar",
          "pattern": "",
          "target": "radar"
        }
      ],
      "targets": {
        "radar": {
          "viewName": "RadarView",
          "viewLevel": 1
        }
      }
    }
  }
}
```

#### `SETUP.md` (new file)
```markdown
# CodeScale Research Radar - Setup Guide

## Prerequisites

- Node.js v20.11.0+ or v22.0.0+
- Python 3.10+
- xAI API key from https://console.x.ai/

## Backend Setup (Track B)

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your XAI_API_KEY
   ```

5. Initialize database:
   ```bash
   python -c "from app.database import init_db; init_db()"
   ```

6. Start FastAPI server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

7. Test API:
   ```bash
   curl http://localhost:8000/api/radar
   ```

## Frontend Setup (Track A)

1. Navigate to project root:
   ```bash
   cd ..
   ```

2. Install UI5 dependencies:
   ```bash
   npm install
   ```

3. Start UI5 dev server:
   ```bash
   npm start
   ```

4. Open browser at http://localhost:8080

## xAI API Key Setup

1. Sign up at https://console.x.ai/
2. Navigate to API Keys section
3. Create new API key
4. Copy key to `backend/.env`:
   ```
   XAI_API_KEY=xai-your-actual-key-here
   ```

## Testing LiteLLM Integration

```python
import litellm
import os
from dotenv import load_dotenv

load_dotenv()

response = litellm.completion(
    model="xai/grok-beta",
    messages=[{"role": "user", "content": "Say hello"}]
)
print(response.choices[0].message.content)
```

## Switching from Mock to Real API

In `webapp/manifest.json`, change the model dataSource:

```json
"models": {
  "": {
    "dataSource": "radarAPI",  // Change from "mockData" to "radarAPI"
    "preload": true
  }
}
```

## Troubleshooting

**CORS errors:**
- Check FastAPI CORS middleware allows `http://localhost:8080`
- Verify backend is running on port 8000

**Grok API errors:**
- Verify `XAI_API_KEY` is set in `.env`
- Check API key is valid at https://console.x.ai/
- Review LiteLLM docs: https://docs.litellm.ai/docs/providers/xai

**UI5 won't start:**
- Run `npm run lint` to check for errors
- Check Node.js version: `node --version`
```

#### `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.env
*.db

# Node
node_modules/
dist/
.DS_Store

# IDE
.vscode/
.idea/
*.swp
*.swo

# UI5
webapp/resources/
webapp/test-resources/
```

### Phase 4: PRD Updates

**Add to PRD.md Section 3 (Track B):**

```markdown
### SQLite Database Schema

```sql
CREATE TABLE trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    radar_date TEXT NOT NULL,
    focus_area TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    classification TEXT NOT NULL CHECK(classification IN ('signal', 'noise')),
    confidence_score INTEGER NOT NULL CHECK(confidence_score >= 1 AND confidence_score <= 100),
    technical_insight TEXT NOT NULL,
    signal_evidence TEXT,  -- JSON array as TEXT
    noise_indicators TEXT, -- JSON array as TEXT
    architectural_verdict INTEGER NOT NULL, -- 0 or 1 (boolean)
    timestamp TEXT NOT NULL, -- ISO 8601
    UNIQUE(radar_date, focus_area, tool_name)
);

CREATE INDEX idx_radar_date ON trends(radar_date);
CREATE INDEX idx_focus_area ON trends(focus_area);
CREATE INDEX idx_classification ON trends(classification);
```

**API Endpoints:**
- `GET /api/radar` - Returns latest radar analysis (default: today)
- `GET /api/radar?date=YYYY-MM-DD` - Returns historical analysis for specific date
- `POST /api/radar/refresh` - Manually trigger Grok analysis (generates new radar data)

**CORS Configuration:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
```

---

## Summary: What Gets Created

### Documentation (2 files)
- Updated `PRD.md` with database schema, API routes, CORS config
- New `SETUP.md` with environment setup for all three tracks

### Backend (12 files)
- Python package structure with FastAPI app
- SQLite models and database connection
- Grok/LiteLLM service integration
- API endpoints for radar data
- Test files for API and services
- `requirements.txt`, `.env.example`, `README.md`

### Frontend (14 files)
- Complete SAP UI5 application structure
- Component, manifest, views, controllers
- Mock data from PRD
- i18n translations
- Test folder structure
- `package.json`, `ui5.yaml`

### AI/Prompts (4 files)
- 3 prompt templates (one per focus area)
- README with prompt engineering guidelines

### Config (2 files)
- `.gitignore` for Python + Node
- Root-level config files

**Total: 34 files + folder structure**

---

## Verification After Implementation

### Phase 1: Verify Backend Independently
```bash
cd backend
source venv/bin/activate
pytest
uvicorn app.main:app --reload
curl http://localhost:8000/api/radar  # Should return mock or empty array
```

### Phase 2: Verify Frontend Independently
```bash
npm start
# Browser opens at http://localhost:8080
# Should see 3 panels with mock data
npm run lint  # Should pass with 0 errors
```

### Phase 3: Verify Integration
1. Start backend on port 8000
2. Update `webapp/manifest.json` to use `radarAPI` dataSource
3. Start frontend on port 8080
4. Verify frontend calls backend (check Network tab)
5. Test manual refresh: `curl -X POST http://localhost:8000/api/radar/refresh`

---

## Next Steps After Scaffold

1. **Dev A (Frontend):** Implement `RadarView.view.xml` with 3 cards
2. **Dev B (Backend):** Implement `grok_service.py` with LiteLLM integration
3. **Dev C (Prompts):** Test prompts in Grok playground, iterate on output quality
4. **Integration:** Connect frontend to backend API once both tracks working

---

**Plan Complete:** Ready to exit plan mode and execute.
