import pandas as pd
from typing import Any, Dict, List
from src.agents.base_agent import BaseAgent


class NutritionVerifierAgent(BaseAgent):
    """
    Agent that verifies meal plans meet nutritional goals and gut-health requirements.
    Demonstrates: Multi-agent system - verification and validation role
    """
    
    def __init__(self, nutrition_csv_path: str = "src/tools/nutritions.csv", logger=None):
        super().__init__("NutritionVerifier", logger)
        self.nutrition_csv_path = nutrition_csv_path
        self.nutrition_data = self._load_nutrition_data()
    
    def _load_nutrition_data(self) -> pd.DataFrame:
        """Load nutrition data from CSV"""
        try:
            return pd.read_csv(self.nutrition_csv_path)
        except FileNotFoundError:
            self.log("ERROR", f"Nutrition CSV not found: {self.nutrition_csv_path}")
            return pd.DataFrame()
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify meal plan meets nutritional requirements.
        
        Args:
            context: Contains meal_plan, user_profile, goal
            
        Returns:
            Verification results with recommendations
        """
        meal_plan = context.get("meal_plan", {})
        user_profile = context.get("user_profile", {})
        goal = user_profile.get("goal", "gain_weight")
        
        self.log("INFO", "Verifying meal plan nutrition")
        
        daily_calories = self._calculate_daily_calories(meal_plan)
        daily_protein = self._calculate_daily_protein(meal_plan)
        gut_risk_items = self._check_gut_risks(meal_plan)
        
        target_calories = self._calculate_target_calories(user_profile, goal)
        target_protein = self._calculate_target_protein(user_profile)
        
        calorie_met = daily_calories >= target_calories * 0.9
        protein_met = daily_protein >= target_protein * 0.9
        gut_safe = len(gut_risk_items) == 0
        
        verification_passed = calorie_met and protein_met and gut_safe
        
        result = {
            "passed": verification_passed,
            "daily_calories": daily_calories,
            "target_calories": target_calories,
            "calorie_met": calorie_met,
            "daily_protein": daily_protein,
            "target_protein": target_protein,
            "protein_met": protein_met,
            "gut_risk_items": gut_risk_items,
            "gut_safe": gut_safe,
            "recommendations": []
        }
        
        if not calorie_met:
            result["recommendations"].append(
                f"Increase calories by {target_calories - daily_calories:.0f} kcal to meet weight gain goal"
            )
        
        if not protein_met:
            result["recommendations"].append(
                f"Increase protein by {target_protein - daily_protein:.0f}g for muscle growth"
            )
        
        if not gut_safe:
            result["recommendations"].append(
                f"Avoid gut-risk ingredients: {', '.join(gut_risk_items)}"
            )
        
        self.log("INFO", "Verification complete", {
            "passed": verification_passed,
            "calories": f"{daily_calories}/{target_calories}",
            "protein": f"{daily_protein}g/{target_protein}g"
        })
        
        return result
    
    def _calculate_daily_calories(self, meal_plan: Dict[str, Any]) -> float:
        """Calculate total daily calories from meal plan"""
        total = 0
        for day_meals in meal_plan.values():
            if isinstance(day_meals, list):
                for meal in day_meals:
                    if "cal" in meal:
                        total += meal["cal"]
        return total / max(len(meal_plan), 1)
    
    def _calculate_daily_protein(self, meal_plan: Dict[str, Any]) -> float:
        """Calculate total daily protein from meal plan"""
        total = 0
        count = 0
        for day_meals in meal_plan.values():
            if isinstance(day_meals, list):
                for meal in day_meals:
                    if "protein_g" in meal:
                        total += meal["protein_g"]
                        count += 1
        return total / max(len(meal_plan), 1) if count > 0 else 0
    
    def _check_gut_risks(self, meal_plan: Dict[str, Any]) -> List[str]:
        """Check for gut-unfriendly ingredients"""
        risk_items = set()
        
        for day_meals in meal_plan.values():
            if isinstance(day_meals, list):
                for meal in day_meals:
                    ingredients = meal.get("ingredients", [])
                    for ingredient in ingredients:
                        ingredient_clean = ingredient.replace(" ", "_").lower()
                        nutrition_row = self.nutrition_data[
                            self.nutrition_data['food_item'] == ingredient_clean
                        ]
                        
                        if not nutrition_row.empty:
                            if not nutrition_row.iloc[0]['gut_friendly']:
                                risk_items.add(ingredient)
        
        return list(risk_items)
    
    def _calculate_target_calories(self, user_profile: Dict[str, Any], goal: str) -> float:
        """Calculate target daily calories based on user profile and goal"""
        weight_kg = user_profile.get("weight_kg", 45)
        height_cm = user_profile.get("height_cm", 168)
        age = user_profile.get("age", 20)
        activity_level = user_profile.get("activity_level", "moderate")
        
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        
        activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        
        tdee = bmr * activity_multipliers.get(activity_level, 1.55)
        
        if goal == "gain_weight":
            return tdee + 500
        elif goal == "lose_weight":
            return tdee - 500
        else:
            return tdee
    
    def _calculate_target_protein(self, user_profile: Dict[str, Any]) -> float:
        """Calculate target daily protein in grams"""
        weight_kg = user_profile.get("weight_kg", 45)
        return weight_kg * 2.0
