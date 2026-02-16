# CodeScale Research Radar

A Signal vs Noise classification tool for architectural decision support. Engineering teams can separate technically substantive tools from marketing hype.

## Overview

**Flow:** `Grok (Discovery + Classification) → SQLite → FastAPI → SAP UI5 Dashboard`

The application analyzes technology trends across three focus areas:
- **Voice AI UX** - Voice interaction technologies
- **Agent Orchestration** - AI agent frameworks and tools
- **Durable Runtime** - Workflow and runtime durability solutions

Each tool discovered is classified as **Signal** (worth evaluating) or **Noise** (skip based on hype indicators).

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | SAP UI5 1.120+, JavaScript (ES6+) |
| Backend | Python 3.11+, FastAPI |
| Database | SQLite |
| AI | LiteLLM with xAI/Grok |

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **xAI API Key** (for Grok integration)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/guilherme-segantini/demo2.git
cd demo2
```

### 2. Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The frontend will be available at `http://localhost:8080`

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template and configure
cp .env.example .env
# Edit .env and add your XAI_API_KEY

# Start the API server
uvicorn app.main:app --reload
```

The backend API will be available at `http://localhost:8000`

### 4. Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
XAI_API_KEY=your-xai-api-key-here
DATABASE_URL=sqlite:///./radar.db
```

## Usage

### Running the Application

1. **Start the backend** (Terminal 1):
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. **Start the frontend** (Terminal 2):
   ```bash
   npm start
   ```

3. Open `http://localhost:8080` in your browser

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/radar` | Returns today's signal/noise analysis |
| `GET /api/radar?date=YYYY-MM-DD` | Returns historical data for a specific date |

### Development Commands

```bash
# Frontend
npm start          # Start dev server (localhost:8080)
npm run build      # Build for production
npm run lint       # Run UI5 linter
npm test           # Run tests

# Backend
cd backend
pytest             # Run tests
uvicorn app.main:app --reload  # Start API with hot reload
```

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
│   │   └── services/          # Business logic
│   ├── tests/                 # Backend tests
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment template
├── prompts/                   # AI prompt templates
├── package.json               # npm configuration
├── ui5.yaml                   # UI5 tooling config
├── PRD.md                     # Product requirements
├── PLAN.md                    # Execution plan
├── TASKS.md                   # Task breakdown
└── CLAUDE.md                  # Agent instructions
```

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

## Classification Criteria

### Signal (Worth Evaluating)
- Published benchmarks or performance data
- Production case studies or real-world usage
- Specific technical architecture details
- Active community with technical discussions

### Noise (Skip)
- Marketing language ("revolutionary", "game-changing")
- No benchmarks or vague performance claims
- Vaporware or pre-announcement hype
- Engagement farming without substance

## Testing

### Frontend
```bash
npm run lint       # Linting
npm test           # Unit tests
```

### Backend
```bash
cd backend
pytest             # Run all tests
pytest -v          # Verbose output
pytest --cov       # With coverage
```

### UI Testing
UI testing uses **Playwright MCP** for automated browser verification. See `CLAUDE.md` for details.

## Contributing

See `CLAUDE.md` for development workflow and coding standards.

## License

MIT
