from abc import ABC, abstractmethod
from typing import Any, Dict
import time


class BaseAgent(ABC):
    """
    Base class for all agents in the multi-agent system.
    Demonstrates: Multi-agent system architecture pattern
    """
    
    def __init__(self, name: str, logger=None):
        self.name = name
        self.logger = logger
        self.execution_time = 0
        
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's primary task.
        
        Args:
            context: Dictionary containing input data and session context
            
        Returns:
            Dictionary containing the agent's output
        """
        pass
    
    def log(self, level: str, message: str, data: Dict[str, Any] = None):
        """Log message with structured data"""
        if self.logger:
            self.logger.log(level, f"[{self.name}] {message}", data or {})
    
    def measure_execution(self, func, *args, **kwargs):
        """Measure execution time of a function"""
        start = time.time()
        result = func(*args, **kwargs)
        self.execution_time = time.time() - start
        return result
