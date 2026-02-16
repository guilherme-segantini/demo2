# CodeScale Research Radar - Product Requirements Document

## 1. Executive Summary

**Goal:** Signal vs Noise classification for architectural decision support. Engineering teams need to separate technically substantive tools from marketing hype.

**Flow:** `Grok (Discovery + Classification) → SQLite → FastAPI → SAP UI5 Dashboard`

**Core Feature:** Weekly analysis using Grok to **discover** relevant news/trends from the past 7 days AND **classify** them as **Signal** (worth evaluating) or **Noise** (skip).

**Key Insight:** No external news API needed - Grok's real-time knowledge of X/Twitter and tech news serves as both the discovery mechanism and the classification engine through prompt engineering.

**Value:** Zero-effort discovery of technically relevant tools across Voice AI, Agent Orchestration, and Durable Runtime domains.

---

## 2. The Golden Contract (JSON Schema)

This schema is the **single source of truth** enabling parallel development across all 3 tracks.

```json
{
  "radar_date": "2026-01-30",
  "trends": [
    {
      "focus_area": "voice_ai_ux",
      "tool_name": "LiveKit Agents",
      "classification": "signal",
      "confidence_score": 92,
      "technical_insight": "Sub-200ms voice-to-voice latency with WebRTC...",
      "signal_evidence": ["Published benchmarks", "Production case studies"],
      "noise_indicators": [],
      "architectural_verdict": true,
      "timestamp": "2026-01-30T08:00:00Z"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `radar_date` | string (YYYY-MM-DD) | Date of this radar analysis |
| `focus_area` | string | One of: `voice_ai_ux`, `agent_orchestration`, `durable_runtime` |
| `tool_name` | string | Name of the tool/technology being analyzed |
| `classification` | string | `"signal"` or `"noise"` |
| `confidence_score` | integer (1-100) | Confidence in the classification |
| `technical_insight` | string | Specific technical details supporting the classification |
| `signal_evidence` | array[string] | Reasons this is signal (empty if noise) |
| `noise_indicators` | array[string] | Reasons this is noise (empty if signal) |
| `architectural_verdict` | boolean | `true` = worth evaluating, `false` = skip |
| `timestamp` | ISO 8601 | When the analysis was performed |

---

## 3. Decoupled Workflows

### Track A: Frontend (SAP UI5)
**Owner:** Dev A  
**Independence:** Works entirely from mock data until backend ready

**Deliverables:**
- Fiori-style grid layout with 3 cards (one per focus area)
- Each card displays:
  - Signal items: Green badge, tool name, confidence score, evidence list
  - Noise items: Gray badge, tool name, noise indicators
- Visual distinction between signal and noise (color coding, icons)
- Data loaded from `mock_radar.json` (matches Golden Contract)
- Auto-refresh when data changes

**Tech:** SAP UI5 1.120+, JSON Model binding

---

### Track B: Backend (Python/FastAPI)
**Owner:** Dev B  
**Independence:** Works from Golden Contract schema; receives prompts from Dev C

**Deliverables:**
- `GET /api/radar` - Returns today's signal/noise analysis (Golden Contract format)
- `GET /api/radar?date=YYYY-MM-DD` - Returns historical data for a specific date
- SQLite database with `trends` table
- Weekly scheduler (cron job) to refresh data once every 7 days
- Sub-200ms response time from database read

**LiteLLM Integration with xAI/Grok:**
```python
import litellm
import os

# xAI API credentials (see https://docs.litellm.ai/docs/providers/xai)
os.environ["XAI_API_KEY"] = "your-xai-api-key"

response = litellm.completion(
    model="xai/grok-beta",  # Grok model via xAI
    messages=[{"role": "user", "content": prompt}]
)
```

---

### Track C: AI/Prompt Engineering (Grok via LiteLLM)
**Owner:** Dev C  
**Independence:** Iterates on prompts; delivers finalized prompts to Dev B

**Core Approach:** Grok handles BOTH discovery AND classification through prompt engineering:
1. **Discovery** - Grok uses its real-time knowledge of X/Twitter discussions and tech news to find relevant tools
2. **Classification** - Grok applies signal/noise criteria to each discovered tool

**No External News API Required** - Grok's training data and real-time access to X/Twitter provides the news discovery mechanism.

**Deliverables:**
- Optimized prompts that instruct Grok to search AND classify
- Prompts extract evidence-based reasoning, not opinions
- Validation: Classifications match expected signal/noise criteria

**Signal Criteria:**
- Published benchmarks or performance data
- Production case studies or real-world usage
- Specific technical architecture details
- Active community with technical discussions

**Noise Criteria:**
- Marketing language ("revolutionary", "game-changing")
- No benchmarks or vague performance claims
- Vaporware or pre-announcement hype
- Engagement farming (controversial takes, no substance)

**Base Prompt Template (Discovery + Classification):**
```
Using your real-time knowledge of X/Twitter discussions and tech news from the past 7 days, 
SEARCH for and ANALYZE tools related to {focus_area}.

