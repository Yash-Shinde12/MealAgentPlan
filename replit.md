# Multi-Agent Meal Planning System

## Project Overview
A sophisticated multi-agent system for personalized meal planning, built for the Google/Kaggle AI Hackathon. Creates 7-day meal plans optimized for weight gain and gut health.

## Architecture
- **Multi-Agent System**: 4 specialized agents (Planner, RecipeWorker, Verifier, Scheduler)
- **Orchestrator Pattern**: Coordinates agent workflow
- **Memory Bank**: JSON-based persistent storage
- **Session Service**: Ephemeral state management
- **Observability**: Structured logging + metrics

## Key Files
- `src/main.py` - CLI entrypoint
- `src/orchestrator.py` - Main coordinator
- `src/agents/` - All agent implementations
- `src/tools/recipe_db.json` - 20 Indian recipes
- `src/tools/nutritions.csv` - Nutrition data
- `simulate.py` - Demo script (no API keys needed)

## Recent Changes (2025-11-20)
- ✅ Complete multi-agent system implemented
- ✅ 4 specialized agents (Planner, RecipeWorker, Verifier, Scheduler)
- ✅ Memory Bank with JSON persistence
- ✅ Session management (pause/resume)
- ✅ Observability (logs.jsonl, metrics.csv)
- ✅ Mock LLM mode for deterministic demos
- ✅ End-to-end test suite
- ✅ Complete documentation (README, pitch, writeup)

## User Preferences
- Focus: Weight gain + gut health
- Cuisine: Indian, South Indian
- Mock mode: Deterministic LLM responses for demos
- Target: 3000 kcal/day, 90g protein

## Tech Stack
- Python 3.11
- Google Gemini integration (optional)
- Pandas for nutrition data
- pytest for testing
- JSON/CSV for data storage

## How to Use
```bash
# Run main application
python src/main.py

# Run simulation (no API keys needed)
python simulate.py

# Run tests
python src/tests/test_end_to_end.py
```

## Course Concepts Demonstrated
1. ✅ Multi-agent systems (4 coordinated agents)
2. ✅ Tools (Recipe DB, Nutrition CSV)
3. ✅ Sessions & Memory (MemoryBank + SessionService)
4. ✅ Long-running tasks (pause/resume capability)
5. ✅ Observability (structured logs + metrics)
6. ✅ Evaluation (nutrition verification, adherence)

## Future Enhancements
- Real LLM integration with Gemini API
- Web scraping for 1000+ recipes
- Google Calendar sync
- Mobile app
- Grocery delivery API integration
