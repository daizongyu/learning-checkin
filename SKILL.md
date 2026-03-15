---
name: learning-checkin
description: Daily learning habit builder with check-ins and smart reminders
metadata: { "copaw": { "emoji": "📚" } }
---

# Learning Check-in Skill

Help users build a daily learning habit through simple check-ins and intelligent reminders.

## Overview

This skill enables users to track their daily learning with:
- Simple daily check-in (just say "I'm done" or "check-in complete")
- Automatic streak tracking
- Optional smart reminders (Agent decides how to implement)
- Optional version updates check

## Data Storage

All data is stored locally in a `data` subfolder next to the skill:

```
<skill_directory>/data/
├── rule.md           - User's customizable rules
├── records.json      - Check-in history
├── version.txt       - Current skill version
├── cron_status.json  - Reminder configuration status
└── reminder_log.json - Reminder sending log
```

The data folder is automatically created on first use.

## Commands

The skill provides these functions that the Agent can call:

### 1. Initialize (First Time)

```bash
python <skill_path>/learning_checkin.py init
```

**When to use:** First time the user activates this skill.

**Returns:**
- `welcome_message` - Welcome text for the user
- `environment` - Environment info (OS, timezone, language, etc.)
- `reminder_strategy` - Suggested reminder times
- `cron_status` - Current reminder configuration status

**Agent action:** 
1. Run the init command
2. Show welcome message and explain the check-in process
3. Ask user if they want daily reminders
4. If yes: Agent decides how to implement (cron, native scheduler, etc.)
5. Ask user to start their first check-in

### 2. Check-in

```bash
python <skill_path>/learning_checkin.py checkin
```

**When to use:** When user says they're done with their learning.

**Returns:**
- `success` - Whether check-in was recorded
- `streak` - Current streak count
- `message` - Celebration message (in English, translate to user's language)

**Agent action:**
- Translate celebration message to user's language
- Show streak count
- Encourage user

### 3. Status

```bash
python <skill_path>/learning_checkin.py status
```

**When to use:** When user asks about their progress or streak.

**Returns:**
- `checked_in_today` - Whether user has checked in today
- `streak` - Current streak count
- `total_checkins` - Total days checked in
- `message` - Status message (in English)

### 4. Get Environment Information

```bash
python <skill_path>/learning_checkin.py env
```

**Returns:**
- `os` - Operating system
- `os_version` - OS version
- `python_version` - Python version
- `locale` - System locale
- `timezone` - User's timezone
- `user_language` - Detected language (zh/en)

### 5. Get Reminder Message

```bash
python <skill_path>/learning_checkin.py message <time>
```

Where `<time>` is one of: `09:00`, `17:00`, `20:00`

**When to use:** When sending a reminder.

**Returns:**
- `message` - Reminder text (in English, translate to user's language)

### 6. Check Reminder Status

```bash
python <skill_path>/learning_checkin.py reminder <time>
```

**When to use:** Before sending a reminder.

**Returns:**
- `should_send` - Whether reminder should be sent
- `checked_in` - Whether user has already checked in today

### 7. Update Cron Status

```bash
python <skill_path>/learning_checkin.py update-cron <times>
```

**When to use:** After setting up reminders (optional).

### 8. Get Cron Status

```bash
python <skill_path>/learning_checkin.py cron-status
```

**Returns:**
- `configured` - Whether reminders are set up
- `times` - Configured reminder times

## Default Behavior

### Check-in Rule
- User checks in once per day
- Simply tell the Agent "I'm done" or "check-in complete"

### Reminder Strategy (Suggested)
If user wants reminders, Agent can set up at preferred time:
- **Morning:** 09:00
- **Afternoon:** 17:00  
- **Evening:** 20:00

The skill will check if user already checked in before sending reminders (to avoid duplicates).

### Streak System
- Consecutive days = streak
- Miss a day = streak resets

## Customization

Users can edit the `rule.md` file (in the data folder) to customize reminder messages.

## Version Check

The Agent can periodically check GitHub for updates:
- Check: https://github.com/daizongyu/learning-checkin/releases
- Current version: 3.0.8
- If newer version available, Agent can inform user

## Agent Guidelines

### First Interaction (Welcome)
The Agent should:
1. Be warm and encouraging
2. Explain the simple check-in process
3. **Ask if user wants daily reminders** - explain what it does
4. If user agrees, Agent decides how to implement (cron, native scheduler, etc.)
5. Ask: "Ready to start your first check-in?"

### Reminder Implementation
- Agent has full control over how to implement reminders
- Use cron skill if available, or platform-native scheduler
- The skill provides `reminder` command to check if reminder should be sent
- The skill provides `message` command to get localized reminder text

### Version Check
- Agent decides when and how to check for updates
- Can use web search or visit GitHub releases page
- Skill returns current version but doesn't auto-check

## Technical Notes

- All messages are in **English** - Agent translates to user's language
- All file paths use UTF-8 encoding
- Compatible with Windows, Linux, macOS
- Data stored in `data` subfolder next to the skill
- **No external network requests** - version check delegated to Agent
- No external dependencies (Python standard library only)

## Version

Current version: 3.0.8

GitHub: https://github.com/daizongyu/learning-checkin