STEP 1 - DISCOVER:
Search your knowledge for tools being discussed in the {focus_area} space.
Look for announcements, releases, technical discussions, and trending topics.

STEP 2 - CLASSIFY each discovered tool as SIGNAL or NOISE:

SIGNAL criteria (worth evaluating):
- Has published benchmarks or performance data
- Shows production usage or real case studies
- Provides specific technical architecture details
- Has active technical community discussion

NOISE criteria (skip):
- Uses marketing language without substance
- No benchmarks or only vague claims
- Pre-announcement hype or vaporware
- Engagement farming without technical depth

For {focus_area}, specifically evaluate:
{evaluation_criteria}

Return JSON array with your findings:
[
  {
    "tool_name": "string",
    "classification": "signal" | "noise",
    "confidence_score": 1-100,
    "technical_insight": "specific technical details you found",
    "signal_evidence": ["evidence1", "evidence2"],
    "noise_indicators": ["indicator1", "indicator2"],
    "architectural_verdict": true | false
  }
]
```

---

## 4. Architecture Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Grok (via LiteLLM)                       │
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │ 1. DISCOVER     │ ── │ 2. CLASSIFY                     │ │
│  │ Search for news │    │ Signal vs Noise analysis        │ │
│  │ about tools in  │    │ based on criteria               │ │
│  │ focus areas     │    │ (benchmarks, evidence, etc.)    │ │
│  └─────────────────┘    └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    Structured JSON Output
                              │
                              ▼
┌─────────────────┐      ┌──────────┐      ┌─────────┐      ┌───────────┐
│  LiteLLM Call   │ ──▶  │  SQLite  │ ──▶  │ FastAPI │ ──▶  │  SAP UI5  │
│   (xAI/Grok)    │      │    DB    │      │   API   │      │ Dashboard │
└─────────────────┘      └──────────┘      └─────────┘      └───────────┘
        │
        │ Weekly batch (every 7 days):
        │ • Grok DISCOVERS trends from past 7 days for 3 focus areas
        │ • Grok CLASSIFIES each as Signal or Noise
        │ • Persist to SQLite with timestamp
        │ • Display only results from previous 7 days
        ▼
```

