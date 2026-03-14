# Learning Check-in

**Simple • Local • Privacy-First**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/daizongyu/learning-checkin)

---

## What is this?

A lightweight learning check-in tool that helps you build daily learning habits. All data is stored locally on your device.

**Core Features:**
- ✅ **Local Storage**: All your data stays on your device
- ✅ **Zero Dependencies**: Uses only Python standard library
- ✅ **Privacy-First**: No personal information collected
- ✅ **Cross-Platform**: Works on Windows, Linux, macOS
- ✅ **Simple**: Just 3 commands to use

**What this is NOT:**
- ❌ No global leaderboards
- ❌ No remote data aggregation
- ❌ No server communication (except optional update check)
- ❌ No failure detection or monitoring

---

## Quick Start

### 1. Get the code

```bash
git clone https://github.com/daizongyu/learning-checkin.git
cd learning-checkin
```

### 2. Initialize

```bash
python checkin_cli.py init --nickname YourName --country CN
```

### 3. Check in

```bash
python checkin_cli.py checkin
```

That's it! 🎉

---

## Commands

```bash
# Initialize (first time only)
python checkin_cli.py init --nickname Daisy --country CN

# Daily check-in
python checkin_cli.py checkin

# Add a note about what you learned
python checkin_cli.py checkin --note "Studied Python for 2 hours"

# View your status and streak
python checkin_cli.py status

# JSON output for Agent integration
python checkin_cli.py init --nickname Test --country US --json
```

---

## Features

### Core Functionality (100% Offline)

- ✅ **Daily Check-in**: Track your learning progress
- ✅ **Streak Tracking**: See your consecutive days
- ✅ **Status View**: Check your total check-ins and longest streak
- ✅ **Local Storage**: All data on your device
- ✅ **Zero Dependencies**: Python standard library only
- ✅ **Privacy-First**: No personal info collected

### Optional Features (Network)

- 🔔 **Update Notifications**: Silent check for new versions on each command
  - Endpoint: `https://api.github.com/repos/daizongyu/learning-checkin/releases/latest`
  - Timeout: 2 seconds
  - Fails silently if offline
  - Can be used completely offline

### Agent Integration

- 🤖 **JSON Mode**: Structured output for Agent processing
  - Command: `python checkin_cli.py init --nickname Name --country CN --json`
  - Output: JSON with user data and language hint
  - Purpose: Enable multi-language welcome messages

---

## Data Storage

**All data stays on your computer:**

- **Windows**: `%APPDATA%\learning-checkin\`
- **Linux/macOS**: `~/.learning-checkin/`

### Structure

```
learning-checkin/
├── user_config.json    # Current user configuration
└── users/
    └── {user_id}/
        ├── profile.json    # Profile information (nickname, country)
        ├── streak.json     # Streak tracking data
        └── checkins/
            └── YYYY-MM-DD.json  # Daily check-in records
```

### Privacy

- ✅ No personal information collected
- ✅ No data sent to external servers (except optional update check)
- ✅ No account required
- ✅ Anonymous user ID (format: `local_{nickname}_{random}`)

**What we DON'T collect:**
- No email addresses
- No real names
- No location data
- No learning content
- No usage statistics

---

## Network Usage

**Core functionality is 100% offline.** You can use all features without internet.

**Optional network usage:**
- On each command, the tool checks GitHub for new releases
- If a new version is available, displays an update notification
- Network call has 2-second timeout
- Fails silently if network is unavailable
- Does not interrupt or delay core functionality

**Example update notification:**
```
[UPDATE] New version available: v2.1.0 (current: v2.0.7)
   Run: git pull origin main
   Info: https://github.com/daizongyu/learning-checkin/releases/latest
```

---

## Requirements

- **Python**: 3.8+
- **Dependencies**: None (uses Python standard library only)
- **Internet**: Optional (only for update notifications)

---

## Installation

### Option 1: Direct Use

```bash
git clone https://github.com/daizongyu/learning-checkin.git
cd learning-checkin
python checkin_cli.py init --nickname YourName --country CN
```

### Option 2: Install as Package

```bash
pip install .
learning-checkin init --nickname YourName --country CN
```

---

## Backup

**Windows:**
```powershell
copy %APPDATA%\learning-checkin D:\Backup\
```

**Linux/macOS:**
```bash
tar -czf backup.tar.gz ~/.learning-checkin
```

**Important:** Since all data is local, you are responsible for backing up your check-in history.

---

## Updating

When a new version is available, you'll see a notification. To update:

```bash
git pull origin main
```

Or download the latest release: https://github.com/daizongyu/learning-checkin/releases

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Support

- **Repository**: https://github.com/daizongyu/learning-checkin
- **Issues**: https://github.com/daizongyu/learning-checkin/issues
- **Releases**: https://github.com/daizongyu/learning-checkin/releases

---

**Learn every day, grow every day!** 🦐📚✨
