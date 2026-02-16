# Role
Act as a **Principal Software Architect** and **Technical Project Manager** specializing in AI-driven data products.

# Objective
Write a **simple, actionable PRD** for the **"CodeScale Research Radar"** PoC using the KISS method.

# Output
Create the PRD document on root folder called `PRD.md`

---

# PRD Core Principles

A strong PRD eliminates ambiguity. This PRD explicitly answers five critical questions:

## 1. What problem is being solved?
Engineering teams waste hours manually tracking emerging tools and trends across Voice AI, Agent Orchestration, and Durable Runtime domains. Information is scattered across Twitter/X, buried in marketing hype, and lacks actionable technical evaluation. Teams need a zero-effort way to discover technically-relevant tools with architectural verdicts.

## 2. Who is the solution for?
| User | Need |
|------|------|
| **Software Architects** | Technology adoption decisions based on technical merit, not hype |
| **Engineering Managers** | Track domain evolution without manual research |
| **Tech Leads** | Quick signal on what's worth evaluating |

## 3. What is in scope / out of scope?

### In Scope
- Research focused in 3 areas: Voice AI UX, Agent Orchestration, Durable Runtime
- **LiteLLM with SAP Generative AI Hub** as the AI provider (see https://docs.litellm.ai/docs/providers/sap)
- Twitter/X trend analysis via AI model's knowledge
- **Signal vs Noise classification** - System must identify and categorize each finding as actionable signal or dismissible noise
- 1-day refresh cycle (daily batch processing)
- SAP UI5 Fiori-style dashboard with 3 cards displaying signal/noise findings per focus area
- SQLite persistence for historical data
- Local development environment only


### Out of Scope
- User authentication
- Multiple or custom data sources
- Custom/configurable focus areas
- Mobile-specific UI
- Production deployment or hardening
- Real-time updates (batch only)

## 4. What constraints must be respected?

| Constraint | Requirement |
|------------|-------------|
| **Parallelism** | Architecture MUST enable 3 developers to work independently |
| **Technology Stack** | SAP UI5, FastAPI, SQLite, LiteLLM with SAP Generative AI Hub (non-negotiable) |
| **Data Source** | SAP Generative AI Hub models—no separate Twitter API integration |
| **Timeline** | PoC scope only—no production features |
| **API Response** | Sub-200ms from database read |

## 5. What does success look like?

| Track | Success Criterion | Pass/Fail |
|-------|-------------------|-----------|
| **Frontend** | 3 cards render with mock data showing signal/noise classification | ☐ |
| **Backend** | `/api/radar` returns valid JSON in <200ms | ☐ |
| **Backend** | Daily scheduler runs and persists to SQLite | ☐ |
| **AI** | Signal vs Noise classification is accurate with supporting evidence | ☐ |
| **AI** | `technical_insight` contains specific details, not marketing copy | ☐ |
| **Integration** | End-to-end flow works: SAP Gen AI Hub → DB → API → UI | ☐ |

---

# Critical Constraint: Maximum Parallelism (3 Developers)
The architecture **MUST** decouple workstreams so 3 developers can work independently:
1. **Dev A (Frontend):** SAP UI5 Dashboard (reads from API/mock)
2. **Dev B (Backend):** FastAPI + Database (manages data flow)
3. **Dev C (AI Engineer):** SAP Generative AI Hub prompt optimization for signal/noise classification

---

# Product Concept
A dashboard tracking **Signal vs Noise** across 3 research areas:
1. **Voice AI UX** (Real-time agents, latency)
2. **Agent Orchestration** (BKG/Knowledge Graph integration)
3. **Durable Runtime** (Fault tolerance, serverless durability)

## Core Feature: Signal vs Noise Classification
Each finding is classified as:
* **Signal** - Technically substantive, backed by benchmarks/production usage, architecturally relevant
* **Noise** - Marketing hype, vaporware, no technical depth, engagement-farming content

## Data Source: SAP Generative AI Hub via LiteLLM
* **Key Insight:** Use SAP Generative AI Hub models through LiteLLM for Twitter/X trend analysis
* **Integration:** LiteLLM provides unified interface to SAP AI Core (see https://docs.litellm.ai/docs/providers/sap)
* **Flow:** `SAP Gen AI Hub → Signal/Noise Analysis → Database → API → Dashboard`
* **Advantage:** Enterprise-grade AI infrastructure with SAP ecosystem integration

# Required PRD Structure (Keep It Simple)

## 1. Executive Summary
* **Goal:** Signal vs Noise classification for architectural decision support
* **Flow:** `LiteLLM (SAP Gen AI Hub) → Database → API → Dashboard`
* **Core Feature:** Daily classification of Twitter/X trends as Signal or Noise
* **Value:** Zero-effort discovery of technically relevant tools, filtering out hype

## 2. The Golden Contract (JSON Schema)
Define the **exact** JSON format that enables parallel development:
* Fields: `focus_area`, `tool_name`, `classification` (signal/noise), `confidence_score` (1-100), `technical_insight`, `signal_evidence` (array), `noise_indicators` (array), `architectural_verdict` (boolean), `timestamp`
* Include a simple example matching the schema with signal/noise examples
* This is the **single source of truth** for all 3 tracks

## 3. Decoupled Workflows

### Track A: Frontend (SAP UI5)
* Build Fiori-style grid with 3 cards (one per focus area)
* Each card displays signal vs noise items with visual distinction
* Use `mock_radar.json` matching Golden Contract
* **Goal:** UI ready before backend exists

### Track B: Backend (Python/FastAPI)
* `GET /api/radar` endpoint returning Golden Contract JSON
* SQLite database for persistence
* Daily scheduler (cron) to run AI analysis once per day
* **LiteLLM Integration with SAP Generative AI Hub:**
  ```python
  import litellm
  
  # Configure SAP AI Core credentials
  response = litellm.completion(
      model="sap/gpt-4",  # or other SAP Gen AI Hub model
      messages=[{"role": "user", "content": prompt}]
  )
  ```
* **Goal:** Sub-200ms response, store historical data

### Track C: AI Engineering (SAP Gen AI Hub via LiteLLM)
* **Core Task:** Optimize prompts to classify signal vs noise accurately
* **Signal Criteria:** Benchmarks, production usage, technical depth, community validation
* **Noise Criteria:** Marketing language, no benchmarks, vaporware, engagement farming
* **Workflow:** Experiment → Measure → Optimize → Deliver prompts to Dev B
* Include a base prompt template for signal/noise classification
* **Goal:** Accurate classification with evidence-based reasoning

## 4. Architecture Flow
Simple ASCII diagram showing data flow:
```
┌─────────────────┐      ┌──────────┐      ┌─────────┐      ┌───────────┐
│  LiteLLM Call   │ ──▶  │  SQLite  │ ──▶  │ FastAPI │ ──▶  │  SAP UI5  │
│ (SAP Gen AI Hub)│      │    DB    │      │   API   │      │ Dashboard │
└─────────────────┘      └──────────┘      └─────────┘      └───────────┘
        │
        │ Daily batch: Analyze Twitter/X trends
        │ Classify as Signal or Noise
        ▼
```
* **SAP Generative AI Hub** - Enterprise-grade AI via LiteLLM
* **Single integration point** - LiteLLM abstracts SAP AI Core API

## 5. Use Cases (Prompt Validation)
Table showing signal vs noise criteria for each focus area:

| Focus Area | Signal Indicators | Noise Indicators |
|------------|-------------------|------------------|
| Voice AI UX | Latency benchmarks (ms), interruption handling specs, streaming architecture | "Revolutionary", no latency data, vague "AI-powered" claims |
| Agent Orchestration | BKG/Knowledge Graph integration details, tool chaining patterns | "Autonomous agents", no integration specs, hype-driven roadmaps |
| Durable Runtime | Durability guarantees, cold-start benchmarks, fault tolerance mechanisms | "Serverless magic", no SLAs, marketing-only content |

## 6. Success Criteria
Simple table with pass/fail metrics for each track, including signal/noise accuracy

## 7. Mock Data
Include ready-to-use `mock_radar.json` with signal and noise examples per focus area

---

# Guidelines
* **KISS:** This is a PoC. No over-engineering.
* **Actionable:** Each section should tell devs exactly what to build.
* **Parallel-Ready:** The Golden Contract is the enabler—define it clearly.
* **Concise:** Aim for ~2 pages, not 20.