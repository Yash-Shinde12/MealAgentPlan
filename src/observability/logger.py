import json
import os
import csv
from datetime import datetime
from typing import Any, Dict


class Logger:
    """
    Structured logging and metrics collection.
    Demonstrates: Observability - logging and metrics tracking
    """
    
    def __init__(self, log_file: str = "data/logs.jsonl", 
                 metrics_file: str = "data/metrics.csv"):
        self.log_file = log_file
        self.metrics_file = metrics_file
        self._ensure_files()
        self._init_metrics()
    
    def _ensure_files(self):
        """Ensure log and metrics files exist"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                pass
        
        if not os.path.exists(self.metrics_file):
            with open(self.metrics_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "metric_name", "value", "unit", "metadata"
                ])
    
    def _init_metrics(self):
        """Initialize metrics tracking"""
        self.metrics = {
            "plan_generation_time": [],
            "verifier_pass_rate": [],
            "agent_execution_time": []
        }
    
    def log(self, level: str, message: str, data: Dict[str, Any] = None):
        """
        Write structured log entry.
        Demonstrates: Observability - structured logging
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "data": data or {}
        }
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"Failed to write log: {e}")
    
    def track_metric(self, metric_name: str, value: float, unit: str = "", 
                    metadata: Dict[str, Any] = None):
        """
        Track a metric value.
        Demonstrates: Observability - metrics collection
        """
        timestamp = datetime.now().isoformat()
        
        if metric_name in self.metrics:
            self.metrics[metric_name].append({
                "timestamp": timestamp,
                "value": value,
                "metadata": metadata or {}
            })
        
        try:
            with open(self.metrics_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp,
                    metric_name,
                    value,
                    unit,
                    json.dumps(metadata or {})
                ])
        except Exception as e:
            print(f"Failed to write metric: {e}")
    
    def get_recent_logs(self, count: int = 10) -> list:
        """Get recent log entries"""
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                recent = lines[-count:] if len(lines) > count else lines
                return [json.loads(line) for line in recent]
        except Exception:
            return []
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of tracked metrics"""
        summary = {}
        for metric_name, values in self.metrics.items():
            if values:
                nums = [v["value"] for v in values]
                summary[metric_name] = {
                    "count": len(nums),
                    "average": sum(nums) / len(nums) if nums else 0,
                    "min": min(nums) if nums else 0,
                    "max": max(nums) if nums else 0
                }
        return summary
    
    def clear_old_logs(self, days: int = 30):
        """Clear logs older than specified days"""
        cutoff = datetime.now().timestamp() - (days * 24 * 3600)
        
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
            
            filtered_lines = []
            for line in lines:
                try:
                    entry = json.loads(line)
                    log_time = datetime.fromisoformat(entry["timestamp"]).timestamp()
                    if log_time >= cutoff:
                        filtered_lines.append(line)
                except Exception:
                    continue
            
            with open(self.log_file, 'w') as f:
                f.writelines(filtered_lines)
        except Exception as e:
            print(f"Failed to clear old logs: {e}")
