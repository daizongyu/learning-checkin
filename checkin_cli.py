#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Learning Check-in CLI

A global learning check-in system with streak tracking, leaderboard, and failure detection.

Usage:
    python checkin_cli.py init --nickname <name> --country <code>
    python checkin_cli.py checkin [--note <text>]
    python checkin_cli.py status
    python checkin_cli.py leaderboard [--country <code>]
    python checkin_cli.py rank
    python checkin_cli.py check-update

Platform: Windows, Linux, macOS
Python: 3.8+
"""

import sys
import os
import json
import argparse
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from github_api import GitHubAPI, GitHubAPIError
from user_manager import UserManager
from checkin import CheckInManager
from leaderboard import LeaderboardManager
from __init__ import DEFAULT_TOKEN, DEFAULT_REPO


# Config file path (cross-platform)
def get_config_path():
    """Get user config file path (cross-platform)"""
    if os.name == 'nt':  # Windows
        config_dir = os.path.join(os.environ.get('APPDATA', ''), 'learning-checkin')
    else:  # Linux/macOS
        config_dir = os.path.join(os.path.expanduser('~'), '.learning-checkin')
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
    
    return os.path.join(config_dir, 'config.json')


def load_user_config():
    """Load user config (local cache)"""
    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_user_config(config):
    """Save user config"""
    config_path = get_config_path()
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def cmd_init(args):
    """Initialize user (centralized repo - no token needed from user)"""
    try:
        gh = GitHubAPI(DEFAULT_TOKEN, DEFAULT_REPO)
        user_manager = UserManager(gh)
        
        result = user_manager.init_user(args.nickname, args.country)
        
        # Save config (no need to store repo and token)
        config = {
            "user_id": result["user_id"],
            "nickname": args.nickname,
            "country": args.country,
            "initialized_at": datetime.utcnow().isoformat()
        }
        save_user_config(config)
        
        # Welcome message with rules
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🎉  Welcome to Learning Check-in System!  🎉           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

✅ User initialization successful!

📋 Your Profile:
   • User ID: {result['user_id']}
   • Nickname: {result['nickname']}
   • Country: {result['country']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖  Learning Check-in Rules:

   1️⃣  Daily Check-in
      • Check in at least once per day
      • Command: python checkin_cli.py checkin
      • Optional: Add notes about what you learned

   2️⃣  Streak Tracking
      • Consecutive days are counted automatically
      • Build your learning habit!

   3️⃣  Failure Rule
      • If you miss ≥2 days in a week, the task fails
      • Don't worry! You can rejoin anytime

   4️⃣  Global Leaderboard
      • Compete with learners worldwide
      • View rankings: python checkin_cli.py leaderboard
      • Filter by country: python checkin_cli.py leaderboard --country CN

   5️⃣  Privacy
      • Your User ID is anonymous
      • Only nickname is displayed publicly
      • No personal information is stored

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀  Quick Start:

   • Daily check-in: python checkin_cli.py checkin
   • Add note: python checkin_cli.py checkin --note "Studied Python"
   • View status: python checkin_cli.py status
   • View ranking: python checkin_cli.py rank
   • Leaderboard: python checkin_cli.py leaderboard

💡  Tips:
   • No GitHub account needed!
   • Works on Windows, Linux, and macOS
   • Your data is stored in a public GitHub repository

🎯  Ready to start your learning journey?
   Run: python checkin_cli.py checkin

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        
    except GitHubAPIError as e:
        print(f"❌ Initialization failed: {str(e)}")
        sys.exit(1)


def check_for_updates():
    """Check for updates silently (called on each command)"""
    try:
        from updater import get_update_check_result
        result = get_update_check_result()
        
        if result.get('has_update'):
            print(f"\n📦 Update available: v{result['local_version']} → v{result['remote_version']}")
            print(f"   Changelog: {result.get('remote_changelog', 'Bug fixes and improvements')}")
            print(f"   Please download the latest version from the repository.\n")
    except Exception:
        # Silently ignore update check errors
        pass


def cmd_checkin(args):
    """Execute check-in"""
    config = load_user_config()
    if not config:
        print("❌ Not initialized, please run init command first")
        print("   Usage: python checkin_cli.py init --nickname <name> --country <code>")
        sys.exit(1)
    
    # Check for updates
    check_for_updates()
    
    try:
        gh = GitHubAPI(DEFAULT_TOKEN, DEFAULT_REPO)
        user_manager = UserManager(gh)
        checkin_manager = CheckInManager(gh, user_manager)
        leaderboard_manager = LeaderboardManager(gh)
        
        user_id = config['user_id']
        
        # Execute check-in
        result = checkin_manager.do_checkin(user_id, getattr(args, 'note', ''))
        
        if result.get('already_checked'):
            print(f"ℹ️  {result['message']}")
            return
        
        if not result.get('success'):
            print(f"❌ {result['message']}")
            sys.exit(1)
        
        # Get ranking
        streak = result['streak']
        rank_info = leaderboard_manager.get_user_rank(user_id, streak)
        rank_msg = leaderboard_manager.format_rank_message(rank_info)
        
        # Output result
        print(f"""
