import json
import os
from typing import Any, Dict, Optional
from datetime import datetime


class MemoryBank:
    """
    Persistent storage for user profiles, preferences, and plan history.
    Demonstrates: Sessions & Memory - persistent user data across sessions
    """
    
    def __init__(self, memory_file: str = "data/memory.json"):
        self.memory_file = memory_file
        self._ensure_file_exists()
        self.data = self._load()
    
    def _ensure_file_exists(self):
        """Ensure memory file and directory exist"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        if not os.path.exists(self.memory_file):
            initial_data = {
                "user_profile": {},
                "preferences": {},
                "pantry": {},
                "history": []
            }
            with open(self.memory_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def _load(self) -> Dict[str, Any]:
        """Load memory from file"""
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "user_profile": {},
                "preferences": {},
                "pantry": {},
                "history": []
            }
    
    def _save(self):
        """Save memory to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Get user profile"""
        return self.data.get("user_profile", {})
    
    def set_user_profile(self, profile: Dict[str, Any]):
        """Set user profile"""
        self.data["user_profile"] = profile
        self._save()
    
    def get_preferences(self) -> Dict[str, Any]:
        """Get user preferences"""
        return self.data.get("preferences", {})
    
    def set_preferences(self, preferences: Dict[str, Any]):
        """Set user preferences"""
        self.data["preferences"] = preferences
        self._save()
    
    def get_pantry(self) -> Dict[str, Any]:
        """Get pantry items"""
        return self.data.get("pantry", {})
    
    def update_pantry(self, items: Dict[str, Any]):
        """Update pantry items"""
        pantry = self.data.get("pantry", {})
        pantry.update(items)
        self.data["pantry"] = pantry
        self._save()
    
    def add_plan_to_history(self, plan_id: str, success_rate: float = 0.0):
        """Add a plan to history"""
        history = self.data.get("history", [])
        history.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "plan_id": plan_id,
            "success_rate": success_rate
        })
        self.data["history"] = history
        self._save()
    
    def get_history(self) -> list:
        """Get plan history"""
        return self.data.get("history", [])
    
    def clear_all(self):
        """Clear all memory (use with caution)"""
        self.data = {
            "user_profile": {},
            "preferences": {},
            "pantry": {},
            "history": []
        }
        self._save()
