"""
Local Storage Management for Learning Check-in
All data stored locally, privacy-first design
"""

import os
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path


def get_data_dir() -> str:
    """Get local data directory (cross-platform)"""
    if os.name == 'nt':  # Windows
        base_dir = os.environ.get('APPDATA', str(Path.home()))
        data_dir = os.path.join(base_dir, 'learning-checkin')
    else:  # Linux/macOS
        data_dir = os.path.join(str(Path.home()), '.learning-checkin')
    
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_user_dir() -> str:
    """Get user-specific data directory"""
    return os.path.join(get_data_dir(), 'user')


def get_file_path(filename: str) -> str:
    """Get full path for a file in user directory"""
    user_dir = get_user_dir()
    os.makedirs(user_dir, exist_ok=True)
    return os.path.join(user_dir, filename)


def load_json(filename: str, default: Any = None) -> Any:
    """Load JSON file, return default if not exists"""
    path = get_file_path(filename)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return default
    return default


def save_json(filename: str, data: Any) -> bool:
    """Save data to JSON file"""
    path = get_file_path(filename)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False


def load_text(filename: str, default: str = "") -> str:
    """Load text file"""
    path = get_file_path(filename)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError:
            return default
    return default


def save_text(filename: str, content: str) -> bool:
    """Save text file"""
    path = get_file_path(filename)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError:
        return False


def get_today_str() -> str:
    """Get today's date string (local timezone)"""
    return datetime.now().strftime("%Y-%m-%d")


def get_timestamp() -> str:
    """Get current timestamp string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# User Profile Management
def get_user_profile() -> Optional[Dict]:
    """Get user profile"""
    return load_json('profile.json')


def save_user_profile(profile: Dict) -> bool:
    """Save user profile"""
    return save_json('profile.json', profile)


def is_user_initialized() -> bool:
    """Check if user has completed initialization"""
    profile = get_user_profile()
    return profile is not None and profile.get('initialized', False)


# Check-in History Management
def get_checkin_history() -> List[Dict]:
    """Get all check-in records"""
    return load_json('history.json', [])


def save_checkin_history(history: List[Dict]) -> bool:
    """Save check-in history"""
    return save_json('history.json', history)


def add_checkin_record(date: str, note: str = "") -> bool:
    """Add a check-in record"""
    history = get_checkin_history()
    
    # Check if already checked in today
    for record in history:
        if record.get('date') == date:
            return False
    
    # Add new record
    history.append({
        'date': date,
        'timestamp': get_timestamp(),
        'note': note,
        'completed': True
    })
    
    # Sort by date (newest first)
    history.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    return save_checkin_history(history)


def get_checkin_streak() -> int:
    """Calculate current streak"""
    history = get_checkin_history()
    if not history:
        return 0
    
    sorted_history = sorted(history, key=lambda x: x.get('date', ''), reverse=True)
    
    streak = 0
    today = datetime.now().date()
    
    for i, record in enumerate(sorted_history):
        try:
            record_date = datetime.strptime(record['date'], '%Y-%m-%d').date()
            
            if i == 0:
                if (today - record_date).days > 1:
                    break
            else:
                prev_date = datetime.strptime(sorted_history[i-1]['date'], '%Y-%m-%d').date()
                if (prev_date - record_date).days != 1:
                    break
            
            streak += 1
        except (ValueError, KeyError):
            continue
    
    return streak


def has_checked_today() -> bool:
    """Check if user has checked in today"""
    today = get_today_str()
    history = get_checkin_history()
    return any(record.get('date') == today for record in history)


def get_last_checkin_date() -> Optional[str]:
    """Get last check-in date"""
    history = get_checkin_history()
    if not history:
        return None
    
    sorted_history = sorted(history, key=lambda x: x.get('date', ''), reverse=True)
    return sorted_history[0].get('date')
