from datetime import datetime
from typing import Any, Dict
import os
from src.agents.planner_agent import PlannerAgent
from src.agents.verifier_agent import NutritionVerifierAgent
from src.agents.recipe_worker import RecipeWorker
from src.agents.scheduler_agent import SchedulerAgent
from src.memory.memory_bank import MemoryBank
from src.sessions.session_service import SessionService
from src.observability.logger import Logger


class OrchestratorAgent:
    """
    Main orchestrator that coordinates all sub-agents.
    Demonstrates: Multi-agent system - orchestration pattern
    """
    
    def __init__(self, memory_bank: MemoryBank, logger: Logger):
        self.memory_bank = memory_bank
        self.logger = logger
        self.session_service = SessionService(logger)
        
        self.recipe_worker = RecipeWorker(logger=logger)
        # Enable real LLM usage automatically when GEMINI_API_KEY is present
        use_real_llm = bool(os.getenv("GEMINI_API_KEY"))
        self.planner = PlannerAgent(self.recipe_worker, logger=logger, use_real_llm=use_real_llm)
        self.verifier = NutritionVerifierAgent(logger=logger)
        self.scheduler = SchedulerAgent(logger=logger)
    
    def create_meal_plan(self, user_input: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Orchestrate the creation of a complete meal plan.
        Demonstrates: Multi-agent coordination workflow
        
        Workflow:
        1. Load user profile from memory
        2. Create session context
        3. Planner generates meal structure
        4. Verifier validates nutrition
        5. Scheduler creates timeline & shopping list
        6. Save to memory & return
        """
        session_id = self.session_service.create_session()
        self.logger.log("INFO", "Starting meal plan creation", {"session_id": session_id})
        
        try:
            user_profile = self.memory_bank.get_user_profile()
            preferences = self.memory_bank.get_preferences()
            pantry = self.memory_bank.get_pantry()
            
            if user_input:
                user_profile.update(user_input.get("profile", {}))
                preferences.update(user_input.get("preferences", {}))
            
            if not user_profile:
                raise ValueError("User profile not found. Please set up profile first.")
            
            context = {
                "user_profile": user_profile,
                "preferences": preferences,
                "pantry": pantry,
                "session_id": session_id
            }
            
            self.session_service.update_session(session_id, "context", context)
            
            self.logger.log("INFO", "Step 1: Generating meal plan with Planner agent")
            planner_result = self.planner.execute(context)
            meal_plan = planner_result["meal_plan"]
            
            self.session_service.update_session(session_id, "meal_plan", meal_plan)
            
            self.logger.log("INFO", "Step 2: Verifying nutrition with Verifier agent")
            verification_context = {
                "meal_plan": meal_plan,
                "user_profile": user_profile
            }
            verification_result = self.verifier.execute(verification_context)
            
            self.session_service.update_session(session_id, "verification", verification_result)
            
            if not verification_result["passed"]:
                self.logger.log("WARNING", "Nutrition verification failed", {
                    "recommendations": verification_result["recommendations"]
                })
            
            self.logger.log("INFO", "Step 3: Scheduling meals with Scheduler agent")
            scheduler_context = {
                "meal_plan": meal_plan,
                "user_profile": user_profile
            }
            scheduler_result = self.scheduler.execute(scheduler_context)
            
            self.session_service.update_session(session_id, "schedule", scheduler_result)
            
            plan_id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            final_result = {
                "plan_id": plan_id,
                "session_id": session_id,
                "user": user_profile.get("name", "User"),
                "days": scheduler_result["scheduled_plan"],
                "shopping_list": scheduler_result["shopping_list"],
                "estimated_daily_calories": planner_result["estimated_daily_calories"],
                "verification": {
                    "passed": verification_result["passed"],
                    "daily_calories": verification_result["daily_calories"],
                    "target_calories": verification_result["target_calories"],
                    "daily_protein": verification_result["daily_protein"],
                    "target_protein": verification_result["target_protein"],
                    "recommendations": verification_result["recommendations"]
                },
                "created_at": datetime.now().isoformat()
            }
            
            self.memory_bank.add_plan_to_history(plan_id, 1.0 if verification_result["passed"] else 0.8)
            
            self.session_service.complete_session(session_id, final_result)
            
            self.logger.log("INFO", "Meal plan creation completed successfully", {
                "plan_id": plan_id,
                "verification_passed": verification_result["passed"]
            })
            
            return final_result
            
        except Exception as e:
            self.logger.log("ERROR", f"Meal plan creation failed: {str(e)}", {
                "session_id": session_id,
                "error": str(e)
            })
            self.session_service.fail_session(session_id, str(e))
            raise
    
    def get_session_state(self, session_id: str) -> Dict[str, Any]:
        """
        Get current session state (for pause/resume functionality).
        Demonstrates: Sessions & Memory - session management
        """
        return self.session_service.get_session(session_id)
    
    def resume_session(self, session_id: str) -> Dict[str, Any]:
        """
        Resume a paused session.
        Demonstrates: Long-running tasks - pause/resume capability
        """
        session = self.session_service.get_session(session_id)
        if session and session["status"] == "paused":
            self.logger.log("INFO", "Resuming session", {"session_id": session_id})
            return self.create_meal_plan()
        else:
            raise ValueError(f"Cannot resume session {session_id}")
