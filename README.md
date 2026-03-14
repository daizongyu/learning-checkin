# Learning Check-in

A daily learning habit tracker skill for OpenClaw/CoPaw agents.

## Features

- **Simple Check-in**: Just tell your agent "I'm done" or "check-in complete"
- **Streak Tracking**: Build your consecutive day streak
- **Smart Reminders**: Morning, afternoon, and evening reminders
- **Customizable**: Edit rules to fit your schedule
- **Version Updates**: Automatic update detection

## Quick Start

### 1. Initialize the Skill

Tell your agent: "I want to use the learning check-in skill"

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

If enabled, you'll receive reminders at:
- **09:00** - Friendly morning reminder
- **17:00** - Encouraging afternoon reminder  
- **20:00** - Urgent evening reminder

The tone becomes more pressing as the day goes on!

## Data Location

Your check-in data is stored in:
- `D:\workspace\learning-checkin\` (Windows)
- `~/workspace/learning-checkin/` (Linux/Mac)

Files:
- `rule.md` - Your personalized rules
- `records.json` - Check-in history
- `version.txt` - Current skill version

## Customization

Edit `rule.md` to customize:
- Reminder times
- Reminder messages
- Your personal goals

## Version

Current: **1.0.0**

## GitHub

https://github.com/daizongyu/learning-checkin

## License

MIT