# Learning Check-in

Global learning check-in system with streak tracking, leaderboard, and failure detection.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Features

- ✅ **Zero Configuration**: No GitHub account or token required
- ✅ **Cross-Platform**: Works on Windows, Linux, and macOS
- ✅ **Streak Tracking**: Automatic consecutive day counting
- ✅ **Global Leaderboard**: Real-time ranking with country filtering
- ✅ **Failure Detection**: Weekly failure detection (≥2 days missed = failed)
- ✅ **Anonymous**: User IDs are auto-generated, no personal info stored

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize User

```bash
python checkin_cli.py init --nickname YourName --country CN
```

### 3. Start Checking In

```bash
python checkin_cli.py checkin
```

That's it! 🎉

---

## Usage

### Basic Commands

```bash
# Initialize (first time only)
python checkin_cli.py init --nickname Daisy --country CN

# Daily check-in
python checkin_cli.py checkin

# Add a note to your check-in
python checkin_cli.py checkin --note "Studied Python for 2 hours"

# View your status
python checkin_cli.py status

# View global leaderboard
python checkin_cli.py leaderboard

# View your ranking
python checkin_cli.py rank

# Check for updates
python checkin_cli.py check-update
```

### Platform-Specific

| Platform | Command |
|----------|---------|
| **Windows** | `python checkin_cli.py <command>` |
| **Linux** | `python3 checkin_cli.py <command>` or `./checkin_cli.py <command>` |
| **macOS** | `python3 checkin_cli.py <command>` or `./checkin_cli.py <command>` |

---

## Installation

### Option 1: Direct Use (Recommended)

```bash
# Clone the repository
git clone https://github.com/OpenClaw-Skills/learning-checkin.git
cd learning-checkin

# Install dependencies
pip install -r requirements.txt

# Run
python checkin_cli.py init --nickname YourName --country CN
```

### Option 2: Install as Package

```bash
# Install from source
pip install .

# Use from anywhere
learning-checkin init --nickname YourName --country CN
```

### Option 3: Create Alias

**Linux/macOS:**
```bash
alias checkin='python /path/to/checkin_cli.py'
checkin init --nickname YourName --country CN
```

**Windows (PowerShell):**
```powershell
function checkin { python C:\path\to\checkin_cli.py @args }
checkin init --nickname YourName --country CN
```

---

## Data Storage

### Local Configuration

- **Windows**: `%APPDATA%\learning-checkin\config.json`
- **Linux/macOS**: `~/.learning-checkin/config.json`

### Remote Data (GitHub)

All check-in data is stored in a public GitHub repository:
- **Repository**: https://github.com/daizongyu/learning-checkin-data
- **Structure**:
  ```
  users/{user_id}/
  ├── profile.json       # User profile
  ├── streak.json        # Streak statistics
  └── checkins/
      └── YYYY-MM-DD.json  # Daily check-in records
  
  leaderboard/
  └── current.json       # Global leaderboard
  ```

---

## Rules

1. **Daily Check-in**: Check in at least once per day
2. **Failure Rule**: Task fails if ≥2 days missed per week
3. **Restart**: Can rejoin anytime after failure

---

## Privacy

- User ID is anonymous (format: `openclaw_{nickname}_{random}`)
- Only nickname is stored (use a pseudonym for privacy)
- No personal sensitive information
- All data is public (this is a public repository)

---

## Requirements

- **Python**: 3.8 or higher
- **Dependencies**: `requests>=2.28.0`
- **Internet**: Required for GitHub API access

---

## Development

### Project Structure

```
learning-checkin/
├── checkin_cli.py         # Main CLI entry point
├── src/                   # Core modules
│   ├── __init__.py       # Main class and exports
│   ├── github_api.py     # GitHub API wrapper
│   ├── user_manager.py   # User management
│   ├── checkin.py        # Check-in logic
│   ├── leaderboard.py    # Leaderboard management
│   ├── failure.py        # Failure detection
│   ├── reminder.py       # Reminder system
│   └── updater.py        # Update checking
├── templates/
│   └── messages.json     # Message templates
├── .github/workflows/    # GitHub Actions
├── requirements.txt      # Dependencies
├── SKILL.md             # Full documentation
├── QUICKSTART.md        # Quick start guide
└── README.md            # This file
```

### Run Tests

```bash
python -m pytest tests/
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Support

- **Documentation**: See [SKILL.md](SKILL.md)
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Issues**: https://github.com/OpenClaw-Skills/learning-checkin/issues

---

**Learn together, grow together!** 🦐📚✨
