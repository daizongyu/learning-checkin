"""
Learning Check-in Skill - Local Version
Stores all data locally, no network required
"""

import os
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any


def get_data_dir():
    """Get local data directory (cross-platform)"""
    if os.name == 'nt':  # Windows
        base_dir = os.environ.get('APPDATA', os.path.expanduser('~'))
        data_dir = os.path.join(base_dir, 'learning-checkin')
    else:  # Linux/macOS
        data_dir = os.path.join(os.path.expanduser('~'), '.learning-checkin')
    
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_user_config_path():
    """Get user config file path"""
    return os.path.join(get_data_dir(), 'user_config.json')


def get_users_dir():
    """Get users data directory"""
    return os.path.join(get_data_dir(), 'users')


def load_json(path: str) -> Optional[Dict[str, Any]]:
    """Load JSON file"""
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_json(path: str, data: Dict[str, Any]) -> None:
    """Save JSON file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class LocalCheckinSkill:
    """Local Learning Check-in Skill"""
    
    def __init__(self):
        self.data_dir = get_data_dir()
        self.users_dir = get_users_dir()
        os.makedirs(self.users_dir, exist_ok=True)
    
    def get_user_id_path(self, user_id: str) -> str:
        """Get user directory path"""
        return os.path.join(self.users_dir, user_id)
    
    def get_profile_path(self, user_id: str) -> str:
        """Get user profile file path"""
        return os.path.join(self.get_user_id_path(user_id), 'profile.json')
    
    def get_streak_path(self, user_id: str) -> str:
        """Get user streak file path"""
        return os.path.join(self.get_user_id_path(user_id), 'streak.json')
    
    def get_checkin_path(self, user_id: str, date: str) -> str:
        """Get check-in file path"""
        checkins_dir = os.path.join(self.get_user_id_path(user_id), 'checkins')
        os.makedirs(checkins_dir, exist_ok=True)
        return os.path.join(checkins_dir, f'{date}.json')
    
    def init_user(self, nickname: str, country: str) -> dict:
        """Initialize new user"""
        import random
        import string
        
        # Generate user ID
        nickname_short = ''.join(c.lower() for c in nickname[:8] if c.isalnum())
        if not nickname_short:
            nickname_short = "user"
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        user_id = f"local_{nickname_short}_{random_str}"
        
        # Check if user exists
        profile_path = self.get_profile_path(user_id)
        if os.path.exists(profile_path):
            raise Exception(f"User ID {user_id} already exists, please retry")
        
        # Create user profile
        profile = {
            "user_id": user_id,
            "nickname": nickname,
            "country": country.upper(),
            "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "status": "active",
            "reminder_time": "20:00",
            "reminder_style": "warm"
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
        
        # Save files
        save_json(profile_path, profile)
        save_json(self.get_streak_path(user_id), streak)
        
        # Save user config
        config = {
            "user_id": user_id,
            "nickname": nickname,
            "country": country.upper(),
            "initialized_at": datetime.now(timezone.utc).isoformat().replace('+00:00', ''),
        }
        save_json(get_user_config_path(), config)
        
        return {
            "user_id": user_id,
            "nickname": nickname,
            "country": country.upper(),
            "message": f"User initialization successful! Your user ID is: {user_id}"
        }
    
    def get_profile(self, user_id: str) -> Optional[dict]:
        """Get user profile"""
        return load_json(self.get_profile_path(user_id))
    
    def get_streak(self, user_id: str) -> Optional[dict]:
        """Get user streak stats"""
        return load_json(self.get_streak_path(user_id))
    
    def update_streak(self, user_id: str, updates: dict) -> dict:
        """Update user streak stats"""
        streak = self.get_streak(user_id)
        if streak:
            streak.update(updates)
            save_json(self.get_streak_path(user_id), streak)
        return streak
    
    def _get_today_str(self) -> str:
        """Get today's date string using local timezone"""
        # Use datetime.now() for local timezone instead of utcnow() with hardcoded offset
        return datetime.now().strftime("%Y-%m-%d")
    
    def is_checked_today(self, user_id: str) -> tuple:
        """Check if already checked in today"""
        today = self._get_today_str()
        checkin_path = self.get_checkin_path(user_id, today)
        return os.path.exists(checkin_path), today
    
    def do_checkin(self, user_id: str, note: str = "") -> dict:
        """Execute check-in"""
        today = self._get_today_str()
        checkin_path = self.get_checkin_path(user_id, today)
        
        # Check if already checked in
        if os.path.exists(checkin_path):
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
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "note": note
        }
        
        # Save check-in
        save_json(checkin_path, checkin_data)
        
        # Update streak
        streak = self.get_streak(user_id)
        last_checkin = streak.get("last_checkin_date")
        current_streak = streak.get("current_streak", 0)
        
        # Calculate new streak
        if last_checkin:
            last_date = datetime.strptime(last_checkin, "%Y-%m-%d")
            today_date = datetime.strptime(today, "%Y-%m-%d")
            if (today_date - last_date).days == 1:
                new_streak = current_streak + 1
            elif (today_date - last_date).days == 0:
                new_streak = current_streak
            else:
                new_streak = 1
        else:
            new_streak = 1
        
        # Update streak
        self.update_streak(user_id, {
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
    
    def get_status(self, user_id: str) -> dict:
        """Get check-in status"""
        today = self._get_today_str()
        checked, _ = self.is_checked_today(user_id)
        streak = self.get_streak(user_id)
        profile = self.get_profile(user_id)
        
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
