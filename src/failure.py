"""
Failure Detection Module
Handles weekly check-in failure detection
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from .github_api import GitHubAPI
from .user_manager import UserManager


class FailureManager:
    """Failure detection management"""
    
    def __init__(self, gh: GitHubAPI, user_manager: UserManager):
        """
        Initialize failure detection manager
        
        Args:
            gh: GitHubAPI instance
            user_manager: UserManager instance
        """
        self.gh = gh
        self.user_manager = user_manager
    
    def _get_week_range(self, date: Optional[datetime] = None) -> Tuple[datetime, datetime]:
        """
        Get week range for specified date (Monday to Sunday)
        
        Args:
            date: Specified date (defaults to today)
            
        Returns:
            (Monday date, Sunday date)
        """
        if date is None:
            date = datetime.utcnow()
        
        # Find Monday (weekday() returns 0-6, 0 is Monday)
        monday = date - timedelta(days=date.weekday())
        monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Sunday
        sunday = monday + timedelta(days=6)
        sunday = sunday.replace(hour=23, minute=59, second=59)
        
        return monday, sunday
    
    def _get_last_week_range(self) -> Tuple[datetime, datetime]:
        """Get last week's range"""
        today = datetime.utcnow()
        last_week = today - timedelta(days=7)
        return self._get_week_range(last_week)
    
    def check_week_failure(self, user_id: str, week_start: Optional[str] = None) -> Dict[str, Any]:
        """
        Check weekly check-in failure status
        
        Args:
            user_id: User ID
            week_start: Week start date YYYY-MM-DD (defaults to last Monday)
            
        Returns:
            Check result
        """
        # Determine week range
        if week_start:
            start_date = datetime.strptime(week_start, "%Y-%m-%d")
            monday, sunday = self._get_week_range(start_date)
        else:
            monday, sunday = self._get_last_week_range()
        
        # Check check-in status for this week
        checked_days = []
        missed_days = []
        
        current = monday
        while current <= sunday:
            date_str = current.strftime("%Y-%m-%d")
            checkin_path = self.gh.get_checkin_path(user_id, date_str)
            
            if self.gh.file_exists(checkin_path):
                checked_days.append(date_str)
            else:
                missed_days.append(date_str)
            
            current += timedelta(days=1)
        
        # Determine failure (≥2 days missed)
        failed = len(missed_days) >= 2
        
        return {
            "user_id": user_id,
            "week_start": monday.strftime("%Y-%m-%d"),
            "week_end": sunday.strftime("%Y-%m-%d"),
            "checked_days": len(checked_days),
            "missed_days": len(missed_days),
            "missed_dates": missed_days,
            "failed": failed,
            "threshold": 2
        }
    
    def check_and_mark_failure(self, user_id: str) -> Dict[str, Any]:
        """
        Check if failed last week, mark user if failed
        
        Args:
            user_id: User ID
            
        Returns:
            Check result
        """
        # Check user status first
        profile = self.user_manager.get_profile(user_id)
        if not profile:
            return {
                "error": "User does not exist"
            }
        
        if profile.get("status") == "failed":
            return {
                "user_id": user_id,
                "already_failed": True,
                "failed_at": profile.get("failed_at")
            }
        
        # Check last week
        result = self.check_week_failure(user_id)
        
        if result["failed"]:
            # Mark user as failed
            self.user_manager.mark_user_failed(user_id)
            return {
                **result,
                "marked_failed": True,
                "message": f"Missed {result['missed_days']} days last week, task failed"
            }
        else:
            return {
                **result,
                "marked_failed": False,
                "message": f"Missed {result['missed_days']} days last week, task continues"
            }
    
    def get_failure_status(self, user_id: str) -> Dict[str, Any]:
        """
        Get user failure status
        
        Args:
            user_id: User ID
            
        Returns:
            Failure status info
        """
        profile = self.user_manager.get_profile(user_id)
        
        if not profile:
            return {"error": "User does not exist"}
        
        return {
            "user_id": user_id,
            "status": profile.get("status", "unknown"),
            "failed_at": profile.get("failed_at"),
            "failed_weeks": self.user_manager.get_streak(user_id).get("failed_weeks", 0) if self.user_manager.get_streak(user_id) else 0,
            "can_rejoin": profile.get("status") == "failed"
        }
