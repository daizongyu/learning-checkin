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
- Smart reminders at appropriate times (via cron jobs)
- Optional version updates check

## Data Storage

All data is stored locally in a `data` subfolder next to the skill:

```
<skill_directory>/data/
├── rule.md           - User's customizable rules
├── records.json      - Check-in history
├── version.txt       - Current version
├── cron_status.json  - Cron configuration status (auto-set by Agent)
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
- `cron_setup` - Commands to set up reminder cron jobs
- `cron_status` - Current cron configuration status
- `auto_cron: true` - Indicates Agent should auto-create cron job

**Agent action:** 
1. Run the init command
2. Collect environment information (OS, timezone, language)
3. **Automatically create cron job** using the command in `cron_setup` (default time: 20:00)
4. **Verify cron setup was successful** - check if cron job was created
5. If cron setup succeeded, call: `python <skill_path> learning_checkin.py update-cron <times>` (e.g., "20:00")
6. If cron setup failed, inform user with manual setup instructions
7. Show welcome message and explain the check-in process
8. Ask user to start their first check-in

### 2. Check-in

```bash
python <skill_path>/learning_checkin.py checkin
```

**When to use:** When user says they're done with their learning (e.g., "I finished my study session", "check-in done", "learning complete", etc.)

**Returns:**
- `success` - Whether check-in was recorded
- `streak` - Current streak count
- `message` - Celebration message (all messages in English, Agent translates)
- `update` - Version update info if available

**Agent action:**
- Run checkin command
- Translate the celebration message to user's language
- Show streak count with celebration
- Encourage user to continue tomorrow

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

**Agent action:**
- Run status command
- Translate message to user's language
- Tell user if they've checked in today
- Share their current streak
- Show total days checked in

### 4. Get Environment Information

```bash
python <skill_path>/learning_checkin.py env
```

**When to use:** Before initialization to gather environment context.

**Returns:**
- `os` - Operating system (Windows, Linux, Darwin)
- `os_version` - OS version string
- `python_version` - Python version
- `locale` - System locale
- `timezone` - User's timezone
- `user_language` - Detected user language (zh/en)

**Agent action:** Use this to understand the user's environment and adapt accordingly.

### 5. Get Reminder Message

```bash
python <skill_path>/learning_checkin.py message <time>
```

Where `<time>` is one of: `09:00`, `17:00`, `20:00`

**When to use:** When sending a scheduled reminder.

**Returns:**
- `message` - Reminder text (in English, Agent translates)

**Agent action:**
- Run message command with appropriate time slot
- Translate the message to user's language
- Send the reminder to user

### 6. Check Reminder Status

```bash
python <skill_path>/learning_checkin.py reminder <time>
```

Where `<time>` is one of: `09:00`, `17:00`, `20:00`

**When to use:** Before sending a reminder (typically called by cron job).

**Returns:**
- `should_send` - Whether reminder should be sent
- `checked_in` - Whether user has already checked in today

**Agent action:**
- Run reminder command
- If result shows "should_send": true, then send the reminder
- The command automatically logs that reminder was sent

### 7. Update Cron Status

```bash
python <skill_path>/learning_checkin.py update-cron <times>
```

Where `<times>` is comma-separated times (e.g., "20:00" or "09:00,20:00")

**When to use:** After successfully setting up cron jobs.

**Agent action:** Call this to save the configured reminder times.

### 8. Get Cron Status

```bash
python <skill_path>/learning_checkin.py cron-status
```

**When to use:** To check if reminders are configured.

**Returns:**
- `configured` - Whether cron is set up
- `times` - Configured reminder times

## Default Behavior

### Check-in Rule
- User checks in once per day
- Simply tell the Agent "I'm done" or "check-in complete"
- That's it! No complex forms or steps

### Default Reminder Schedule
- **09:00 (Morning):** Friendly reminder
- **17:00 (Afternoon):** Encouraging reminder  
- **20:00 (Evening):** Urgent reminder (don't break the streak!)

### Streak System
- Consecutive days of check-ins = streak
- Miss a day = streak resets to 0

## Customization

Users can edit the `rule.md` file (in the data folder) to customize:
- Reminder times
- Reminder messages
- Their personal goals or notes

## Version Check

On each check-in, the skill can optionally check GitHub for new versions:
- Non-blocking (5 second timeout)
- If new version available, Agent tells user

## Agent Guidelines

### First Interaction (Welcome)
The Agent should:
1. Be warm and encouraging
2. Explain in simple, non-technical language:
   - "Just tell me when you've done your learning for today"
   - "I'll remind you if you forget"
   - "You'll build a streak!"
3. **Automatically set up daily reminder** by running the cron command returned from init (default: 20:00)
4. **Verify cron setup was successful**
   - If cron creation command succeeded: call `update-cron` to save status
   - If failed: show manual setup instructions based on the app being used
5. Explain that the system will check if they've already checked in before sending reminders (to avoid duplicates)
6. Ask: "Ready to start your first check-in?"

### Cron Setup Verification (Critical)
The Agent **MUST** verify cron setup:
1. Attempt to create the cron job using the provided command
2. Check if the cron job was created successfully
3. If successful: call `update-cron` with the configured times
4. If failed: provide manual instructions:
   - **For CoPaw:** Show the cron create command for user to run manually
   - **For OpenClaw:** Same, adjust command prefix as needed
   - **For other tools:** Provide generic instructions

### Daily Check-in Interaction
The Agent should:
1. Celebrate the check-in
2. Mention current streak
3. Encourage for tomorrow
4. Keep it positive and simple

### Reminder Interaction
The Agent should:
1. Use the appropriate tone for the time of day
2. Morning: Cheerful and friendly
3. Afternoon: Supportive and encouraging
4. Evening: Urgent but caring
5. Translate all messages to user's language

## Technical Notes

- All messages are in **English** - Agent should translate to user's language
- All file paths use UTF-8 encoding
- Compatible with Windows, Linux, macOS
- Data stored in `data` subfolder next to the skill
- No external dependencies (Python standard library only)

## Version

Current version: 3.0.6

GitHub: https://github.com/daizongyu/learning-checkin