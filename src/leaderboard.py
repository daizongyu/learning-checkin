"""
Leaderboard Module
Handles global ranking, percentile calculation, etc.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from .github_api import GitHubAPI, GitHubAPIError


class LeaderboardManager:
    """Leaderboard management"""
    
    def __init__(self, gh: GitHubAPI):
        """
        Initialize leaderboard manager
        
        Args:
            gh: GitHubAPI instance
        """
        self.gh = gh
    
    def get_leaderboard(self) -> Optional[Dict[str, Any]]:
        """
        Get global leaderboard
        
        Returns:
            Leaderboard data, None if not exists
        """
        return self.gh.get_json(self.gh.get_leaderboard_path())
    
    def get_user_rank(self, user_id: str, current_streak: int) -> Dict[str, Any]:
        """
        Get user ranking (calculated from local cache)
        
        Args:
            user_id: User ID
            current_streak: User's current streak
            
        Returns:
            Ranking info
        """
        leaderboard = self.get_leaderboard()
        
        if not leaderboard:
            return {
                "rank": None,
                "percentile": None,
                "total_users": 0,
                "message": "Leaderboard data temporarily unavailable"
            }
        
        rankings = leaderboard.get("rankings", [])
        total_users = leaderboard.get("total_users", len(rankings))
        
        # Find user rank
        user_rank = None
        users_above = 0
        
        for i, entry in enumerate(rankings):
            if entry.get("user_id") == user_id:
                user_rank = i + 1
                break
            if entry.get("current_streak", 0) > current_streak:
                users_above += 1
        
        # If user not in leaderboard, estimate rank based on streak
        if user_rank is None:
            user_rank = users_above + 1
        
        # Calculate percentile (percentage of users beaten)
        percentile = ((total_users - user_rank) / total_users * 100) if total_users > 0 else 0
        
        return {
            "rank": user_rank,
            "percentile": round(percentile, 1),
            "total_users": total_users,
            "current_streak": current_streak
        }
    
    def format_rank_message(self, rank_info: Dict[str, Any]) -> str:
        """
        Format ranking message
        
        Args:
            rank_info: Ranking info
            
        Returns:
            Formatted message string
        """
        if rank_info.get("rank") is None:
            return "Ranking data temporarily unavailable"
        
        rank = rank_info["rank"]
        percentile = rank_info["percentile"]
        total = rank_info["total_users"]
        streak = rank_info["current_streak"]
        
        if rank == 1:
            rank_emoji = "🏆"
            rank_text = "Global Rank #1!"
        elif rank <= 10:
            rank_emoji = "🥇"
            rank_text = f"Global Rank #{rank}!"
        elif rank <= 100:
            rank_emoji = "🌟"
            rank_text = f"Global Rank #{rank}"
        else:
            rank_emoji = "📊"
            rank_text = f"Global Rank #{rank}"
        
        return f"{rank_emoji} {rank_text}, beat {percentile}% of learners! (Total: {total}, Streak: {streak} days)"
    
    def get_top_users(self, limit: int = 10, country: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get top users list
        
        Args:
            limit: Number to return
            country: Country code filter (optional)
            
        Returns:
            Top users list
        """
        leaderboard = self.get_leaderboard()
        
        if not leaderboard:
            return []
        
        rankings = leaderboard.get("rankings", [])
        
        # Country filter
        if country:
            rankings = [r for r in rankings if r.get("country") == country.upper()]
        
        return rankings[:limit]
    
    def format_leaderboard_message(self, top_users: List[Dict[str, Any]], 
                                   country: Optional[str] = None) -> str:
        """
        Format leaderboard message
        
        Args:
            top_users: Top users list
            country: Country code
            
        Returns:
            Formatted leaderboard message
        """
        if not top_users:
            return "Leaderboard data temporarily unavailable"
        
        region = f"{country} Region" if country else "Global"
        lines = [f"🏆 {region} Check-in Leaderboard Top 10\n"]
        
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        for i, user in enumerate(top_users[:10]):
            medal = medals[i] if i < len(medals) else f"{i+1}."
            nickname = user.get("nickname", "Unknown")
            streak = user.get("current_streak", 0)
            total = user.get("total_checkins", 0)
            lines.append(f"{medal} {nickname}: {streak} days streak (Total: {total} days)")
        
        return "\n".join(lines)
