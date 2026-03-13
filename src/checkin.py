"""
Check-in Core Logic Module
Handles check-in, status query, history, etc.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from .github_api import GitHubAPI, GitHubAPIError
from .user_manager import UserManager


class CheckInManager:
    """Check-in management"""
    
    def __init__(self, gh: GitHubAPI, user_manager: UserManager):
        """
        Initialize check-in manager
        
        Args:
            gh: GitHubAPI instance
            user_manager: UserManager instance
        """
        self.gh = gh
        self.user_manager = user_manager
    
    def _get_today_str(self, tz_offset: int = 8) -> str:
        """
        Get today's date string (considering timezone)
        
        Args:
            tz_offset: Timezone offset (hours), 8 for China
            
        Returns:
            Date string YYYY-MM-DD
        """
        utc_now = datetime.utcnow()
        local_now = utc_now + timedelta(hours=tz_offset)
        return local_now.strftime("%Y-%m-%d")
    
    def is_checked_today(self, user_id: str, tz_offset: int = 8) -> Tuple[bool, Optional[str]]:
        """
        Check if already checked in today
        
        Args:
            user_id: User ID
            tz_offset: Timezone offset
            
        Returns:
            (Is checked in, check-in date)
        """
        today = self._get_today_str(tz_offset)
        checkin_path = self.gh.get_checkin_path(user_id, today)
        return self.gh.file_exists(checkin_path), today
    
    def do_checkin(self, user_id: str, note: str = "", tz_offset: int = 8) -> Dict[str, Any]:
        """
        Execute check-in
        
        Args:
            user_id: User ID
            note: Check-in note (optional)
            tz_offset: Timezone offset
            
        Returns:
            Check-in result
        """
        today = self._get_today_str(tz_offset)
        checkin_path = self.gh.get_checkin_path(user_id, today)
        
        # Check if already checked in
        if self.gh.file_exists(checkin_path):
            return {
                "success": False,
                "message": "Already checked in today",
                "already_checked": True
            }
        
        # Create check-in record
        checkin_data = {
            "user_id": user_id,
            "date": today,
            "checked": True,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "note": note
        }
        
        try:
            # Write check-in file
            self.gh.put_json(
                checkin_path,
                checkin_data,
                f"Checkin for {user_id} on {today}"
            )
            
            # Update streak stats
            streak = self.user_manager.get_streak(user_id)
            last_checkin = streak.get("last_checkin_date")
            current_streak = streak.get("current_streak", 0)
            
            # Calculate new streak
            if last_checkin:
                last_date = datetime.strptime(last_checkin, "%Y-%m-%d")
                today_date = datetime.strptime(today, "%Y-%m-%d")
                if (today_date - last_date).days == 1:
                    # Consecutive check-in
                    new_streak = current_streak + 1
                elif (today_date - last_date).days == 0:
                    # Already counted today (should not happen)
                    new_streak = current_streak
                else:
                    # Restart after break
                    new_streak = 1
            else:
                # First check-in
                new_streak = 1
            
            # Update streak
            self.user_manager.update_streak(user_id, {
                "current_streak": new_streak,
                "total_checkins": streak.get("total_checkins", 0) + 1,
                "last_checkin_date": today,
                "longest_streak": max(new_streak, streak.get("longest_streak", 0))
            })
            
            return {
                "success": True,
                "message": "Check-in successful",
                "date": today,
                "streak": new_streak,
                "total_checkins": streak.get("total_checkins", 0) + 1
            }
            
        except GitHubAPIError as e:
            return {
                "success": False,
                "message": f"Check-in failed: {str(e)}"
            }
    
    def get_status(self, user_id: str, tz_offset: int = 8) -> Dict[str, Any]:
        """
        Get check-in status
        
        Args:
            user_id: User ID
            tz_offset: Timezone offset
            
        Returns:
            Status info
        """
        today = self._get_today_str(tz_offset)
        checked, _ = self.is_checked_today(user_id, tz_offset)
        streak = self.user_manager.get_streak(user_id)
        profile = self.user_manager.get_profile(user_id)
        
        return {
            "user_id": user_id,
            "nickname": profile.get("nickname") if profile else "Unknown",
            "today": today,
            "checked_today": checked,
            "current_streak": streak.get("current_streak", 0) if streak else 0,
            "total_checkins": streak.get("total_checkins", 0) if streak else 0,
            "longest_streak": streak.get("longest_streak", 0) if streak else 0,
            "status": profile.get("status", "unknown") if profile else "unknown"
        }
    
    def get_history(self, user_id: str, month: Optional[str] = None, 
                    limit: int = 30) -> Dict[str, Any]:
        """
        Get check-in history
        
        Args:
            user_id: User ID
            month: Month YYYY-MM (optional, defaults to recent)
            limit: Maximum days to return
            
        Returns:
            History records
        """
        # Get streak stats
        streak = self.user_manager.get_streak(user_id)
        
        # If no month specified, return recent stats
        if month is None:
            return {
                "user_id": user_id,
                "current_streak": streak.get("current_streak", 0) if streak else 0,
                "total_checkins": streak.get("total_checkins", 0) if streak else 0,
                "last_checkin_date": streak.get("last_checkin_date") if streak else None,
                "message": "Use --month YYYY-MM to view specific month records"
            }
        
        # Get all check-in files for specified month
        # Note: This requires directory scanning, GitHub API doesn't support direct directory listing
        # Simplified: return stats only
        return {
            "user_id": user_id,
            "month": month,
            "message": "History query feature in development"
        }
