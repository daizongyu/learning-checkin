# Learning Check-in

A daily learning habit tracker skill for OpenClaw/CoPaw agents.

## Features

- **Simple Check-in**: Just tell your agent "I'm done" or "check-in complete"
- **Streak Tracking**: Build your consecutive day streak
- **Smart Reminders**: Morning, afternoon, and evening reminders (via cron)
- **Customizable**: Edit rules to fit your schedule
- **Automatic Updates**: Version check on each check-in

## Installation

This skill is designed to be used with CoPaw or similar applications.

### Manual Installation

1. Copy the skill folder to your CoPaw skills directory:
   - Path: `C:\Users\YourName\.copaw\active_skills\learning-checkin\`

2. The skill will automatically initialize when first used.

### Usage

Simply tell your agent:
- "I want to use the learning check-in skill" (first time)
- "I'm done with my learning" or "check-in complete" (daily check-in)
- "What's my streak?" or "How am I doing?" (check progress)

## Quick Start

### 1. First Time Setup

The first time you activate this skill, tell your agent:
"I want to use the learning check-in skill"

The agent will:
- Welcome you and explain the rules
- Set up your personal check-in folder
- Ask you to start your first check-in

### 2. Daily Check-in

After completing your daily learning, tell your agent:
- "I'm done with my learning"
- "Check-in complete"
- "I finished studying"

Your agent will:
- Record your check-in
- Tell you your current streak
- Encourage you for tomorrow

### 3. Reminders (Optional)

If you set up cron jobs for reminders, you'll receive messages at:
- **09:00** - Friendly morning reminder
- **17:00** - Encouraging afternoon reminder  
- **20:00** - Urgent evening reminder

The tone becomes more pressing as the day goes on!

## Data Storage

Your check-in data is stored in your workspace:
- `D:\workspace\learning-checkin\` (Windows)
- `~/workspace/learning-checkin/` (Linux/Mac)

Files:
- `rule.md` - Your personalized rules (auto-created on first use)
- `records.json` - Check-in history
- `version.txt` - Current skill version

## Customization

Edit `rule.md` to customize:
- Reminder times
- Reminder messages
- Your personal goals

## Technical Requirements

- Python 3.x
- No external dependencies (uses standard library only)
- Works on Windows, Linux, and macOS

## Version

Current: **1.0.0**

## GitHub

https://github.com/daizongyu/learning-checkin

## License

MIT