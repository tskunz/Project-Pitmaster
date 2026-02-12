# The Predictive Pitmaster

A mobile-first PWA that predicts BBQ cook times using physics-based simulation and Monte Carlo uncertainty quantification. Enter your meat, smoker, and target — get P10/P50/P90 finish time estimates that update live as you log probe readings.

## How It Works

1. **1D heat diffusion** (Fourier's Law) models heat transfer through the meat
2. **Stall model** couples evaporative cooling into the physics at 140–185°F
3. **Monte Carlo engine** (1000 iterations per update) samples biological variation, smoker fluctuations, and weather to produce confidence intervals
4. **9-state machine** tracks your cook from SETUP through DONE with a 4-tier trust system

## Quickstart

### Prerequisites

- Python 3.11+
- Node.js 18+

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

The API runs at `http://localhost:8000`. Verify with:

```bash
curl http://localhost:8000/api/v1/health
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:5173` with hot reload. The Vite dev server proxies `/api` requests to the backend.

### Environment Variables (optional)

Copy `.env.example` to `backend/.env`:

```
PITMASTER_OPENWEATHER_API_KEY=your_key_here   # free tier: openweathermap.org/api
PITMASTER_DATABASE_PATH=pitmaster.db
PITMASTER_MC_ITERATIONS=5000
PITMASTER_DEFAULT_ALTITUDE_FT=0
```

The app works without an API key — weather defaults to 75°F, 5 mph wind, 50% humidity.

## Usage

1. **Setup** — Pick your protein (brisket, pork butt, ribs, chicken, etc.), enter weight/thickness, choose equipment, set smoker temp and target temp. Optionally set a dinner time for backward planning.
2. **Cook** — Log probe readings via the number pad. The app re-runs the Monte Carlo simulation on each reading and updates P10/P50/P90 estimates. Toggle **Nerd Mode** for timeline charts, stall probability gauges, and slope analysis.
3. **Report** — After finishing, view predicted vs actual temperature curves, residuals, and rate your cook.

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/cook/setup` | Create session, run initial simulation |
| POST | `/api/v1/cook/{id}/reading` | Log probe temp, advance state, re-run MC |
| POST | `/api/v1/cook/{id}/lid-open` | Log lid-open event |
| POST | `/api/v1/cook/{id}/wrap` | Log wrap decision, adjust model |
| GET | `/api/v1/cook/{id}/prediction` | Get latest cached prediction |
| GET | `/api/v1/cook/{id}/state` | Get current state + confidence |
| POST | `/api/v1/cook/{id}/finish` | End cook, compute report |
| GET | `/api/v1/cook/{id}/report` | Get post-cook report |
| GET | `/api/v1/weather` | Proxy OpenWeather |
| GET | `/api/v1/equipment/presets` | List equipment profiles |
| GET | `/api/v1/health` | Health check |

## Project Structure

```
Project Pitmaster/
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── simulation/              # Physics kernel, stall model, Monte Carlo
│   ├── state_machine/           # 9-state cook tracker + trust system
│   ├── planning/                # Backward planner, wrap intervention
│   ├── services/                # Weather, equipment, session orchestrator
│   ├── database/                # aiosqlite schema + CRUD
│   ├── routers/                 # API endpoints
│   └── tests/                   # pytest suite
├── frontend/
│   ├── src/
│   │   ├── components/          # Setup, Normal Mode, Nerd Mode, Report
│   │   ├── pages/               # SetupPage, CookPage, ReportPage
│   │   ├── hooks/               # useCookSession, usePrediction
│   │   └── api/                 # Typed API client
│   └── vite.config.ts           # Vite + PWA config
└── .env.example
```

## Running Tests

```bash
cd "Project Pitmaster"
python -m pytest backend/tests/ -v
```

## Tech Stack

**Backend:** FastAPI, NumPy, SciPy, aiosqlite, Pydantic
**Frontend:** React 18, TypeScript, Vite, Recharts, vite-plugin-pwa

## License

MIT
