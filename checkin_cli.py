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
        
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🎉  Welcome to Learning Check-in!  🎉                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

✅ User initialization successful!

📋 Your Profile:
   • User ID: {result['user_id']}
   • Nickname: {result['nickname']}
   • Country: {result['country']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖  Rules:

   1️⃣  Daily Check-in
      • Check in at least once per day
      • Command: python checkin_cli.py checkin
      • Optional: Add notes about what you learned

   2️⃣  Streak Tracking
      • Consecutive days are counted automatically
      • Build your learning habit!

   3️⃣  Privacy
      • All data stored locally
      • No network connection required
      • No personal information collected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀  Quick Start:

   • Daily check-in: python checkin_cli.py checkin
   • Add note: python checkin_cli.py checkin --note "Studied Python"
   • View status: python checkin_cli.py status

💡  Data Storage:
   • Windows: %APPDATA%\\learning-checkin\\
   • Linux/macOS: ~/.learning-checkin/

🎯  Ready to start?
   Run: python checkin_cli.py checkin

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        
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
        print(f"""
✅ Check-in successful!

📅 Date: {result['date']}
🔥 Streak: {result['streak']} days
📊 Total: {result['total_checkins']} days

Keep going, you're getting better! 🌟
        """)
        
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
