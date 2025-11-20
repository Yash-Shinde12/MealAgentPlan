from typing import Any, Dict, List
from collections import defaultdict
from src.agents.base_agent import BaseAgent


class SchedulerAgent(BaseAgent):
    """
    Agent that schedules meals/workouts to time slots and generates shopping lists.
    Demonstrates: Multi-agent system - scheduling and aggregation role
    """
    
    def __init__(self, logger=None):
        super().__init__("Scheduler", logger)
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule meals and generate shopping list.
        
        Args:
            context: Contains meal_plan, user_profile (wake/sleep times)
            
        Returns:
            Scheduled plan with shopping list
        """
        meal_plan = context.get("meal_plan", {})
        user_profile = context.get("user_profile", {})
        
        self.log("INFO", "Scheduling meals and generating shopping list")
        
        scheduled_plan = self._schedule_meals(meal_plan, user_profile)
        
        shopping_list = self._generate_shopping_list(meal_plan)
        
        result = {
            "scheduled_plan": scheduled_plan,
            "shopping_list": shopping_list,
            "total_items": len(shopping_list)
        }
        
        self.log("INFO", "Scheduling complete", {
            "days": len(scheduled_plan),
            "shopping_items": len(shopping_list)
        })
        
        return result
    
    def _schedule_meals(self, meal_plan: Dict[str, Any], 
                       user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule meals to appropriate time slots.
        Already scheduled in PlannerAgent, so just validate and return.
        """
        wake_time = user_profile.get("wake_time", "07:00")
        sleep_time = user_profile.get("sleep_time", "23:00")
        
        scheduled = {}
        for day, meals in meal_plan.items():
            if isinstance(meals, list):
                sorted_meals = sorted(meals, key=lambda m: m.get("time", "00:00"))
                scheduled[day] = sorted_meals
            else:
                scheduled[day] = meals
        
        return scheduled
    
    def _generate_shopping_list(self, meal_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate aggregated shopping list from all meals.
        Demonstrates: Aggregation and deduplication
        """
        ingredient_counts = defaultdict(float)
        
        for day, meals in meal_plan.items():
            if isinstance(meals, list):
                for meal in meals:
                    if "ingredients" in meal:
                        for ingredient in meal["ingredients"]:
                            ingredient_counts[ingredient] += 1
        
        shopping_list = []
        for ingredient, count in sorted(ingredient_counts.items()):
            qty = self._estimate_quantity(ingredient, count)
            shopping_list.append({
                "item": ingredient,
                "qty": qty,
                "meals_used": int(count)
            })
        
        return shopping_list
    
    def _estimate_quantity(self, ingredient: str, meal_count: float) -> str:
        """
        Estimate quantity needed for ingredient based on meal count.
        Simple heuristic estimation.
        """
        base_quantities = {
            "rice": 0.5,
            "chicken": 0.3,
            "chicken_breast": 0.25,
            "eggs": 2,
            "milk": 0.2,
            "yogurt": 0.15,
            "paneer": 0.2,
            "vegetables": 0.3,
            "potato": 0.2,
            "sweet_potato": 0.2,
            "spinach": 0.2,
            "tomatoes": 0.15,
            "banana": 1,
            "dates": 0.05,
            "almonds": 0.03,
            "cashews": 0.03,
            "coconut": 0.1,
            "ghee": 0.05,
            "olive_oil": 0.03,
            "whole_wheat_flour": 0.15,
            "moong_dal": 0.1,
            "urad_dal": 0.1,
            "lentils": 0.1,
            "chickpeas": 0.1,
            "kidney_beans": 0.1,
            "semolina": 0.1,
            "oats": 0.1
        }
        
        ingredient_clean = ingredient.replace(" ", "_").lower()
        base_qty = base_quantities.get(ingredient_clean, 0.1)
        total_kg = base_qty * meal_count
        
        if ingredient in ["eggs"]:
            return f"{int(total_kg * meal_count)} pieces"
        elif ingredient in ["banana", "dates"]:
            return f"{int(total_kg * meal_count)} pieces"
        elif total_kg < 0.1:
            return f"{int(total_kg * 1000)}g"
        elif total_kg < 1:
            return f"{int(total_kg * 1000)}g"
        else:
            return f"{total_kg:.1f}kg"
    
    def format_schedule_for_display(self, scheduled_plan: Dict[str, Any]) -> str:
        """Format schedule for user display"""
        output = []
        for day, meals in scheduled_plan.items():
            output.append(f"\n{day}:")
            if isinstance(meals, list):
                for meal in meals:
                    time = meal.get("time", "")
                    meal_type = meal.get("meal", "")
                    name = meal.get("recipe_name", meal.get("type", ""))
                    cal = meal.get("cal", meal.get("duration_min", ""))
                    output.append(f"  {time} - {meal_type}: {name} ({cal})")
        return "\n".join(output)
