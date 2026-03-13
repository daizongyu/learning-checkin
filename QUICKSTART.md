# Quick Start Guide

**Get configured in 30 seconds and start checking in!**

---

## Step 1: Install Dependencies (10 seconds)

```bash
pip install -r requirements.txt
```

---

## Step 2: Initialize User (30 seconds)

```bash
python checkin_cli.py init --nickname "Daisy" --country "CN"
```

**On success, you'll see:**
```
✅ User initialization successful!

User ID: openclaw_daisy_a1b2c3
Nickname: Daisy
Country: CN

🎉 No GitHub account needed, start checking in directly!
Next: Run 'python checkin_cli.py checkin'
```

**Note your User ID!** (The system will use it automatically, but it's useful to know)

---

## Step 3: Start Checking In (10 seconds)

```bash
python checkin_cli.py checkin
```

**On success, you'll see:**
```
✅ Check-in successful!

📅 Date: 2025-01-20
🔥 Streak: 1 day
📊 Total: 1 day
📊 Ranking info...

Keep going, you're getting better! 🌟
```

---

## View Status and Ranking

```bash
# View current status
python checkin_cli.py status

# View global leaderboard
python checkin_cli.py leaderboard

# View your ranking
python checkin_cli.py rank
```

---

## Done!

**That's it!**

**Just run once daily:**
```bash
python checkin_cli.py checkin
```

---

## Optional Configuration

### Add Check-in Note

```bash
python checkin_cli.py checkin --note "Learned Python for 2 hours"
```

### View Country-specific Leaderboard

```bash
python checkin_cli.py leaderboard --country CN
python checkin_cli.py leaderboard --country US
python checkin_cli.py leaderboard --country UK
```

---

## Platform-Specific Commands

### Windows

```cmd
# Using Command Prompt
python checkin_cli.py checkin

# Using PowerShell
python checkin_cli.py checkin
```

### Linux

```bash
# Using python3
python3 checkin_cli.py checkin

# Or make executable and run directly
chmod +x checkin_cli.py
./checkin_cli.py checkin
```

### macOS

```bash
# Using python3
python3 checkin_cli.py checkin

# Or make executable and run directly
chmod +x checkin_cli.py
./checkin_cli.py checkin
```

---

## FAQ

### Q: Do I need a GitHub account?
A: **No!** Uses a centralized public repository, zero barrier to entry.

### Q: What happens if I forget to check in?
A: 
- Your streak will be broken
- Task fails if ≥2 days missed per week
- You can rejoin after failure

### Q: How to restart after failure?
A: 
```bash
python checkin_cli.py init --nickname YourName --country CN
```

### Q: How is data privacy protected?
A: 
- User ID is generated anonymously (`openclaw_{nickname}_{random}`)
- Only nickname is stored (pseudonym recommended)
- No personal sensitive information is stored
- Data is fully public (this is a public repository)

### Q: Can I use this on multiple devices?
A: Yes! The config file location:
- **Windows**: `%APPDATA%\learning-checkin\config.json`
- **Linux**: `~/.learning-checkin/config.json`
- **macOS**: `~/.learning-checkin/config.json`

Copy the config file to use the same user on multiple devices.

### Q: How to change nickname?
A: Re-initialize (generates a new user ID):
```bash
python checkin_cli.py init --nickname "NewNickname" --country CN
```

---

## Troubleshooting

### "python: command not found"

**Windows:**
- Install Python from [python.org](https://python.org)
- During installation, check "Add Python to PATH"
- Restart terminal

**Linux:**
```bash
sudo apt install python3  # Debian/Ubuntu
sudo yum install python3  # CentOS/RHEL
```

**macOS:**
```bash
brew install python3
# Or use system Python
```

### "ModuleNotFoundError: No module named 'requests'"

```bash
pip install -r requirements.txt
# Or
pip3 install -r requirements.txt
```

### "Not initialized" error

```bash
python checkin_cli.py init --nickname YourName --country CN
```

---

## More Documentation

- [SKILL.md](SKILL.md) - Complete command reference
- [README.md](README.md) - Project overview
- [RELEASE_NOTES.md](RELEASE_NOTES.md) - Version history

---

## Data Center

All data is stored at: https://github.com/daizongyu/learning-checkin-data

This is a **public repository** where anyone can view check-in records from learners worldwide.

---

**Happy learning and checking in!** 🦐📚✨
