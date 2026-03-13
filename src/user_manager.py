"""
User Management Module
Handles user initialization, configuration, ID generation, etc.
"""

import json
import random
import string
from datetime import datetime
from typing import Dict, Any, Optional
from .github_api import GitHubAPI, GitHubAPIError


def generate_user_id(nickname: str) -> str:
    """
    Generate user ID
    
    Format: openclaw_{nickname_abbrev}_{random_string}
    
    Args:
        nickname: User nickname
        
    Returns:
        User ID string
    """
    # First 8 chars of nickname, lowercase, remove spaces and special chars
    nickname_short = ''.join(c.lower() for c in nickname[:8] if c.isalnum())
    if not nickname_short:
        nickname_short = "user"
    
    # Generate 6-char random string
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    return f"openclaw_{nickname_short}_{random_str}"


class UserManager:
    """User management"""
    
    def __init__(self, gh: GitHubAPI):
        """
        Initialize user manager
        
        Args:
            gh: GitHubAPI instance
        """
        self.gh = gh
    
    def init_user(self, nickname: str, country: str) -> Dict[str, Any]:
        """
        Initialize new user
        
        Args:
            nickname: User nickname
            country: Country code (e.g., CN, US)
            
        Returns:
            User configuration info
        """
        user_id = generate_user_id(nickname)
        
        # Check if user already exists
        profile_path = self.gh.get_profile_path(user_id)
        if self.gh.file_exists(profile_path):
            raise GitHubAPIError(f"User ID {user_id} already exists, please retry")
        
        # Create user profile
        profile = {
            "user_id": user_id,
            "nickname": nickname,
            "country": country.upper(),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "status": "active",
            "failed_at": None,
            "reminder_time": "20:00",
            "reminder_style": "warm",
            "max_reminders": 3
        }
        
        # Create streak stats
        streak = {
            "user_id": user_id,
            "current_streak": 0,
            "total_checkins": 0,
            "longest_streak": 0,
            "last_checkin_date": None,
            "failed_weeks": 0
        }
        
        # Write files
        try:
            self.gh.put_json(
                profile_path, 
                profile, 
                f"Init user {user_id}"
            )
            self.gh.put_json(
                self.gh.get_streak_path(user_id),
                streak,
                f"Init streak for {user_id}"
            )
        except GitHubAPIError as e:
            raise GitHubAPIError(f"Failed to initialize user: {str(e)}")
        
        return {
            "user_id": user_id,
            "nickname": nickname,
            "country": country.upper(),
            "profile_path": profile_path,
            "message": f"User initialization successful! Your user ID is: {user_id}"
        }
    
    def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user profile
        
        Args:
            user_id: User ID
            
        Returns:
            User profile dictionary, None if not exists
        """
        return self.gh.get_json(self.gh.get_profile_path(user_id))
    
    def update_profile(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user profile
        
        Args:
            user_id: User ID
            updates: Fields to update
            
        Returns:
            Updated profile
        """
        def update_func(current_data):
            current_data.update(updates)
            return current_data
        
        self.gh.update_json_with_retry(
            self.gh.get_profile_path(user_id),
            update_func,
            f"Update profile for {user_id}"
        )
        
        # Return updated profile
        return self.get_profile(user_id)
    
    def get_streak(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user streak statistics
        
        Args:
            user_id: User ID
            
        Returns:
            Statistics dictionary, None if not exists
        """
        return self.gh.get_json(self.gh.get_streak_path(user_id))
    
    def update_streak(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user streak statistics
        
        Args:
            user_id: User ID
            updates: Fields to update
            
        Returns:
            Updated statistics
        """
        def update_func(current_data):
            current_data.update(updates)
            return current_data
        
        self.gh.update_json_with_retry(
            self.gh.get_streak_path(user_id),
            update_func,
            f"Update streak for {user_id}"
        )
        
        return self.get_streak(user_id)
    
    def mark_user_failed(self, user_id: str) -> None:
        """
        Mark user task as failed
        
        Args:
            user_id: User ID
        """
        self.update_profile(user_id, {
            "status": "failed",
            "failed_at": datetime.utcnow().isoformat() + "Z"
        })
        
        # Update streak
        streak = self.get_streak(user_id)
        if streak:
            self.update_streak(user_id, {
                "failed_weeks": streak.get("failed_weeks", 0) + 1
            })
    
    def reactivate_user(self, user_id: str) -> Dict[str, Any]:
        """
        Reactivate user (rejoin after failure)
        
        Args:
            user_id: User ID
            
        Returns:
            Updated profile
        """
        # Reset streak
        self.update_streak(user_id, {
            "current_streak": 0,
            "last_checkin_date": None
        })
        
        # Activate user
        return self.update_profile(user_id, {
            "status": "active",
            "failed_at": None
        })
