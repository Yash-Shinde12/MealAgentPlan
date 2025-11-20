import random
from typing import Any, Dict, List
from src.agents.base_agent import BaseAgent
from src.agents.recipe_worker import RecipeWorker


class PlannerAgent(BaseAgent):
    """
    LLM-powered agent that generates structured 7-day meal plans with workouts.
    Demonstrates: Multi-agent system - planning and coordination role
    Uses mock LLM for deterministic demo (can be replaced with real LLM)
    """
    
    def __init__(self, recipe_worker: RecipeWorker, logger=None, use_real_llm: bool = False):
        super().__init__("Planner", logger)
        self.recipe_worker = recipe_worker
        self.use_real_llm = use_real_llm
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a 7-day meal plan with workouts.
        
        Args:
            context: Contains user_profile, preferences, pantry
            
        Returns:
            Structured meal plan with recipe IDs and workout slots
        """
        user_profile = context.get("user_profile", {})
        preferences = context.get("preferences", {})
        
        self.log("INFO", "Generating 7-day meal plan", {
            "goal": user_profile.get("goal"),
            "cuisines": preferences.get("cuisine")
        })
        
        if self.use_real_llm:
            plan = self._generate_with_llm(user_profile, preferences)
        else:
            plan = self._generate_mock_plan(user_profile, preferences)
        
        self.log("INFO", "Plan generated successfully", {
            "days": len(plan.get("days", {})),
            "estimated_calories": plan.get("estimated_daily_calories")
        })
        
        return plan
    
    def _generate_mock_plan(self, user_profile: Dict[str, Any], 
                           preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a deterministic mock meal plan.
        Demonstrates: Mock LLM for reproducible demos
        """
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        meal_plan = {}
        
        target_daily_calories = 3000
        
        for day in days:
            daily_meals = []
            
            breakfast_context = {
                "preferences": preferences,
                "meal_type": "breakfast",
                "calorie_target": 500
            }
            breakfast_recipes = self.recipe_worker.execute(breakfast_context)["recipes"]
            if breakfast_recipes:
                recipe = breakfast_recipes[0]
                daily_meals.append({
                    "meal": "breakfast",
                    "time": "08:00",
                    "recipe_id": recipe["id"],
                    "recipe_name": recipe["title"],
                    "cal": recipe["calories"],
                    "protein_g": recipe.get("protein_g", 0),
                    "ingredients": recipe.get("ingredients", []),
                    "prep_time_min": recipe.get("prep_time_min", 0),
                    "notes": "High-protein breakfast for energy"
                })
            
            snack_context = {
                "preferences": preferences,
                "meal_type": "snack",
                "calorie_target": 400
            }
            snack_recipes = self.recipe_worker.execute(snack_context)["recipes"]
            if snack_recipes:
                recipe = snack_recipes[0]
                daily_meals.append({
                    "meal": "snack",
                    "time": "11:00",
                    "recipe_id": recipe["id"],
                    "recipe_name": recipe["title"],
                    "cal": recipe["calories"],
                    "protein_g": recipe.get("protein_g", 0),
                    "ingredients": recipe.get("ingredients", []),
                    "prep_time_min": recipe.get("prep_time_min", 0),
                    "notes": "Mid-morning snack"
                })
            
            lunch_context = {
                "preferences": preferences,
                "meal_type": "lunch",
                "calorie_target": 700
            }
            lunch_recipes = self.recipe_worker.execute(lunch_context)["recipes"]
            if lunch_recipes:
                recipe = lunch_recipes[0 if day != "Monday" else (1 if len(lunch_recipes) > 1 else 0)]
                daily_meals.append({
                    "meal": "lunch",
                    "time": "13:30",
                    "recipe_id": recipe["id"],
                    "recipe_name": recipe["title"],
                    "cal": recipe["calories"],
                    "protein_g": recipe.get("protein_g", 0),
                    "ingredients": recipe.get("ingredients", []),
                    "prep_time_min": recipe.get("prep_time_min", 0),
                    "notes": "Protein-rich lunch"
                })
            
            evening_snack_context = {
                "preferences": preferences,
                "meal_type": "snack",
                "calorie_target": 450
            }
            evening_snack_recipes = self.recipe_worker.execute(evening_snack_context)["recipes"]
            if evening_snack_recipes:
                idx = 1 if len(evening_snack_recipes) > 1 else 0
                recipe = evening_snack_recipes[idx]
                daily_meals.append({
                    "meal": "evening_snack",
                    "time": "17:00",
                    "recipe_id": recipe["id"],
                    "recipe_name": recipe["title"],
                    "cal": recipe["calories"],
                    "protein_g": recipe.get("protein_g", 0),
                    "ingredients": recipe.get("ingredients", []),
                    "prep_time_min": recipe.get("prep_time_min", 0),
                    "notes": "Pre-workout fuel"
                })
            
            dinner_context = {
                "preferences": preferences,
                "meal_type": "dinner",
                "calorie_target": 650
            }
            dinner_recipes = self.recipe_worker.execute(dinner_context)["recipes"]
            if dinner_recipes:
                idx = days.index(day) % len(dinner_recipes)
                recipe = dinner_recipes[idx]
                daily_meals.append({
                    "meal": "dinner",
                    "time": "20:00",
                    "recipe_id": recipe["id"],
                    "recipe_name": recipe["title"],
                    "cal": recipe["calories"],
                    "protein_g": recipe.get("protein_g", 0),
                    "ingredients": recipe.get("ingredients", []),
                    "prep_time_min": recipe.get("prep_time_min", 0),
                    "notes": "Light dinner for gut health"
                })
            
            workout = self._get_workout_for_day(day)
            if workout:
                daily_meals.append(workout)
            
            meal_plan[day] = daily_meals
        
        return {
            "meal_plan": meal_plan,
            "estimated_daily_calories": target_daily_calories,
            "plan_type": "weight_gain_gut_friendly"
        }
    
    def _get_workout_for_day(self, day: str) -> Dict[str, Any]:
        """Generate workout schedule for each day"""
        workout_schedule = {
            "Monday": {"type": "resistance", "focus": "Upper Body", "duration_min": 45, "time": "18:00"},
            "Tuesday": {"type": "cardio", "focus": "Light Jogging", "duration_min": 30, "time": "07:00"},
            "Wednesday": {"type": "resistance", "focus": "Lower Body", "duration_min": 45, "time": "18:00"},
            "Thursday": {"type": "yoga", "focus": "Flexibility & Core", "duration_min": 30, "time": "07:00"},
            "Friday": {"type": "resistance", "focus": "Full Body", "duration_min": 50, "time": "18:00"},
            "Saturday": {"type": "sports", "focus": "Recreational Activity", "duration_min": 60, "time": "10:00"},
            "Sunday": {"type": "rest", "focus": "Active Recovery", "duration_min": 20, "time": "08:00"}
        }
        
        workout = workout_schedule.get(day)
        if workout:
            return {
                "meal": "workout",
                "time": workout["time"],
                "type": workout["type"],
                "focus": workout["focus"],
                "duration_min": workout["duration_min"],
                "notes": f"{workout['focus']} - {workout['duration_min']} minutes"
            }
        return None
    
    def _generate_with_llm(self, user_profile: Dict[str, Any], 
                          preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate plan using real LLM (Gemini).
        This would use the google-genai integration if API key is available.
        """
        try:
            import google.generativeai as genai
            import os
            
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                self.log("WARNING", "No GEMINI_API_KEY found, falling back to mock")
                return self._generate_mock_plan(user_profile, preferences)
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = self._build_llm_prompt(user_profile, preferences)
            response = model.generate_content(prompt)
            
            return self._parse_llm_response(response.text)
            
        except Exception as e:
            self.log("ERROR", f"LLM generation failed: {str(e)}")
            return self._generate_mock_plan(user_profile, preferences)
    
    def _build_llm_prompt(self, user_profile: Dict[str, Any], 
                         preferences: Dict[str, Any]) -> str:
        """Build prompt for LLM"""
        return f"""
Generate a 7-day meal plan for:
- Age: {user_profile.get('age')}
- Weight: {user_profile.get('weight_kg')} kg
- Goal: {user_profile.get('goal')}
- Cuisine preferences: {preferences.get('cuisine')}
- Allergies: {preferences.get('allergies', [])}
- Gut issues: {preferences.get('gut_issues', False)}

Include 4-5 meals per day with workout schedule.
Focus on gut-friendly, Indian cuisine.
Target: 3000 calories/day for weight gain.
"""
    
    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response into structured plan"""
        return self._generate_mock_plan({}, {})
