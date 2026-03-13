# Learning Check-in - Usage Guide

## Installation & Usage

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Initialize User

```bash
python checkin_cli.py init --nickname YourName --country CN
```

### Step 3: Start Checking In

```bash
python checkin_cli.py checkin
```

---

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize new user | `python checkin_cli.py init --nickname Daisy --country CN` |
| `checkin` | Daily check-in | `python checkin_cli.py checkin` |
| `checkin --note` | Check-in with note | `python checkin_cli.py checkin --note "Studied Python"` |
| `status` | View your status | `python checkin_cli.py status` |
| `leaderboard` | Global leaderboard | `python checkin_cli.py leaderboard` |
| `leaderboard --country` | Country leaderboard | `python checkin_cli.py leaderboard --country US` |
| `rank` | Your ranking | `python checkin_cli.py rank` |
| `check-update` | Check for updates | `python checkin_cli.py check-update` |

---

## Platform-Specific Instructions

### Windows

**Using Command Prompt:**
```cmd
cd C:\path\to\learning-checkin
python checkin_cli.py init --nickname YourName --country CN
python checkin_cli.py checkin
```

**Using PowerShell:**
```powershell
cd C:\path\to\learning-checkin
python checkin_cli.py init --nickname YourName --country CN
python checkin_cli.py checkin
```

**Optional: Create a function for easier access:**
```powershell
function checkin { python C:\path\to\learning-checkin\checkin_cli.py @args }
checkin init --nickname YourName --country CN
```

### Linux

**Using python3:**
```bash
cd /path/to/learning-checkin
python3 checkin_cli.py init --nickname YourName --country CN
python3 checkin_cli.py checkin
```

**Or make executable:**
```bash
chmod +x checkin_cli.py
./checkin_cli.py init --nickname YourName --country CN
```

**Optional: Create an alias:**
```bash
echo "alias checkin='python3 /path/to/learning-checkin/checkin_cli.py'" >> ~/.bashrc
source ~/.bashrc
checkin init --nickname YourName --country CN
```

### macOS

**Using python3:**
```bash
cd /path/to/learning-checkin
python3 checkin_cli.py init --nickname YourName --country CN
python3 checkin_cli.py checkin
```

**Or make executable:**
```bash
chmod +x checkin_cli.py
./checkin_cli.py init --nickname YourName --country CN
```

**Optional: Create an alias:**
```bash
echo "alias checkin='python3 /path/to/learning-checkin/checkin_cli.py'" >> ~/.zshrc
source ~/.zshrc
checkin init --nickname YourName --country CN
```

---

## Optional: Install as Python Package

### From Source

```bash
cd /path/to/learning-checkin
pip install .
```

Then use from anywhere:
```bash
learning-checkin init --nickname YourName --country CN
learning-checkin checkin
```

### Uninstall

```bash
pip uninstall learning-checkin
```

---

## Troubleshooting

### "python: command not found"

**Windows:**
1. Download Python from https://python.org
2. During installation, check "Add Python to PATH"
3. Restart terminal

**Linux:**
```bash
sudo apt install python3  # Debian/Ubuntu
sudo yum install python3  # CentOS/RHEL
sudo dnf install python3  # Fedora
```

**macOS:**
```bash
brew install python3
# Or use system Python (pre-installed)
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

### Config file location

- **Windows**: `%APPDATA%\learning-checkin\config.json`
- **Linux**: `~/.learning-checkin/config.json`
- **macOS**: `~/.learning-checkin/config.json`

---

## Requirements

- Python 3.8 or higher
- requests>=2.28.0
- Internet connection (for GitHub API)

---

## Support

- Documentation: See SKILL.md
- Quick Start: See QUICKSTART.md
- Issues: https://github.com/OpenClaw-Skills/learning-checkin/issues

---

**Happy learning!** 🦐📚✨