**Key Architecture Decisions:**
- **No external news API** - Grok's real-time knowledge serves as the news source
- **Single prompt = Discovery + Classification** - One call to Grok handles both
- **xAI/Grok** - AI provider via LiteLLM (see https://docs.litellm.ai/docs/providers/xai)
- **Prompt engineering driven** - The quality of results depends on prompt design
- **Weekly refresh** - Batch processing every 7 days, showing results from the past week

---

## 5. Use Cases (Signal vs Noise Criteria by Focus Area)

| Focus Area | Signal Indicators | Noise Indicators |
|------------|-------------------|------------------|
| **Voice AI UX** | Latency benchmarks (ms), interruption handling specs, WebRTC/streaming architecture, VAD implementation | "Revolutionary AI", no latency data, vague "human-like" claims, demo-only |
| **Agent Orchestration** | BKG/Knowledge Graph integration, tool chaining patterns, state persistence, human-in-loop specs | "Autonomous agents", no integration details, hype-driven roadmaps, AGI claims |
| **Durable Runtime** | Durability guarantees (SLAs), cold-start benchmarks, checkpoint/recovery specs, fault tolerance | "Serverless magic", no SLAs, marketing-only, "infinite scale" without details |

---

## 6. Success Criteria

| Track | Success Criterion | Pass/Fail |
|-------|-------------------|-----------|
| **Frontend** | 3 cards render with signal/noise visual distinction | ☐ |
| **Frontend** | Signal items show green badge + evidence list | ☐ |
| **Frontend** | Noise items show gray badge + noise indicators | ☐ |
| **Backend** | `/api/radar` returns valid JSON in <200ms | ☐ |
| **Backend** | Weekly scheduler runs and persists to SQLite | ☐ |
| **Backend** | Historical data queryable by date | ☐ |
| **AI** | Signal classifications include concrete evidence | ☐ |
| **AI** | Noise classifications identify specific hype patterns | ☐ |
| **AI** | `technical_insight` contains specifics, not marketing copy | ☐ |
| **Integration** | End-to-end: xAI/Grok → DB → API → UI | ☐ |

---

## 7. Mock Data

File: `mock_radar.json`

```json
{
  "radar_date": "2026-01-30",
  "trends": [
    {
      "focus_area": "voice_ai_ux",
      "tool_name": "LiveKit Agents",
      "classification": "signal",
      "confidence_score": 92,
      "technical_insight": "Sub-200ms voice-to-voice latency with WebRTC. Supports interruption handling via VAD (Voice Activity Detection). Native Python SDK with async streaming. Published benchmarks show P95 latency <250ms.",
      "signal_evidence": [
        "Published latency benchmarks",
        "Production usage at scale (Daily.co integration)",
        "Open-source with active technical community"
      ],
      "noise_indicators": [],
      "architectural_verdict": true,
      "timestamp": "2026-01-30T08:00:00Z"
    },
    {
      "focus_area": "voice_ai_ux",
      "tool_name": "VoiceHype AI",
      "classification": "noise",
      "confidence_score": 85,
      "technical_insight": "Claims 'revolutionary conversational AI' but provides no latency benchmarks. Demo video only, no SDK or architecture documentation available.",
      "signal_evidence": [],
      "noise_indicators": [
        "No published benchmarks",
        "Marketing language ('revolutionary', 'human-like')",
        "Demo-only, no production evidence"
      ],
      "architectural_verdict": false,
      "timestamp": "2026-01-30T08:00:00Z"
    },
    {
      "focus_area": "agent_orchestration",
      "tool_name": "LangGraph",
      "classification": "signal",
      "confidence_score": 87,
      "technical_insight": "Graph-based agent orchestration with built-in state persistence. Supports cyclic workflows and human-in-the-loop patterns. Native integration with LangChain tools. Checkpoint API enables workflow recovery.",
      "signal_evidence": [
        "Detailed architecture documentation",
        "Production case studies (multiple enterprises)",
        "Active GitHub with technical discussions"
      ],
      "noise_indicators": [],
      "architectural_verdict": true,
      "timestamp": "2026-01-30T08:00:00Z"
    },
    {
      "focus_area": "agent_orchestration",
      "tool_name": "AutoAgent Pro",
      "classification": "noise",
      "confidence_score": 78,
      "technical_insight": "Promises 'fully autonomous agents' but lacks integration documentation. Roadmap-heavy announcements without shipping history.",
      "signal_evidence": [],
      "noise_indicators": [
        "AGI-adjacent marketing claims",
        "No integration specifications",
        "Roadmap announcements without releases"
      ],
      "architectural_verdict": false,
      "timestamp": "2026-01-30T08:00:00Z"
    },
    {
      "focus_area": "durable_runtime",
      "tool_name": "Temporal.io",
      "classification": "signal",
      "confidence_score": 94,
      "technical_insight": "Workflow durability with automatic retries and state recovery. Cold-start ~50ms for cached workers. Supports long-running workflows (days/weeks) with checkpoint persistence. Published SLAs for cloud offering.",
      "signal_evidence": [
        "Published cold-start benchmarks",
        "SLA documentation for durability guarantees",
        "Enterprise production usage (Netflix, Snap)"
      ],
      "noise_indicators": [],
      "architectural_verdict": true,
      "timestamp": "2026-01-30T08:00:00Z"
    },
    {
      "focus_area": "durable_runtime",
      "tool_name": "InfiniScale Runtime",
      "classification": "noise",
      "confidence_score": 81,
      "technical_insight": "Claims 'infinite scale with zero cold starts' but provides no benchmark data. Private beta with waitlist, no architecture documentation.",
      "signal_evidence": [],
      "noise_indicators": [
        "Impossible claims ('zero cold starts')",
        "No published benchmarks",
        "Waitlist-only, no technical docs"
      ],
      "architectural_verdict": false,
      "timestamp": "2026-01-30T08:00:00Z"
    }
  ]
}