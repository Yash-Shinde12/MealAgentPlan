import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.orchestrator import OrchestratorAgent
from src.memory.memory_bank import MemoryBank
from src.observability.logger import Logger
from src.agents.recipe_worker import RecipeWorker
from src.agents.verifier_agent import NutritionVerifierAgent
from src.agents.planner_agent import PlannerAgent
from src.agents.scheduler_agent import SchedulerAgent


class TestEndToEnd:
    """
    End-to-end tests for the multi-agent system.
    Demonstrates: Testing and quality assurance
    """
    
    def setup_method(self):
        """Set up test fixtures"""
        self.logger = Logger(
            log_file="data/test_logs.jsonl",
            metrics_file="data/test_metrics.csv"
        )
        self.memory_bank = MemoryBank(memory_file="data/test_memory.json")
        
        test_profile = {
            "name": "Test User",
            "age": 20,
            "height_cm": 168,
            "weight_kg": 45,
            "goal": "gain_weight",
            "activity_level": "moderate",
            "wake_time": "07:00",
            "sleep_time": "23:00"
        }
        
        test_preferences = {
            "cuisine": ["Indian", "South Indian"],
            "dislikes": [],
            "allergies": [],
            "gut_issues": True
        }
        
        self.memory_bank.set_user_profile(test_profile)
        self.memory_bank.set_preferences(test_preferences)
    
    def test_recipe_worker_fetches_recipes(self):
        """Test: RecipeWorker can fetch appropriate recipes"""
        worker = RecipeWorker(logger=self.logger)
        
        context = {
            "preferences": {"cuisine": ["Indian"], "allergies": [], "gut_issues": True},
            "meal_type": "breakfast",
            "calorie_target": 400
        }
        
        result = worker.execute(context)
        
        assert "recipes" in result
        assert len(result["recipes"]) > 0
        assert result["recipes"][0]["meal_type"][0] in ["breakfast", "snack"]
    
    def test_verifier_validates_nutrition(self):
        """Test: NutritionVerifier validates meal plans"""
        verifier = NutritionVerifierAgent(logger=self.logger)
        
        mock_plan = {
            "Monday": [
                {"meal": "breakfast", "cal": 450, "protein_g": 15, "ingredients": ["rice", "eggs"]},
                {"meal": "lunch", "cal": 650, "protein_g": 35, "ingredients": ["chicken", "rice"]},
                {"meal": "dinner", "cal": 600, "protein_g": 30, "ingredients": ["fish", "rice"]}
            ]
        }
        
        context = {
            "meal_plan": mock_plan,
            "user_profile": {
                "weight_kg": 45,
                "height_cm": 168,
                "age": 20,
                "goal": "gain_weight",
                "activity_level": "moderate"
            }
        }
        
        result = verifier.execute(context)
        
        assert "passed" in result
        assert "daily_calories" in result
        assert "target_calories" in result
    
    def test_planner_generates_plan(self):
        """Test: PlannerAgent generates 7-day plan"""
        worker = RecipeWorker(logger=self.logger)
        planner = PlannerAgent(worker, logger=self.logger)
        
        context = {
            "user_profile": self.memory_bank.get_user_profile(),
            "preferences": self.memory_bank.get_preferences()
        }
        
        result = planner.execute(context)
        
        assert "meal_plan" in result
        assert len(result["meal_plan"]) == 7
        assert "Monday" in result["meal_plan"]
    
    def test_scheduler_creates_shopping_list(self):
        """Test: SchedulerAgent generates shopping list"""
        scheduler = SchedulerAgent(logger=self.logger)
        
        mock_plan = {
            "Monday": [
                {"meal": "breakfast", "ingredients": ["rice", "eggs", "milk"]},
                {"meal": "lunch", "ingredients": ["chicken", "rice", "tomatoes"]}
            ],
            "Tuesday": [
                {"meal": "breakfast", "ingredients": ["oats", "milk", "banana"]},
                {"meal": "lunch", "ingredients": ["chicken", "rice"]}
            ]
        }
        
        context = {
            "meal_plan": mock_plan,
            "user_profile": self.memory_bank.get_user_profile()
        }
        
        result = scheduler.execute(context)
        
        assert "shopping_list" in result
        assert len(result["shopping_list"]) > 0
    
    def test_orchestrator_full_flow(self):
        """Test: Orchestrator coordinates all agents successfully"""
        orchestrator = OrchestratorAgent(self.memory_bank, self.logger)
        
        result = orchestrator.create_meal_plan()
        
        assert "plan_id" in result
        assert "days" in result
        assert "shopping_list" in result
        assert "verification" in result
        assert len(result["days"]) == 7
    
    def test_memory_persistence(self):
        """Test: Memory bank persists data correctly"""
        memory = MemoryBank(memory_file="data/test_memory2.json")
        
        profile = {"name": "Test", "age": 25}
        memory.set_user_profile(profile)
        
        loaded_profile = memory.get_user_profile()
        assert loaded_profile["name"] == "Test"
        
        memory.add_plan_to_history("plan_001", 0.9)
        history = memory.get_history()
        assert len(history) > 0


def run_tests():
    """Run all tests"""
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    run_tests()
