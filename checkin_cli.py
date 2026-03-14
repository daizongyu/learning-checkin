#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Learning Check-in CLI - Local Version

A simple local learning check-in system with streak tracking.
No network required, all data stored locally.

Usage:
    python checkin_cli.py init --nickname <name> --country <code>
    python checkin_cli.py checkin [--note <text>]
    python checkin_cli.py status

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

from local_skill import LocalCheckinSkill

# Version info
__version__ = "v2.0.0"
__repo__ = "daizongyu/learning-checkin"


def check_update():
    """
    Check for updates from GitHub (lightweight, non-blocking)
    Uses urllib (standard library) - no external dependencies
    """
    try:
        import urllib.request
        
        url = f"https://api.github.com/repos/{__repo__}/releases/latest"
        
        # Set timeout to 2 seconds, fail silently
        request = urllib.request.Request(
            url,
            headers={'User-Agent': 'Learning-Checkin-CLI'}
        )
        
        with urllib.request.urlopen(request, timeout=2) as response:
            data = json.loads(response.read())
            latest_version = data.get('tag_name', '')
            
            # Compare versions
            if latest_version and latest_version != __version__:
                print(f"\n💡 New version available: {latest_version} (current: {__version__})")
                print(f"   Update: git pull origin main")
                print(f"   Release: https://github.com/{__repo__}/releases/latest\n")
    except Exception:
        # Silently ignore any network errors
        pass


def load_user_config():
    """Load user config (local cache)"""
    from local_skill import get_user_config_path
    config_path = get_user_config_path()
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def cmd_init(args):
    """Initialize user"""
    try:
        skill = LocalCheckinSkill()
        result = skill.init_user(args.nickname, args.country)
        
        print("")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                                                           ║")
        print("║   🎉  Welcome to Learning Check-in!  🎉                  ║")
        print("║                                                           ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print("")
        print("✅ User initialization successful!")
        print("")
        print("👤 Your Profile:")
        print(f"   • User ID: {result['user_id']}")
        print(f"   • Nickname: {result['nickname']}")
        print(f"   • Country: {result['country']}")
        print("")
        print("┌───────────────────────────────────────────────────────────┐")
        print("")
        print("📋  Rules:")
        print("")
        print("   1️⃣  Daily Check-in")
        print("      • Check in at least once per day")
        print("      • Command: python checkin_cli.py checkin")
        print("      • Optional: Add notes about what you learned")
        print("")
        print("   2️⃣  Streak Tracking")
        print("      • Consecutive days are counted automatically")
        print("      • Build your learning habit!")
        print("")
        print("   3️⃣  Privacy")
        print("      • All data stored locally")
        print("      • No network connection required")
        print("      • No personal information collected")
        print("")
        print("└───────────────────────────────────────────────────────────┘")
        print("")
        print("🚀  Quick Start:")
        print("")
        print("   • Daily check-in: python checkin_cli.py checkin")
        print('   • Add note: python checkin_cli.py checkin --note "Studied Python"')
        print("   • View status: python checkin_cli.py status")
        print("")
        print("💾  Data Storage:")
        print("   • Windows: %APPDATA%\\learning-checkin\\")
        print("   • Linux/macOS: ~/.learning-checkin/")
        print("")
        print("🎯  Ready to start?")
        print("   Run: python checkin_cli.py checkin")
        print("")
        print("└───────────────────────────────────────────────────────────┘")
        print("")
        
    except Exception as e:
        print(f"❌ Initialization failed: {str(e)}")
        sys.exit(1)


def cmd_checkin(args):
    """Execute check-in"""
    config = load_user_config()
    if not config:
        print("❌ Not initialized, please run init command first")
        print("   Usage: python checkin_cli.py init --nickname <name> --country <code>")
        sys.exit(1)
    
    try:
        skill = LocalCheckinSkill()
        user_id = config['user_id']
        
        # Execute check-in
        result = skill.do_checkin(user_id, getattr(args, 'note', ''))
        
        if result.get('already_checked'):
            print(f"ℹ️  {result['message']}")
            return
        
        if not result.get('success'):
            print(f"❌ {result['message']}")
            sys.exit(1)
        
        # Output result
        print("")
        print("✅ Check-in successful!")
        print("")
        print(f"📅 Date: {result['date']}")
        print(f"🔥 Streak: {result['streak']} days")
        print(f"📊 Total: {result['total_checkins']} days")
        print("")
        print("Keep going, you're getting better! 🚀")
        print("")
        
    except Exception as e:
        print(f"❌ Check-in failed: {str(e)}")
        sys.exit(1)


def cmd_status(args):
    """View status"""
    config = load_user_config()
    if not config:
        print("❌ Not initialized, please run init command first")
        sys.exit(1)
    
    try:
        skill = LocalCheckinSkill()
        user_id = config['user_id']
        status = skill.get_status(user_id)
        
        checked_emoji = "✅" if status['checked_today'] else "❌"
        
        print("")
        print("📊 Check-in Status")
        print("")
        print(f"User: {status['nickname']} ({status['user_id']})")
        print(f"Status: {status['status']}")
        print(f"{checked_emoji} Today: {'Checked in' if status['checked_today'] else 'Not checked'}")
        print(f"🔥 Streak: {status['current_streak']} days")
        print(f"📈 Total: {status['total_checkins']} days")
        print(f"🏆 Longest: {status['longest_streak']} days")
        print("")
        
    except Exception as e:
        print(f"❌ Failed to get status: {str(e)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Learning Check-in CLI - Simple local check-in system (no network required)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python checkin_cli.py init --nickname Daisy --country CN
  python checkin_cli.py checkin
  python checkin_cli.py checkin --note "Learned Python"
  python checkin_cli.py status
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
    
    args = parser.parse_args()
    
    # Check for updates (non-blocking, runs in background)
    check_update()
    
    if args.command == 'init':
        cmd_init(args)
    elif args.command == 'checkin':
        cmd_checkin(args)
    elif args.command == 'status':
        cmd_status(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
