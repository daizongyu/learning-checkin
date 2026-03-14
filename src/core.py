"""
Core Logic for Learning Check-in
Main business logic and user interaction handling
"""

import json
from datetime import datetime
from typing import Optional, Dict, Any

# Import modules directly
import storage
import reminder
import version


DEFAULT_RULES_ZH = """# 我的打卡规则

## 基本信息
- 昵称：{nickname}
- 开始日期：{start_date}
- 语言：中文

## 打卡规则

### 1. 每日打卡
- 频率：每天一次
- 方式：主动告知"打卡完成"即可
- 时间：不限，完成学习后随时打卡

### 2. 提醒规则
- 如果当天未打卡，会在以下时间提醒：
  - 早上 9:00 - 温和提醒
  - 下午 5:00 - 中等提醒
  - 晚上 8:00 - 紧急提醒
- 已打卡则当天不提醒

### 3. 提醒风格
- 根据时间调整语气（晚上更严厉）
- 结合季节、节假日调整内容
- 考虑个人习惯和偏好

### 4. 鼓励机制
- 打卡成功后表扬并显示连续天数
- 特殊里程碑（7 天、30 天、100 天）有特别祝贺
- 连续中断后鼓励重新开始

## 个性化设置

### 可用时间
- 工作日：{weekday_availability}
- 周末：{weekend_availability}

### 学习目标
{learning_goals}

### 其他偏好
{other_preferences}

---

**规则版本**: 1.0
**最后更新**: {update_date}

> 提示：规则可以根据需要随时调整，告诉我你的想法即可！
"""


DEFAULT_RULES_EN = """# My Check-in Rules

## Basic Information
- Nickname: {nickname}
- Start Date: {start_date}
- Language: English

## Check-in Rules

### 1. Daily Check-in
- Frequency: Once per day
- Method: Simply say "check-in complete"
- Time: Anytime after completing learning

### 2. Reminder Rules
- If not checked in, reminders at:
  - 9:00 AM - Gentle reminder
  - 5:00 PM - Moderate reminder
  - 8:00 PM - Urgent reminder
- No reminders if already checked in

### 3. Reminder Style
- Tone adjusts based on time (stricter in evening)
- Content adapts to season and holidays
- Considers personal habits and preferences

### 4. Encouragement
- Praise and show streak after check-in
- Special congratulations for milestones (7, 30, 100 days)
- Encourage restart after breaks

## Personal Settings

### Availability
- Weekdays: {weekday_availability}
- Weekends: {weekend_availability}

### Learning Goals
{learning_goals}

### Other Preferences
{other_preferences}

---

**Rule Version**: 1.0
**Last Updated**: {update_date}

> Tip: Rules can be adjusted anytime, just let me know!
"""


class CheckinSkill:
    """Main Check-in Skill Class"""
    
    def __init__(self):
        self.version_info = version.get_version_info()
    
    def initialize_user(self, nickname: str = None, language: str = 'zh') -> Dict[str, Any]:
        """Initialize a new user (silent, no user interaction needed)"""
        if not nickname:
            nickname = '朋友'
        
        profile = {
            'nickname': nickname,
            'language': language,
            'initialized': True,
            'initialized_at': storage.get_timestamp(),
            'timezone': 'local',
            'weekday_availability': '灵活安排',
            'weekend_availability': '灵活安排',
            'learning_goals': '- 持续学习，每天进步',
            'other_preferences': '- 无特殊要求'
        }
        
        if not storage.save_user_profile(profile):
            return {
                'success': False,
                'error': 'Failed to save user profile'
            }
        
        today = storage.get_today_str()
        if language == 'zh':
            rules_content = DEFAULT_RULES_ZH.format(
                nickname=nickname,
                start_date=today,
                weekday_availability=profile['weekday_availability'],
                weekend_availability=profile['weekend_availability'],
                learning_goals=profile['learning_goals'],
                other_preferences=profile['other_preferences'],
                update_date=today
            )
        else:
            rules_content = DEFAULT_RULES_EN.format(
                nickname=nickname,
                start_date=today,
                weekday_availability=profile['weekday_availability'],
                weekend_availability=profile['weekend_availability'],
                learning_goals=profile['learning_goals'],
                other_preferences=profile['other_preferences'],
                update_date=today
            )
        
        storage.save_text('RULE.md', rules_content)
        
        update_info = version.check_update()
        
        return {
            'success': True,
            'nickname': nickname,
            'language': language,
            'update_available': update_info is not None,
            'update_info': update_info
        }
    
    def do_checkin(self, note: str = "") -> Dict[str, Any]:
        """Perform daily check-in"""
        if not storage.is_user_initialized():
            return {
                'success': False,
                'error': 'User not initialized',
                'action_required': 'initialize'
            }
        
        if storage.has_checked_today():
            return {
                'success': False,
                'already_checked': True,
                'message': '今天已经打卡过了，明天继续哦！'
            }
        
        today = storage.get_today_str()
        if not storage.add_checkin_record(today, note):
            return {
                'success': False,
                'error': 'Failed to save check-in record'
            }
        
        streak = storage.get_checkin_streak()
        
        profile = storage.get_user_profile()
        language = profile.get('language', 'zh')
        
        congrats_msg = reminder.generate_congratulations(streak, language)
        
        update_info = version.check_update()
        update_msg = ""
        if update_info:
            if language == 'zh':
                update_msg = f"\n\n💡 有新版本可用：{update_info['latest_version']}（当前：{update_info['current_version']}）\n更新：git pull origin main"
            else:
                update_msg = f"\n\n💡 New version available: {update_info['latest_version']} (current: {update_info['current_version']})\nUpdate: git pull origin main"
        
        return {
            'success': True,
            'date': today,
            'streak': streak,
            'message': congrats_msg + update_msg,
            'update_available': update_info is not None,
            'update_info': update_info
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get user's check-in status"""
        if not storage.is_user_initialized():
            return {
                'error': 'User not initialized',
                'action_required': 'initialize'
            }
        
        profile = storage.get_user_profile()
        today = storage.get_today_str()
        checked_today = storage.has_checked_today()
        streak = storage.get_checkin_streak()
        history = storage.get_checkin_history()
        last_checkin = storage.get_last_checkin_date()
        
        total_checkins = len([r for r in history if r.get('completed', False)])
        
        return {
            'nickname': profile.get('nickname', 'Unknown'),
            'language': profile.get('language', 'zh'),
            'today': today,
            'checked_today': checked_today,
            'current_streak': streak,
            'total_checkins': total_checkins,
            'last_checkin': last_checkin,
            'initialized_at': profile.get('initialized_at', ''),
            'update_available': version.check_update() is not None
        }
    
    def generate_reminder(self, hour: int = None) -> str:
        """Generate reminder message for user"""
        if storage.has_checked_today():
            return ""
        
        profile = storage.get_user_profile()
        if not profile:
            return ""
        
        nickname = profile.get('nickname', '')
        streak = storage.get_checkin_streak()
        
        return reminder.generate_reminder(
            user_name=nickname,
            streak=streak,
            hour=hour
        )
    
    def get_rules(self) -> str:
        """Get user's rules file content"""
        return storage.load_text('RULE.md', '')
    
    def update_rules(self, content: str) -> bool:
        """Update user's rules file"""
        return storage.save_text('RULE.md', content)
    
    def get_version_info(self) -> Dict[str, str]:
        """Get version information"""
        return self.version_info
