#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Learning Check-in Skill
A skill to help users build daily learning habits through check-ins and reminders.
"""

import os
import sys

# Fix Windows console encoding for UTF-8
if sys.platform == "win32":
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

import json
import datetime
import threading
import time
import re
import urllib.request
import urllib.error

# Configuration
VERSION = "1.0.0"
GITHUB_REPO = "daizongyu/learning-checkin"
DEFAULT_DATA_DIR = os.path.join(os.path.expanduser("~"), "workspace", "learning-checkin")

# Fallback to D:\workspace on Windows if ~/workspace doesn't exist
if sys.platform == "win32":
    alt_path = "D:\\workspace\\learning-checkin"
    if os.path.exists("D:\\workspace") and not os.path.exists(DEFAULT_DATA_DIR):
        DEFAULT_DATA_DIR = alt_path

DATA_DIR = os.path.normpath(DEFAULT_DATA_DIR)
RULE_FILE = os.path.join(DATA_DIR, "rule.md")
RECORDS_FILE = os.path.join(DATA_DIR, "records.json")
VERSION_FILE = os.path.join(DATA_DIR, "version.txt")
REMINDER_LOG_FILE = os.path.join(DATA_DIR, "reminder_log.json")

# Default reminder times (24-hour format)
DEFAULT_REMINDER_TIMES = ["09:00", "17:00", "20:00"]

# Reminder messages by time of day
DEFAULT_MESSAGES = {
    "09:00": [
        "Good morning! Don't forget your daily learning check-in today! 🌅",
        "Morning check-in! Start your day with learning! ☀️",
        "Hey! Time to check in for today's learning session! 📚"
    ],
    "17:00": [
        "Afternoon reminder: Have you checked in your learning today? 🕔",
        "It's {time}! Don't forget your daily check-in! 💪",
        "Time to log your learning progress for today! 🌤️"
    ],
    "20:00": [
        "It's getting late! Have you completed your learning check-in? 🌙",
        "Final reminder: Don't forget to check in your learning today! 🔥",
        "Last call for today's learning check-in! Don't miss your streak! ⭐"
    ]
}


def ensure_dir():
    """Ensure data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


def load_records():
    """Load check-in records."""
    if not os.path.exists(RECORDS_FILE):
        return {"checkins": []}
    try:
        with open(RECORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"checkins": []}


