import uuid
from datetime import datetime
from typing import Any, Dict, Optional


class SessionService:
    """
    Manages ephemeral session state during plan creation.
    Demonstrates: Sessions & Memory - ephemeral session context with pause/resume
    """
    
    def __init__(self, logger=None):
        self.logger = logger
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self) -> str:
        """Create a new session and return session ID"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "id": session_id,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "data": {}
        }
        if self.logger:
            self.logger.log("INFO", "Session created", {"session_id": session_id})
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, key: str, value: Any):
        """Update session data"""
        if session_id in self.sessions:
            self.sessions[session_id]["data"][key] = value
            self.sessions[session_id]["updated_at"] = datetime.now().isoformat()
    
    def pause_session(self, session_id: str):
        """
        Pause a session (for long-running tasks).
        Demonstrates: Long-running tasks - pause capability
        """
        if session_id in self.sessions:
            self.sessions[session_id]["status"] = "paused"
            self.sessions[session_id]["paused_at"] = datetime.now().isoformat()
            if self.logger:
                self.logger.log("INFO", "Session paused", {"session_id": session_id})
    
    def resume_session(self, session_id: str):
        """
        Resume a paused session.
        Demonstrates: Long-running tasks - resume capability
        """
        if session_id in self.sessions:
            self.sessions[session_id]["status"] = "active"
            self.sessions[session_id]["resumed_at"] = datetime.now().isoformat()
            if self.logger:
                self.logger.log("INFO", "Session resumed", {"session_id": session_id})
    
    def complete_session(self, session_id: str, result: Any):
        """Mark session as completed"""
        if session_id in self.sessions:
            self.sessions[session_id]["status"] = "completed"
            self.sessions[session_id]["completed_at"] = datetime.now().isoformat()
            self.sessions[session_id]["result"] = result
            if self.logger:
                self.logger.log("INFO", "Session completed", {"session_id": session_id})
    
    def fail_session(self, session_id: str, error: str):
        """Mark session as failed"""
        if session_id in self.sessions:
            self.sessions[session_id]["status"] = "failed"
            self.sessions[session_id]["failed_at"] = datetime.now().isoformat()
            self.sessions[session_id]["error"] = error
            if self.logger:
                self.logger.log("ERROR", "Session failed", {
                    "session_id": session_id,
                    "error": error
                })
    
    def get_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Get all sessions"""
        return self.sessions
    
    def clear_old_sessions(self, max_age_hours: int = 24):
        """Clear old sessions older than max_age_hours"""
        now = datetime.now()
        to_remove = []
        
        for session_id, session in self.sessions.items():
            created = datetime.fromisoformat(session["created_at"])
            age_hours = (now - created).total_seconds() / 3600
            if age_hours > max_age_hours:
                to_remove.append(session_id)
        
        for session_id in to_remove:
            del self.sessions[session_id]
        
        if self.logger and to_remove:
            self.logger.log("INFO", f"Cleared {len(to_remove)} old sessions")