✅ Check-in successful!

📅 Date: {result['date']}
🔥 Streak: {streak} days
📊 Total: {result['total_checkins']} days
{rank_msg}

Keep going, you're getting better! 🌟
        """)
        
    except GitHubAPIError as e:
        print(f"❌ Check-in failed: {str(e)}")
        sys.exit(1)


def cmd_status(args):
    """View status"""
    config = load_user_config()
    if not config:
        print("❌ Not initialized, please run init command first")
        sys.exit(1)
    
    # Check for updates
    check_for_updates()
    
    try:
        gh = GitHubAPI(DEFAULT_TOKEN, DEFAULT_REPO)
        user_manager = UserManager(gh)
        checkin_manager = CheckInManager(gh, user_manager)
        
        user_id = config['user_id']
        status = checkin_manager.get_status(user_id)
        
        checked_emoji = "✅" if status['checked_today'] else "⏳"
        
        print(f"""
📊 Check-in Status

User: {status['nickname']} ({status['user_id']})
Status: {status['status']}
{checked_emoji} Today: {'Checked in' if status['checked_today'] else 'Not checked'}
🔥 Streak: {status['current_streak']} days
📈 Total: {status['total_checkins']} days
🏆 Longest: {status['longest_streak']} days
        """)
        
    except GitHubAPIError as e:
        print(f"❌ Failed to get status: {str(e)}")
        sys.exit(1)


def cmd_leaderboard(args):
    """View leaderboard"""
    config = load_user_config()
    if not config:
        print("❌ Not initialized, please run init command first")
        sys.exit(1)
    
    try:
        gh = GitHubAPI(DEFAULT_TOKEN, DEFAULT_REPO)
        leaderboard_manager = LeaderboardManager(gh)
        
        country = getattr(args, 'country', None)
        top_users = leaderboard_manager.get_top_users(10, country)
        
        if not top_users:
            print("ℹ️  Leaderboard data temporarily unavailable")
            return
        
        msg = leaderboard_manager.format_leaderboard_message(top_users, country)
        print(msg)
        
    except GitHubAPIError as e:
        print(f"❌ Failed to get leaderboard: {str(e)}")
        sys.exit(1)


def cmd_rank(args):
    """View your ranking"""
    config = load_user_config()
    if not config:
        print("❌ Not initialized, please run init command first")
        sys.exit(1)
    
    try:
        gh = GitHubAPI(DEFAULT_TOKEN, DEFAULT_REPO)
        user_manager = UserManager(gh)
        leaderboard_manager = LeaderboardManager(gh)
        
        user_id = config['user_id']
        streak = user_manager.get_streak(user_id)
        current_streak = streak.get('current_streak', 0) if streak else 0
        
        rank_info = leaderboard_manager.get_user_rank(user_id, current_streak)
        msg = leaderboard_manager.format_rank_message(rank_info)
        
        print(f"📊 Your Ranking\n\n{msg}")
        
    except GitHubAPIError as e:
        print(f"❌ Failed to get ranking: {str(e)}")
        sys.exit(1)


def cmd_check_update(args):
    """Check for updates"""
    from updater import get_update_check_result
    
    result = get_update_check_result()
    
    if result.get('has_update'):
        print(f"""
📦 New version available!

Local version: {result['local_version']}
Latest version: {result['remote_version']}
Changelog: {result.get('remote_changelog', 'Unknown')}

Please download the latest version from the repository.
        """)
    else:
        print(f"✅ Already latest version (v{result['local_version']})")


def main():
    parser = argparse.ArgumentParser(
        description='Learning Check-in CLI - Global learning check-in system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python checkin_cli.py init --nickname Daisy --country CN
  python checkin_cli.py checkin
  python checkin_cli.py checkin --note "Learned Python"
  python checkin_cli.py status
  python checkin_cli.py leaderboard
  python checkin_cli.py leaderboard --country US
  python checkin_cli.py rank
  python checkin_cli.py check-update
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # init command
    init_parser = subparsers.add_parser('init', help='Initialize new user')
    init_parser.add_argument('--nickname', required=True, help='User nickname')
    init_parser.add_argument('--country', required=True, help='Country code (e.g., CN, US, UK)')
    
    # checkin command
    checkin_parser = subparsers.add_parser('checkin', help='Check in for today')
    checkin_parser.add_argument('--note', help='Check-in note (optional)')
    
    # status command
    subparsers.add_parser('status', help='View current check-in status')
    
    # leaderboard command
    leaderboard_parser = subparsers.add_parser('leaderboard', help='View global leaderboard')
    leaderboard_parser.add_argument('--country', help='Filter by country code (e.g., CN, US)')
    
    # rank command
    subparsers.add_parser('rank', help='View your ranking')
    
    # check-update command
    subparsers.add_parser('check-update', help='Check for Skill updates')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        cmd_init(args)
    elif args.command == 'checkin':
        cmd_checkin(args)
    elif args.command == 'status':
        cmd_status(args)
    elif args.command == 'leaderboard':
        cmd_leaderboard(args)
    elif args.command == 'rank':
        cmd_rank(args)
    elif args.command == 'check-update':
        cmd_check_update(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