def save_records(records):
    """Save check-in records."""
    ensure_dir()
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def load_rules():
    """Load user rules from rule.md."""
    if not os.path.exists(RULE_FILE):
        return None
    try:
        with open(RULE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except IOError:
        return None


def load_reminder_log():
    """Load reminder log."""
    if not os.path.exists(REMINDER_LOG_FILE):
        return {}
    try:
        with open(REMINDER_LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_reminder_log(log_data):
    """Save reminder log."""
    ensure_dir()
    with open(REMINDER_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)


def get_today():
    """Get today's date string."""
    return datetime.datetime.now().strftime("%Y-%m-%d")


def is_checked_in_today():
    """Check if user has already checked in today."""
    records = load_records()
    today = get_today()
    for checkin in records.get("checkins", []):
        if checkin.get("date") == today:
            return True
    return False


def get_streak():
    """Calculate current check-in streak."""
    records = load_records()
    checkins = records.get("checkins", [])

    if not checkins:
        return 0

    # Sort by date descending
    sorted_checkins = sorted(checkins, key=lambda x: x.get("date", ""), reverse=True)

    streak = 0
    today = datetime.datetime.now()
    expected_date = today.strftime("%Y-%m-%d")

    # Check if checked in today
    if sorted_checkins and sorted_checkins[0].get("date") == expected_date:
        streak = 1
        expected_date = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # Count consecutive days
    for checkin in sorted_checkins[1:]:
        checkin_date = checkin.get("date", "")
        if checkin_date == expected_date:
            streak += 1
            expected_date = (datetime.datetime.strptime(expected_date, "%Y-%m-%d") - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            break

    return streak


def do_checkin():
    """Perform check-in."""
    if is_checked_in_today():
        return {
            "success": False,
            "message": "You have already checked in today! Great job! 🎉",
            "streak": get_streak()
        }

    now = datetime.datetime.now()
    checkin_record = {
        "date": now.strftime("%Y-%m-%d"),
        "timestamp": now.isoformat()
    }

    records = load_records()
    records["checkins"].append(checkin_record)
    save_records(records)

    streak = get_streak()

    return {
        "success": True,
        "message": f"Check-in successful! You're on a {streak}-day streak! 🌟",
        "streak": streak,
        "date": checkin_record["date"]
    }


def get_status():
    """Get current check-in status."""
    today_checked = is_checked_in_today()
    streak = get_streak()
    records = load_records()
    total_checkins = len(records.get("checkins", []))

    return {
        "checked_in_today": today_checked,
        "streak": streak,
        "total_checkins": total_checkins,
        "today": get_today()
    }


def check_version_async(callback):
    """Check for new version in background."""
    def _check():
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            req = urllib.request.Request(url, headers={"User-Agent": "Learning-Checkin-Skill"})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                latest_version = data.get("tag_name", "").strip("v")
                if latest_version and compare_versions(latest_version, VERSION) > 0:
                    callback({
                        "has_update": True,
                        "latest_version": latest_version,
                        "url": data.get("html_url", "")
                    })
                    return
        except Exception:
            pass
        callback({"has_update": False})

    thread = threading.Thread(target=_check)
    thread.daemon = True
    thread.start()


def compare_versions(v1, v2):
    """Compare two version strings. Returns 1 if v1 > v2, -1 if v1 < v2, 0 if equal."""
    def parse_version(v):
        return [int(x) for x in re.findall(r'\d+', v)]

    parts1 = parse_version(v1)
    parts2 = parse_version(v2)

    for p1, p2 in zip(parts1, parts2):
        if p1 > p2:
            return 1
        elif p1 < p2:
            return -1

    return 0


def init_skill():
    """Initialize the skill - create data directory and default files."""
    ensure_dir()

    # Create default rule.md if not exists
    if not os.path.exists(RULE_FILE):
        default_rule = """# Learning Check-in Rules

## Daily Check-in
- One check-in per day
- Simply tell me "I finished my learning" or "check-in done" when you're done

## Reminder Times
- 09:00 - Morning reminder (friendly)
- 17:00 - Afternoon reminder (encouraging)
- 20:00 - Evening reminder (urgent)

## Streak
- Keep your streak going by checking in every day!
- I'll remind you if you forget

## Customization
You can edit this file to customize your rules:
- Change reminder times
- Edit reminder messages
- Add your own notes

Just let me know if you want to make changes!
"""
        with open(RULE_FILE, "w", encoding="utf-8") as f:
            f.write(default_rule)

    # Create empty records if not exists
    if not os.path.exists(RECORDS_FILE):
        save_records({"checkins": []})

    # Save current version
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(VERSION)

    return {
        "success": True,
        "message": "Learning check-in skill initialized!",
        "data_dir": DATA_DIR
    }


def get_reminder_message(time_slot):
    """Get reminder message for specific time slot."""
    # Try to load custom messages from rule.md
    rules = load_rules()
    if rules:
        # Look for custom messages in rule.md
        lines = rules.split("\n")
        in_reminder_section = False
        custom_messages = []
        for line in lines:
            if "message" in line.lower() or "reminder" in line.lower():
                in_reminder_section = True
            elif in_reminder_section and line.strip():
                if line.startswith("-") or line.startswith("*"):
                    custom_messages.append(line.lstrip("-* ").strip())
                elif line.startswith("#"):
                    break

        if custom_messages:
            import random
            return random.choice(custom_messages)

    # Use default messages
    import random
    default_msgs = DEFAULT_MESSAGES.get(time_slot, DEFAULT_MESSAGES["20:00"])
    return random.choice(default_msgs)


def should_send_reminder(time_slot):
    """Check if reminder should be sent for this time slot today."""
    reminder_log = load_reminder_log()
    today = get_today()
    key = f"{today}_{time_slot}"

    # Already reminded today at this time
    if reminder_log.get(key):
        return False

    # Check if already checked in today
    if is_checked_in_today():
        return False

    return True


def log_reminder_sent(time_slot):
    """Log that reminder was sent."""
    reminder_log = load_reminder_log()
    today = get_today()
    key = f"{today}_{time_slot}"
    reminder_log[key] = {"timestamp": datetime.datetime.now().isoformat()}
    save_reminder_log(reminder_log)


# CLI Interface
def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("Usage: python learning_checkin.py <command> [args]")
        print("Commands:")
        print("  init              - Initialize the skill (first time setup)")
        print("  checkin           - Record a check-in")
        print("  status            - Get current status")
        print("  streak            - Get current streak")
        print("  version           - Get current version")
        print("  check-version     - Check for updates")
        print("  reminder <time>   - Check if reminder should be sent (e.g., 09:00)")
        print("  message <time>    - Get reminder message for time slot")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "init":
        result = init_skill()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "checkin":
        result = do_checkin()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "status":
        result = get_status()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "streak":
        print(json.dumps({"streak": get_streak()}, ensure_ascii=False, indent=2))

    elif command == "version":
        print(json.dumps({"version": VERSION}, ensure_ascii=False, indent=2))

    elif command == "check-version":
        def on_result(result):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        check_version_async(on_result)
        # Wait a bit for async result
        time.sleep(6)

    elif command == "reminder":
        if len(sys.argv) < 3:
            print("Usage: python learning_checkin.py reminder <time_slot>")
            sys.exit(1)
        time_slot = sys.argv[2]
        result = {
            "should_send": should_send_reminder(time_slot),
            "checked_in": is_checked_in_today()
        }
        if result["should_send"]:
            log_reminder_sent(time_slot)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "message":
        if len(sys.argv) < 3:
            print("Usage: python learning_checkin.py message <time_slot>")
            sys.exit(1)
        time_slot = sys.argv[2]
        message = get_reminder_message(time_slot)
        print(json.dumps({"message": message}, ensure_ascii=False, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()