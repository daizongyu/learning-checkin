"""
Reminder Check Module
Provides reminder judgment interface (actual reminders handled locally by the user's system)
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from .github_api import GitHubAPI
from .user_manager import UserManager
from .checkin import CheckInManager


class ReminderManager:
    """Reminder management (data interface only)"""
    
    def __init__(self, gh: GitHubAPI, user_manager: UserManager, checkin_manager: CheckInManager):
        """
        Initialize reminder manager
        
        Args:
            gh: GitHubAPI instance
            user_manager: UserManager instance
            checkin_manager: CheckInManager instance
        """
        self.gh = gh
        self.user_manager = user_manager
        self.checkin_manager = checkin_manager
    
    def check_reminder(self, user_id: str, current_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Check if reminder should be sent
        
        Args:
            user_id: User ID
            current_time: Current time (defaults to now)
            
        Returns:
            Reminder judgment result
        """
        if current_time is None:
            current_time = datetime.utcnow()
        
        # Get user profile
        profile = self.user_manager.get_profile(user_id)
        if not profile:
            return {"error": "User does not exist"}
        
        # Check user status
        if profile.get("status") != "active":
            return {
                "should_remind": False,
                "reason": f"User status is {profile.get('status')}"
            }
        
        # Check if already checked in today
        checked, today = self.checkin_manager.is_checked_today(user_id)
        if checked:
            return {
                "should_remind": False,
                "reason": "Already checked in today",
                "date": today
            }
        
        # Get reminder config
        reminder_time_str = profile.get("reminder_time", "20:00")
        max_reminders = profile.get("max_reminders", 3)
        
        # Parse reminder time
        try:
            reminder_hour, reminder_minute = map(int, reminder_time_str.split(":"))
        except ValueError:
            reminder_hour, reminder_minute = 20, 0
        
        # Check if current time is past reminder time
        reminder_time = current_time.replace(
            hour=reminder_hour, 
            minute=reminder_minute, 
            second=0, 
            microsecond=0
        )
        
        if current_time < reminder_time:
            return {
                "should_remind": False,
                "reason": "Not yet reminder time",
                "reminder_time": reminder_time_str,
                "next_reminder": reminder_time.isoformat()
            }
        
        # Calculate today's reminder count (requires history query, simplified here)
        # Actual implementation needs to record each reminder
        reminder_count = 0  # TODO: Read from local or remote
        
        if reminder_count >= max_reminders:
            return {
                "should_remind": False,
                "reason": "Reached max reminder count",
                "reminder_count": reminder_count,
                "max_reminders": max_reminders
            }
        
        # Calculate reminder urgency
        hours_since_reminder = (current_time - reminder_time).total_seconds() / 3600
        urgency = "normal"
        if hours_since_reminder > 4:
            urgency = "urgent"
        elif hours_since_reminder > 2:
            urgency = "strong"
        
        return {
            "should_remind": True,
            "reason": "Not checked in and past reminder time",
            "reminder_count": reminder_count + 1,
            "max_reminders": max_reminders,
            "urgency": urgency,
            "user_config": {
                "reminder_time": reminder_time_str,
                "reminder_style": profile.get("reminder_style", "warm")
            }
        }
    
    def get_reminder_config(self, user_id: str) -> Dict[str, Any]:
        """
        Get user reminder config
        
        Args:
            user_id: User ID
            
        Returns:
            Reminder config
        """
        profile = self.user_manager.get_profile(user_id)
        
        if not profile:
            return {"error": "User does not exist"}
        
        return {
            "user_id": user_id,
            "reminder_time": profile.get("reminder_time", "20:00"),
            "reminder_style": profile.get("reminder_style", "warm"),
            "max_reminders": profile.get("max_reminders", 3),
            "timezone": profile.get("timezone", "UTC+8")
        }
    
    def should_send_final_reminder(self, user_id: str, current_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Check if final reminder should be sent (evening)
        
        Args:
            user_id: User ID
            current_time: Current time
            
        Returns:
            Judgment result
        """
        if current_time is None:
            current_time = datetime.utcnow()
        
        # Check if already checked in today
        checked, _ = self.checkin_manager.is_checked_today(user_id)
        if checked:
            return {
                "should_remind": False,
                "reason": "Already checked in today"
            }
        
        # Check if time is evening (after 22:00)
        if current_time.hour < 22:
            return {
                "should_remind": False,
                "reason": "Not yet final reminder time",
                "next_check": "22:00"
            }
        
        # Get user status
        profile = self.user_manager.get_profile(user_id)
        if profile.get("status") != "active":
            return {
                "should_remind": False,
                "reason": f"User status is {profile.get('status')}"
            }
        
        return {
            "should_remind": True,
            "reason": "Evening check-in missed, send final reminder",
            "urgency": "final",
            "message_style": "urgent"
        }
