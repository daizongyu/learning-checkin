# Learning Check-in Skill

Global learning check-in system with streak tracking, global leaderboard, and failure detection.

---

## Quick Start

### 1. Initialize User

```bash
python checkin_cli.py init --nickname <your_nickname> --country <country_code>
```

**Parameters:**
- `nickname`: Your nickname (displayed on leaderboard, use a pseudonym for privacy)
- `country`: Country code (e.g., CN, US, UK)

**Example:**
```bash
python checkin_cli.py init --nickname Daisy --country CN
```

After initialization, you'll receive:
- User ID (format: `openclaw_daisy_a1b2c3`)
- Next steps guide

**No GitHub account required! No token needed! Ready to use!**

---

## Command Reference

### Check-in Commands

| Command | Description |
|---------|-------------|
| `python checkin_cli.py checkin` | Check in for today |
| `python checkin_cli.py checkin --note "text"` | Check in with a note |
| `python checkin_cli.py status` | View current check-in status |
| `python checkin_cli.py rank` | View your ranking |

### Leaderboard

| Command | Description |
|---------|-------------|
| `python checkin_cli.py leaderboard` | View global leaderboard |
| `python checkin_cli.py leaderboard --country CN` | View country leaderboard |

### System

| Command | Description |
|---------|-------------|
| `python checkin_cli.py check-update` | Check for Skill updates |

---

## Installation

### Option 1: Direct Use (Recommended)

```bash
# Clone or download the repository
git clone https://github.com/OpenClaw-Skills/learning-checkin.git
cd learning-checkin

# Install dependencies
pip install -r requirements.txt

# Initialize and start
python checkin_cli.py init --nickname YourName --country CN
python checkin_cli.py checkin
```

### Option 2: Install as Python Package

```bash
# Install from source
pip install .

# Use from anywhere
learning-checkin init --nickname YourName --country CN
learning-checkin checkin
```

### Option 3: Create Alias (Optional)

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

## Platform Support

| Platform | Command |
|----------|---------|
| **Windows** | `python checkin_cli.py <command>` |
| **Linux** | `python3 checkin_cli.py <command>` or `./checkin_cli.py <command>` |
| **macOS** | `python3 checkin_cli.py <command>` or `./checkin_cli.py <command>` |

---

## Requirements

- **Python**: 3.8 or higher
- **Dependencies**: `requests>=2.28.0`
- **Internet**: Required for GitHub API access

---

## Data Storage

### Local Storage
- **Config file**: 
  - Windows: `%APPDATA%\learning-checkin\config.json`
  - Linux/macOS: `~/.learning-checkin/config.json`

### Remote Storage (GitHub)
- **Repository**: `daizongyu/learning-checkin-data`
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

## API Integration

### Python Library Usage

```python
from src import LearningCheckinSkill

# Initialize skill
skill = LearningCheckinSkill()

# Initialize user
result = skill.init_user("Daisy", "CN")
print(f"User ID: {result['user_id']}")

# Check in
result = skill.checkin("openclaw_daisy_a1b2c3", note="Learned Python")
print(f"Streak: {result['streak']} days")

# Get status
status = skill.get_status("openclaw_daisy_a1b2c3")
print(f"Checked today: {status['checked_today']}")

# Get leaderboard
leaderboard = skill.get_leaderboard()
print(f"Total users: {leaderboard['total_users']}")
```

---

## FAQ

**Q: Do I need a GitHub account?**
A: **No!** Uses a centralized public repository, zero barrier to entry.

**Q: What happens if I forget to check in?**
A: 
- Your streak will be broken
- Task fails if ≥2 days missed per week
- You can rejoin after failure

**Q: How is data privacy protected?**
A: 
- User ID is generated anonymously (`openclaw_{nickname}_{random}`)
- Only nickname is stored (pseudonym recommended)
- No personal sensitive information is stored
- Data is fully public (this is a public repository)

**Q: How to change nickname?**
A: Re-initialize (generates a new user ID):
```bash
python checkin_cli.py init --nickname NewName --country CN
```

**Q: Can I use this on multiple devices?**
A: Yes! Just copy the config file to the same location on each device, or re-initialize with the same nickname.

---

## Troubleshooting

### "Not initialized" error
```bash
python checkin_cli.py init --nickname YourName --country CN
```

### Network connection failed
- Check your internet connection
- Verify GitHub API is accessible
- Try again later (rate limit: 5000 requests/hour)

### Python not found
- **Windows**: Install Python from python.org, ensure "Add to PATH" is checked
- **Linux**: `sudo apt install python3` or `sudo yum install python3`
- **macOS**: `brew install python3` or use system Python

---

## Version History

- v1.0.0 (2025-01-20): Initial release
  - User initialization
  - Daily check-in
  - Streak tracking
  - Global leaderboard
  - Failure detection
  - Automatic updates

---

## License

MIT License - See LICENSE file for details

---

**Learn together, grow together!** 🦐📚✨
