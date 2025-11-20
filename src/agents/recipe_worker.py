import json
import os
from typing import Any, Dict, List, Optional
from src.agents.base_agent import BaseAgent


class RecipeWorker(BaseAgent):
    """
    Tool agent that fetches recipes from the database.
    Demonstrates: Tools - Recipe database access
    """
    
    def __init__(self, recipe_db_path: str = "src/tools/recipe_db.json", logger=None):
        super().__init__("RecipeWorker", logger)
        self.recipe_db_path = recipe_db_path
        self.recipes = self._load_recipes()
    
    def _load_recipes(self) -> List[Dict[str, Any]]:
        """Load recipes from JSON database"""
        try:
            with open(self.recipe_db_path, 'r') as f:
                data = json.load(f)
                return data.get("recipes", [])
        except FileNotFoundError:
            self.log("ERROR", f"Recipe database not found: {self.recipe_db_path}")
            return []
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch recipes based on context requirements.
        
        Args:
            context: Contains preferences, allergies, meal_type, etc.
            
        Returns:
            Dictionary with matched recipes
        """
        preferences = context.get("preferences", {})
        meal_type = context.get("meal_type", "lunch")
        calorie_target = context.get("calorie_target", 500)
        exclude_allergens = preferences.get("allergies", [])
        preferred_cuisines = preferences.get("cuisine", [])
        gut_friendly_only = preferences.get("gut_issues", False)
        
        self.log("INFO", f"Searching recipes for {meal_type}", {
            "calorie_target": calorie_target,
            "cuisines": preferred_cuisines,
            "gut_friendly": gut_friendly_only
        })
        
        matched_recipes = []
        for recipe in self.recipes:
            if not self._matches_criteria(recipe, meal_type, exclude_allergens, 
                                         preferred_cuisines, gut_friendly_only):
                continue
            
            matched_recipes.append(recipe)
        
        matched_recipes.sort(key=lambda r: abs(r["calories"] - calorie_target))
        
        self.log("INFO", f"Found {len(matched_recipes)} matching recipes")
        
        return {
            "recipes": matched_recipes[:5],
            "total_found": len(matched_recipes)
        }
    
    def _matches_criteria(self, recipe: Dict[str, Any], meal_type: str, 
                         exclude_allergens: List[str], preferred_cuisines: List[str],
                         gut_friendly_only: bool) -> bool:
        """Check if recipe matches search criteria"""
        if meal_type not in recipe.get("meal_type", []):
            return False
        
        if any(allergen in recipe.get("allergens", []) for allergen in exclude_allergens):
            return False
        
        if preferred_cuisines and recipe.get("cuisine") not in preferred_cuisines:
            if recipe.get("cuisine") not in ["Indian", "South Indian"]:
                return False
        
        if gut_friendly_only and not recipe.get("gut_friendly", False):
            return False
        
        return True
    
    def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific recipe by ID"""
        for recipe in self.recipes:
            if recipe["id"] == recipe_id:
                return recipe
        return None
    
    def get_all_recipes(self) -> List[Dict[str, Any]]:
        """Get all recipes"""
        return self.recipes
