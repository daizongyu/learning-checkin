#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Learning Check-in CLI - Local Version
v2.0.6

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

# Fix Windows console encoding for UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from local_skill import LocalCheckinSkill

# Version info
__version__ = "v2.0.7"
__repo__ = "daizongyu/learning-checkin"


def parse_version(version_str):
    """Parse version string like 'v2.0.4' into tuple (2, 0, 4)"""
    try:
        version_str = version_str.lstrip('v')
        parts = version_str.split('.')
        return tuple(int(p) for p in parts[:3])
    except (ValueError, AttributeError):
        return (0, 0, 0)


def check_update():
    """Check for updates from GitHub (2s timeout, silent fail)"""
    try:
        import urllib.request
        url = f"https://api.github.com/repos/{__repo__}/releases/latest"
        request = urllib.request.Request(url, headers={'User-Agent': 'Learning-Checkin-CLI'})
        with urllib.request.urlopen(request, timeout=2) as response:
            data = json.loads(response.read())
            latest_version = data.get('tag_name', '')
            if latest_version:
                current_ver = parse_version(__version__)
                latest_ver = parse_version(latest_version)
                if latest_ver > current_ver:
                    print(f"\n[UPDATE] New version available: {latest_version} (current: {__version__})")
                    print(f"   Run: git pull origin main")
                    print(f"   Info: https://github.com/{__repo__}/releases/latest\n")
                    return True
    except Exception:
        pass
    return False


def load_user_config():
    """Load user config from local storage"""
    from local_skill import get_user_config_path
    config_path = get_user_config_path()
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def cmd_init(args, json_output=False):
    """Initialize user"""
    try:
        skill = LocalCheckinSkill()
        result = skill.init_user(args.nickname, args.country)
        
        if json_output:
            output = {
                "type": "init_success",
                "data": {
                    "user_id": result['user_id'],
                    "nickname": result['nickname'],
                    "country": result['country'],
                    "language_hint": "zh" if result['country'].upper() in ['CN', 'TW', 'HK', 'MO', 'SG'] else "en"
                }
            }
            print(json.dumps(output, ensure_ascii=False))
            return
        
        # Human-readable output
        print("")
        print("=" * 60)
        print("  Welcome to Learning Check-in!")
        print("=" * 60)
        print("")
        print("[OK] User initialization successful!")
        print("")
        print("Your Profile:")
        print(f"  - User ID: {result['user_id']}")
        print(f"  - Nickname: {result['nickname']}")
        print(f"  - Country: {result['country']}")
        print("")
        print("-" * 60)
        print("Rules:")
        print("-" * 60)
        print("")
        print("1. Daily Check-in")
        print("   - Check in at least once per day")
        print("   - Command: python checkin_cli.py checkin")
        print("   - Optional: Add notes (--note \"text\")")
        print("")
        print("2. Streak Tracking")
        print("   - Consecutive days counted automatically")
        print("   - Build your learning habit!")
        print("")
        print("3. Privacy First")
        print("   - All data stored locally")
        print("   - No network required (core features)")
        print("   - No personal info collected")
        print("")
        print("-" * 60)
        print("Quick Start:")
        print("-" * 60)
        print("")
        print("  - Daily: python checkin_cli.py checkin")
        print("  - Note:  python checkin_cli.py checkin --note \"Learned X\"")
        print("  - Status: python checkin_cli.py status")
        print("")
        print("Data Storage:")
        print("  - Windows: %APPDATA%\\learning-checkin\\")
        print("  - Linux/macOS: ~/.learning-checkin/")
        print("")
        print("=" * 60)
        print("Ready? Run: python checkin_cli.py checkin")
        print("=" * 60)
        print("")
        
    except Exception as e:
        print(f"[ERROR] Initialization failed: {str(e)}")
        sys.exit(1)


def cmd_checkin(args):
    """Execute check-in"""
    config = load_user_config()
    if not config:
        print("[ERROR] Not initialized. Run: python checkin_cli.py init --nickname <name> --country <code>")
        sys.exit(1)
    
    try:
        skill = LocalCheckinSkill()
        user_id = config['user_id']
        result = skill.do_checkin(user_id, getattr(args, 'note', ''))
        
        if result.get('already_checked'):
            print(f"[INFO] {result['message']}")
            return
        
        if not result.get('success'):
            print(f"[ERROR] {result['message']}")
            sys.exit(1)
        
        print("")
        print("[OK] Check-in successful!")
        print("")
        print(f"  Date: {result['date']}")
        print(f"  Streak: {result['streak']} days")
        print(f"  Total: {result['total_checkins']} days")
        print("")
        print("Keep going! You're getting better!")
        print("")
        
    except Exception as e:
        print(f"[ERROR] Check-in failed: {str(e)}")
        sys.exit(1)


def cmd_status(args):
    """View status"""
    config = load_user_config()
    if not config:
        print("[ERROR] Not initialized. Run init command first.")
        sys.exit(1)
    
    try:
        skill = LocalCheckinSkill()
        user_id = config['user_id']
        status = skill.get_status(user_id)
        
        checked = "[OK]" if status['checked_today'] else "[ ]"
        
        print("")
        print("Check-in Status")
        print("=" * 40)
        print(f"User: {status['nickname']} ({status['user_id']})")
        print(f"Status: {status['status']}")
        print(f"Today: {checked} {'Checked in' if status['checked_today'] else 'Not checked'}")
        print(f"Streak: {status['current_streak']} days")
        print(f"Total: {status['total_checkins']} days")
        print(f"Longest: {status['longest_streak']} days")
        print("=" * 40)
        print("")
        
    except Exception as e:
        print(f"[ERROR] Failed to get status: {str(e)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Learning Check-in CLI - Local, privacy-first habit tracker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python checkin_cli.py init --nickname Daisy --country CN
  python checkin_cli.py checkin
  python checkin_cli.py checkin --note "Learned Python"
  python checkin_cli.py status
  python checkin_cli.py init --nickname Test --country US --json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # init
    init_p = subparsers.add_parser('init', help='Initialize new user')
    init_p.add_argument('--nickname', required=True, help='Your nickname')
    init_p.add_argument('--country', required=True, help='Country code (CN, US, UK, etc.)')
    init_p.add_argument('--json', action='store_true', help='JSON output for Agent')
    
    # checkin
    checkin_p = subparsers.add_parser('checkin', help='Daily check-in')
    checkin_p.add_argument('--note', help='Optional learning note')
    
    # status
    subparsers.add_parser('status', help='View your status')
    
    args = parser.parse_args()
    
    # Check for updates
    check_update()
    
    if args.command == 'init':
        cmd_init(args, json_output=args.json)
    elif args.command == 'checkin':
        cmd_checkin(args)
    elif args.command == 'status':
        cmd_status(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

