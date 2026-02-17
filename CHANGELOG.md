# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Fixed
- **UI5 manifest.json routing configuration** - Migrated to manifest version 2.0.0 format with correct routing config (`type: "View"`, `path` instead of `viewPath`, removed deprecated `async` property). Fixes app shell initialization and linting errors.
- **RadarView controller null checks** - Added defensive null checks for `getOwnerComponent()` and model retrieval in onInit to handle timing issues during view creation.

## [0.1.0] - 2026-02-16

### Scaffolding Complete ✅

This release verifies that the project foundation is complete and working. All files are in place, dependencies install successfully, and both frontend and backend start without errors.

### Added
- **XML View Fragments** - Created SignalItem.fragment.xml and NoiseItem.fragment.xml for displaying radar trends in the UI
- **Voice AI prompt template** (`prompts/voice_ai_prompt.md`) - Discovery and classification prompt with criteria for latency benchmarks, VAD implementation, streaming architecture
- **Agent Orchestration prompt template** (`prompts/agent_orchestration_prompt.md`) - Discovery and classification prompt with criteria for state persistence, tool chaining, human-in-the-loop patterns
- **Durable Runtime prompt template** (`prompts/durable_runtime_prompt.md`) - Discovery and classification prompt with criteria for durability guarantees, cold-start benchmarks, checkpoint/recovery
- **SAPUI5 project structure** - Complete webapp folder structure with Component.js, manifest.json, views, controllers, i18n, and routing
- **RadarView with focus area cards** - Three cards (Voice AI, Agent Orchestration, Durable Runtime) with signal/noise sections using CSS Grid layout
- **Mock data and JSON model binding** - mock_radar.json with 6 sample trends, JSON model configured in manifest, controller filters data by focus area
- **Signal vs Noise classification** - Core feature to distinguish actionable technical findings from marketing hype
- `signal_evidence` and `noise_indicators` fields in Golden Contract schema
- Mock data with signal and noise examples for each focus area (6 items total)
- Historical data query support (`GET /api/radar?date=YYYY-MM-DD`)
- **LiteLLM proxy configuration** (`litellm_config.yaml`) for routing Grok API calls
- Configurable `LITELLM_BASE_URL`, `LITELLM_API_KEY`, `GROK_MODEL` environment variables

### Changed
- **AI Provider**: Switched from Grok 4 to **SAP Generative AI Hub via LiteLLM** (see https://docs.litellm.ai/docs/providers/sap)
- **Refresh cycle**: Changed from 30-minute to **daily (1-day)** batch processing
- **Golden Contract**: Added `classification`, `signal_evidence`, `noise_indicators` fields; renamed `trend_score` to `confidence_score`
- **Success criteria**: Updated to include signal/noise classification accuracy metrics
- **Prompt template**: Redesigned for signal vs noise classification with specific criteria per focus area

### Deferred
- Grok 4 direct integration - Rationale: Using SAP Generative AI Hub for enterprise-grade AI infrastructure
- 30-minute refresh cycle - Rationale: Daily batch is sufficient for PoC scope, reduces API costs
