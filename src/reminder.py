"""
Smart Reminder Generation for Learning Check-in
Generates contextual reminders based on time, season, and user habits
"""

from datetime import datetime
from typing import Optional
import random


SEASONS = {
    'spring': {
        'months': [3, 4, 5],
        'themes': ['春天', '万物复苏', '新的开始', '春暖花开'],
        'encouragements': ['一年之计在于春', '春日好时光', '春天是学习的好季节']
    },
    'summer': {
        'months': [6, 7, 8],
        'themes': ['夏天', '热情似火', '充满活力', '夏日炎炎'],
        'encouragements': ['夏日炎炎也要坚持', '热情不减', '夏天是成长的好时机']
    },
    'autumn': {
        'months': [9, 10, 11],
        'themes': ['秋天', '收获季节', '金秋时节', '秋高气爽'],
        'encouragements': ['秋天是收获的季节', '春华秋实', '金秋好时光']
    },
    'winter': {
        'months': [12, 1, 2],
        'themes': ['冬天', '温暖坚持', '冬日暖阳', '寒冬腊月'],
        'encouragements': ['冬日坚持更可贵', '温暖过冬', '冬天来了春天还会远吗']
    }
}


TONE_LEVELS = {
    'morning': {
        'level': 'gentle',
        'openers': ['早上好呀', '早安', '新的一天开始啦', '早晨好'],
        'reminders': ['记得今天的学习打卡哦', '今天的学习计划别忘了', '抽空完成今天的打卡吧'],
        'encouragements': ['加油', '相信你可以的', '期待你的进步']
    },
    'afternoon': {
        'level': 'moderate',
        'openers': ['下午好', '工作学习一天了', '傍晚时分'],
        'reminders': ['今天的打卡完成了吗', '别忘了今天的学习目标', '记得抽空打卡'],
        'encouragements': ['坚持就是胜利', '再忙也要记得学习', '你很棒，继续加油']
    },
    'evening': {
        'level': 'urgent',
        'openers': ['晚上好', '一天快结束了', '睡前提醒'],
        'reminders': ['今天还没打卡呢', '马上就要过完一天了', '最后的打卡时间'],
        'encouragements': ['今天的事今天完成', '不要留遗憾', '现在打卡还来得及']
    },
    'late': {
        'level': 'strict',
        'openers': ['这么晚了', '深夜提醒', '最后一天了'],
        'reminders': ['今天必须打卡了', '马上就要明天了', '最后的机会'],
        'encouragements': ['明天要加油了', '今天不能再拖了', '坚持住']
    }
}


def get_season() -> str:
    """Get current season based on month"""
    month = datetime.now().month
    for season, info in SEASONS.items():
        if month in info['months']:
            return season
    return 'spring'


def get_time_period(hour: Optional[int] = None) -> str:
    """Get time period based on hour"""
    if hour is None:
        hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 22:
        return 'evening'
    else:
        return 'late'


def generate_reminder(
    user_name: Optional[str] = None,
    streak: int = 0,
    hour: Optional[int] = None,
    is_weekend: bool = False,
    is_holiday: bool = False
) -> str:
    """Generate a contextual reminder message"""
    time_period = get_time_period(hour)
    tone = TONE_LEVELS.get(time_period, TONE_LEVELS['morning'])
    season = get_season()
    season_info = SEASONS[season]
    
    parts = []
    
    # Greeting
    greeting = random.choice(tone['openers'])
    if user_name:
        parts.append(f"{greeting}，{user_name}！")
    else:
        parts.append(f"{greeting}！")
    
    # Seasonal context (optional)
    if random.random() > 0.7:
        season_theme = random.choice(season_info['themes'])
        parts.append(f"{season_theme}，")
    
    # Main reminder
    reminder = random.choice(tone['reminders'])
    parts.append(reminder)
    
    # Streak motivation
    if streak > 0:
        if streak < 7:
            parts.append(f"已经坚持{streak}天啦，")
        elif streak < 30:
            weeks = streak // 7
            parts.append(f"已经坚持{streak}天（{weeks}周）了，")
        else:
            months = streak // 30
            parts.append(f"太厉害了！已经坚持{streak}天（约{months}个月）了，")
        
        if time_period in ['evening', 'late']:
            parts.append("不要让连续记录断掉哦！")
        else:
            parts.append("继续保持！")
    
    # Weekend/holiday context
    if is_weekend:
        parts.append("周末也要记得学习哦～")
    elif is_holiday:
        parts.append("假期也要保持学习习惯～")
    
    # Encouragement
    encouragement = random.choice(tone['encouragements'])
    if random.random() > 0.5:
        encouragement = random.choice(season_info['encouragements'])
    parts.append(encouragement)
    
    message = " ".join(parts)
    message = message.replace("，，", "，")
    message = message.replace("。。", "。")
    
    return message


def generate_congratulations(streak: int, language: str = 'zh') -> str:
    """Generate congratulations message after check-in"""
    if language == 'zh':
        messages = [
            f"太棒了！打卡完成！🎉\n\n你已经连续坚持了 {streak} 天！\n\n每天进步一点点，积累起来就是大不同。\n明天也要继续哦，我相信你可以的！💪",
            f"恭喜你完成今天的打卡！✨\n\n连续 {streak} 天，真的很了不起！\n\n学习的路上，坚持就是胜利。\n期待明天继续见到你！🌟",
            f"打卡成功！为你点赞！👍\n\n{streak} 天的坚持，说明你真的很用心！\n\n继续保持这个节奏，你会越来越优秀的！\n明天见！😊"
        ]
        
        if streak == 7:
            messages.append(f"🎊 恭喜达成 7 天成就！\n\n一周的坚持，已经养成习惯了！\n\n继续加油，下一个目标是 14 天！💪")
        elif streak == 30:
            messages.append(f"🏆 太厉害了！30 天成就达成！\n\n一个月的坚持，你已经超越大多数人！\n\n学习已经成为你生活的一部分，继续前进！🌟")
        elif streak == 100:
            messages.append(f"👑 100 天！这是一个里程碑！\n\n一百天的坚持，你证明了自己的毅力！\n\n你是真正的学习者，为你骄傲！🎉")
        
        return random.choice(messages)
    else:
        return f"Great job! Check-in complete! 🎉\n\nYou're on a {streak}-day streak!\n\nKeep it up, you're doing amazing! 💪"
