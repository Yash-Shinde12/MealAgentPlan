# Multi-Agent Meal Planning System

A sophisticated multi-agent system that creates personalized 7-day meal plans with workout schedules, optimized for weight gain and gut health. Built for the Google/Kaggle AI Hackathon.

## 🎯 Project Overview

This system uses **four coordinated AI agents** to generate personalized meal plans:

- **Planner Agent**: Generates meal structures using LLM (mock mode for demos)
- **Recipe Worker**: Fetches gut-friendly recipes from database
- **Nutrition Verifier**: Validates calorie/macro targets for weight gain
- **Scheduler Agent**: Creates timelines and aggregated shopping lists

## ✨ Key Features

- ✅ **Multi-Agent Architecture**: 4 specialized agents coordinated by Orchestrator
- ✅ **Persistent Memory**: User profiles and plan history stored across sessions
- ✅ **Session Management**: Pause/resume capability for long-running tasks
- ✅ **Nutrition Validation**: Automated verification against weight gain goals
- ✅ **Gut-Friendly Focus**: Filters recipes based on gut health requirements
- ✅ **Shopping List Generation**: Automated aggregation with quantity estimation
- ✅ **Structured Observability**: JSON logs and CSV metrics tracking
- ✅ **Deterministic Demo Mode**: Mock LLM for reproducible demonstrations
- ✅ **Comprehensive Testing**: End-to-end test suite included

## 🏗️ Architecture

```
User Input
    ↓
OrchestratorAgent
    ├── PlannerAgent (LLM-powered)
    ├── RecipeWorker (Database tool)
    ├── NutritionVerifier (Validation)
    └── SchedulerAgent (Timeline & Shopping)
    ↓
MemoryBank (Persistence) ←→ SessionService (Ephemeral)
    ↓
Observability (Logs & Metrics)
```

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py

# Run tests
python src/tests/test_end_to_end.py

# Run simulation (no API keys needed)
python simulate.py
```

## 🚀 Quick Start

### First Time Setup

```bash
python src/main.py
```

You'll be prompted to create your profile:
- Name, age, height, weight
- Activity level (sedentary to very active)
- Wake/sleep times
- Cuisine preferences
- Food allergies and dislikes
- Gut sensitivity status

### Generate a Meal Plan

The system will:
1. **Analyze** your profile and goals
2. **Generate** 7-day meal structure with workouts
3. **Verify** nutrition meets weight gain targets
4. **Schedule** meals to optimal time slots
5. **Create** shopping list with quantities

## 📊 Output Example

```
MEAL PLAN: plan_20251120_143022

User: Yash
Target Calories: 3000 kcal/day

--- Nutrition Verification ---
Status: ✓ PASSED
Daily Calories: 2950 / 3000 kcal
Daily Protein: 95g / 90g

--- Monday ---
  08:00 - Breakfast: Idli with Coconut Chutney
          350 kcal, 10g protein, 25 min prep
  11:00 - Snack: Protein Smoothie with Nuts
          480 kcal, 28g protein, 5 min prep
  13:30 - Lunch: Rajma Chawal
          620 kcal, 20g protein, 45 min prep
  18:00 - Workout: Resistance - Upper Body (45 min)
  20:00 - Dinner: Palak Paneer with Roti
          540 kcal, 24g protein, 35 min prep

--- Shopping List (32 items) ---
  • rice: 3.5kg
  • chicken: 2.1kg
  • eggs: 14 pieces
  • milk: 1.4kg
  ...
```

## 🧪 Testing

### Run All Tests
```bash
pytest src/tests/test_end_to_end.py -v
```

### Run Simulation (Demo Mode)
```bash
python simulate.py
```

The simulation demonstrates the complete workflow without external API dependencies.

## 📁 Project Structure

```
capstone-meal-agent/
├── README.md
├── pitch.md
├── requirements.txt
├── simulate.py
├── src/
│   ├── main.py                 # CLI entrypoint
│   ├── orchestrator.py         # Main coordinator
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── planner_agent.py
│   │   ├── verifier_agent.py
│   │   ├── recipe_worker.py
│   │   └── scheduler_agent.py
│   ├── tools/
│   │   ├── recipe_db.json      # 20 Indian recipes
│   │   └── nutritions.csv      # Nutrition data
│   ├── memory/
│   │   └── memory_bank.py      # Persistent storage
│   ├── sessions/
│   │   └── session_service.py  # Session management
│   ├── observability/
│   │   └── logger.py           # Logs & metrics
│   └── tests/
│       └── test_end_to_end.py
└── writeup/
    └── writeup.md
```

## 🔧 Configuration

### Using Real LLM (Gemini)

To use Google's Gemini instead of mock responses:

1. Set environment variable:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

2. The system will automatically detect and use the real LLM

### Mock Mode (Default)

For deterministic demos and testing, the system uses mock LLM responses by default. This ensures reproducible results without API dependencies.

## 📈 Observability

The system tracks:
- **Structured Logs**: `data/logs.jsonl` (JSON lines format)
- **Metrics**: `data/metrics.csv` (plan generation time, verification rates)
- **Session State**: In-memory with persistence option

View recent activity:
```python
from src.observability.logger import Logger
logger = Logger()
print(logger.get_metrics_summary())
```

## 🎓 Course Concepts Demonstrated

| Concept | Implementation |
|---------|----------------|
| **Multi-agent systems** | 4 specialized agents with orchestration |
| **Tools** | Recipe database, nutrition CSV |
| **Sessions & Memory** | MemoryBank (persistent) + SessionService |
| **Long-running tasks** | Pause/resume session capability |
| **Observability** | Structured logging + metrics tracking |
| **Evaluation** | Nutrition verification, adherence tracking |

## 🤝 Contributing

This project was built for the Google/Kaggle AI Hackathon. Contributions and improvements are welcome!

## 📝 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Built with ❤️ for the Google/Kaggle AI Hackathon

---

**Note**: This system uses mock data and deterministic algorithms for demonstration. Replace with real recipe APIs and LLM integration for production use.
