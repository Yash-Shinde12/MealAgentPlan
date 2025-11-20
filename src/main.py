#!/usr/bin/env python3
import json
import sys
from typing import Dict, Any
from src.orchestrator import OrchestratorAgent
from src.memory.memory_bank import MemoryBank
from src.observability.logger import Logger


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("     Multi-Agent Meal Planning System")
    print("     Weight Gain + Gut Health Optimizer")
    print("=" * 60)
    print()


def setup_user_profile(memory_bank: MemoryBank):
    """Interactive user profile setup"""
    print("\n--- User Profile Setup ---")
    print("Let's set up your profile for personalized meal planning.\n")
    
    name = input("Your name: ").strip() or "User"
    age = int(input("Your age: ").strip() or "20")
    height_cm = int(input("Your height (cm): ").strip() or "168")
    weight_kg = int(input("Your current weight (kg): ").strip() or "45")
    
    print("\nActivity Level:")
    print("1. Sedentary (little or no exercise)")
    print("2. Light (exercise 1-3 days/week)")
    print("3. Moderate (exercise 3-5 days/week)")
    print("4. Active (exercise 6-7 days/week)")
    print("5. Very Active (intense exercise daily)")
    activity_choice = input("Select (1-5): ").strip() or "3"
    activity_levels = {
        "1": "sedentary",
        "2": "light",
        "3": "moderate",
        "4": "active",
        "5": "very_active"
    }
    activity_level = activity_levels.get(activity_choice, "moderate")
    
    wake_time = input("Wake up time (HH:MM, e.g., 07:00): ").strip() or "07:00"
    sleep_time = input("Sleep time (HH:MM, e.g., 23:00): ").strip() or "23:00"
    
    profile = {
        "name": name,
        "age": age,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "goal": "gain_weight",
        "activity_level": activity_level,
        "wake_time": wake_time,
        "sleep_time": sleep_time
    }
    
    print("\n--- Preferences ---")
    cuisine_input = input("Preferred cuisines (comma-separated, e.g., Indian, South Indian): ").strip()
    cuisines = [c.strip() for c in cuisine_input.split(",")] if cuisine_input else ["Indian", "South Indian"]
    
    dislikes_input = input("Foods you dislike (comma-separated): ").strip()
    dislikes = [d.strip() for d in dislikes_input.split(",")] if dislikes_input else []
    
    allergies_input = input("Food allergies (comma-separated): ").strip()
    allergies = [a.strip() for a in allergies_input.split(",")] if allergies_input else []
    
    gut_issues = input("Do you have gut sensitivity issues? (y/n): ").strip().lower() == 'y'
    
    preferences = {
        "cuisine": cuisines,
        "dislikes": dislikes,
        "allergies": allergies,
        "gut_issues": gut_issues
    }
    
    memory_bank.set_user_profile(profile)
    memory_bank.set_preferences(preferences)
    
    print("\n✓ Profile saved successfully!")


def display_meal_plan(plan: Dict[str, Any]):
    """Display the generated meal plan"""
    print("\n" + "=" * 60)
    print(f"  MEAL PLAN: {plan['plan_id']}")
    print("=" * 60)
    
    print(f"\nUser: {plan['user']}")
    print(f"Target Calories: {plan['estimated_daily_calories']} kcal/day")
    
    verification = plan.get("verification", {})
    print(f"\n--- Nutrition Verification ---")
    print(f"Status: {'✓ PASSED' if verification.get('passed') else '✗ NEEDS ADJUSTMENT'}")
    print(f"Daily Calories: {verification.get('daily_calories', 0):.0f} / {verification.get('target_calories', 0):.0f} kcal")
    print(f"Daily Protein: {verification.get('daily_protein', 0):.0f}g / {verification.get('target_protein', 0):.0f}g")
    
    if verification.get('recommendations'):
        print("\nRecommendations:")
        for rec in verification['recommendations']:
            print(f"  • {rec}")
    
    print("\n--- 7-Day Schedule ---")
    for day, meals in plan['days'].items():
        print(f"\n{day}:")
        for meal in meals:
            time = meal.get('time', '')
            meal_type = meal.get('meal', '').replace('_', ' ').title()
            
            if meal_type == 'Workout':
                workout_type = meal.get('type', '').title()
                focus = meal.get('focus', '')
                duration = meal.get('duration_min', 0)
                print(f"  {time} - {workout_type}: {focus} ({duration} min)")
            else:
                name = meal.get('recipe_name', '')
                cal = meal.get('cal', 0)
                protein = meal.get('protein_g', 0)
                prep_time = meal.get('prep_time_min', 0)
                print(f"  {time} - {meal_type}: {name}")
                print(f"          {cal} kcal, {protein}g protein, {prep_time} min prep")
    
    print("\n--- Shopping List ---")
    shopping_list = plan.get('shopping_list', [])
    print(f"Total items: {len(shopping_list)}")
    
    for item in shopping_list[:15]:
        print(f"  • {item['item']}: {item['qty']} (used in {item['meals_used']} meals)")
    
    if len(shopping_list) > 15:
        print(f"  ... and {len(shopping_list) - 15} more items")
    
    print("\n" + "=" * 60)


def main():
    """Main CLI application"""
    print_banner()
    
    logger = Logger()
    memory_bank = MemoryBank()
    orchestrator = OrchestratorAgent(memory_bank, logger)
    
    logger.log("INFO", "Application started", {})
    
    user_profile = memory_bank.get_user_profile()
    
    if not user_profile:
        print("Welcome! It looks like this is your first time.")
        print("Let's set up your profile to create personalized meal plans.\n")
        setup_user_profile(memory_bank)
    else:
        print(f"Welcome back, {user_profile.get('name', 'User')}!")
        print("\nOptions:")
        print("1. Generate new meal plan")
        print("2. Update profile")
        print("3. View history")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == "2":
            setup_user_profile(memory_bank)
            return
        elif choice == "3":
            history = memory_bank.get_history()
            print(f"\n--- Plan History ({len(history)} plans) ---")
            for entry in history[-5:]:
                print(f"  {entry['date']} - {entry['plan_id']} (Success: {entry['success_rate']*100:.0f}%)")
            return
        elif choice == "4":
            print("Goodbye!")
            return
    
    print("\n🔄 Generating your personalized 7-day meal plan...")
    print("   This involves coordinating multiple AI agents:\n")
    print("   1️⃣  Planner Agent: Creating meal structure")
    print("   2️⃣  Recipe Worker: Fetching gut-friendly recipes")
    print("   3️⃣  Verifier Agent: Checking nutrition goals")
    print("   4️⃣  Scheduler Agent: Organizing timeline & shopping list\n")
    
    try:
        import time
        start_time = time.time()
        
        plan = orchestrator.create_meal_plan()
        
        execution_time = time.time() - start_time
        logger.track_metric("plan_generation_time", execution_time, "seconds")
        
        display_meal_plan(plan)
        
        print(f"\n✓ Plan generated in {execution_time:.2f} seconds")
        
        save = input("\nSave plan to file? (y/n): ").strip().lower()
        if save == 'y':
            filename = f"data/{plan['plan_id']}.json"
            with open(filename, 'w') as f:
                json.dump(plan, f, indent=2)
            print(f"✓ Saved to {filename}")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        logger.log("ERROR", "Plan generation failed", {"error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
