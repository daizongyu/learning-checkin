# Learning Check-in

**Simple • Local • Offline • Privacy-First**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/daizongyu/learning-checkin)

---

## What is this?

A simple, offline learning check-in tool. Track your daily learning progress and build habits.

**No network • No account • No dependencies**

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

# Add a note
python checkin_cli.py checkin --note "Studied Python for 2 hours"

# View status
python checkin_cli.py status
```

---

## Features

- ✅ **100% Offline**: No network connection needed
- ✅ **Zero Dependencies**: Uses only Python standard library
- ✅ **Privacy First**: All data stored locally
- ✅ **Cross-Platform**: Windows, Linux, macOS
- ✅ **Simple**: Just 3 commands to use

---

## Data Storage

All data stays on your computer:

- **Windows**: `%APPDATA%\learning-checkin\`
- **Linux/macOS**: `~/.learning-checkin/`

### Structure

```
learning-checkin/
├── user_config.json    # Current user
└── users/
    └── {user_id}/
        ├── profile.json
        ├── streak.json
        └── checkins/
            └── YYYY-MM-DD.json
```

---

## Requirements

- **Python**: 3.8+
- **Dependencies**: None!
- **Internet**: Not required

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

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

**Learn every day, grow every day!** 🦐📚✨
