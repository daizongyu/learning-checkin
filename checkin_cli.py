#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Learning Check-in CLI
Natural language interface for daily learning tracking

Usage:
    Agent calls this module programmatically
    No direct user interaction needed
"""

import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import CheckinSkill


def handle_request(action: str, params: dict = None) -> dict:
    """Handle a request from Agent"""
    if params is None:
        params = {}
    
    skill = CheckinSkill()
    
    try:
        if action == 'init':
            nickname = params.get('nickname')
            language = params.get('language', 'zh')
            result = skill.initialize_user(nickname, language)
            return {
                'success': result['success'],
                'initialized': True
            }
        
        elif action == 'checkin':
            note = params.get('note', '')
            return skill.do_checkin(note)
        
        elif action == 'status':
            return skill.get_status()
        
        elif action == 'reminder':
            hour = params.get('hour')
            return {
                'reminder': skill.generate_reminder(hour)
            }
        
        elif action == 'rules':
            if 'content' in params:
                success = skill.update_rules(params['content'])
                return {'success': success}
            else:
                return {'rules': skill.get_rules()}
        
        elif action == 'version':
            return skill.get_version_info()
        
        else:
            return {
                'success': False,
                'error': f'Unknown action: {action}'
            }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def main():
    """Main entry point for CLI usage"""
    if len(sys.argv) < 2:
        print("Learning Check-in - Natural language interface")
        print("This tool is designed to be called by an Agent.")
        print("")
        print("Available actions:")
        print("  init      - Initialize new user")
        print("  checkin   - Daily check-in")
        print("  status    - View status")
        print("  reminder  - Generate reminder")
        print("  rules     - Get/update rules")
        print("  version   - Show version info")
        return
    
    action = sys.argv[1]
    params = {}
    
    if len(sys.argv) > 2:
        try:
            params = json.loads(' '.join(sys.argv[2:]))
        except json.JSONDecodeError:
            print("Error: Invalid JSON parameters")
            return
    
    result = handle_request(action, params)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
