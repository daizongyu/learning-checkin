# Learning Check-in Skill

**Simple • Local • Privacy-First**

---

## What is this?

A lightweight learning check-in tool that helps you build daily learning habits. All data is stored locally on your device.

**Key Features:**
- ✅ **Local Storage**: All your data stays on your device
- ✅ **Zero Dependencies**: Uses only Python standard library
- ✅ **Privacy-First**: No personal information collected
- ✅ **Cross-Platform**: Works on Windows, Linux, macOS
- ✅ **Simple**: Just 3 commands to use

---

## Quick Start

### 1. Initialize

```bash
python checkin_cli.py init --nickname YourName --country CN
```

### 2. Check in

```bash
python checkin_cli.py checkin
```

### 3. View status

```bash
python checkin_cli.py status
```

---

## Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize new user |
| `checkin` | Daily check-in |
| `checkin --note "..."` | Check-in with note about what you learned |
| `status` | View your check-in status and streak |

---

## Installation

**This is a source-only package. Choose one of these methods:**

### Method 1: Git Clone (Recommended)

```bash
git clone https://github.com/daizongyu/learning-checkin.git
cd learning-checkin
python checkin_cli.py init --nickname YourName --country CN
```

### Method 2: Pip Install from Source

```bash
git clone https://github.com/daizongyu/learning-checkin.git
cd learning-checkin
pip install .
learning-checkin init --nickname YourName --country CN
```

**Package Type:** Source distribution (no pre-built wheels)  
**Install Spec:** `pip install .` or direct usage via `python checkin_cli.py`

---

## Data Storage

**All data is stored locally on your device:**

- **Windows**: `%APPDATA%\learning-checkin\`
- **Linux/macOS**: `~/.learning-checkin/`

**Data Structure:**
```
learning-checkin/
├── user_config.json      # Your user configuration
└── users/
    └── {user_id}/
        ├── profile.json  # Profile information
        ├── streak.json   # Streak tracking
        └── checkins/     # Daily check-in records
            └── YYYY-MM-DD.json
```

---

## Network Usage

**Core functionality is 100% offline.** However, the tool performs an optional update check:

- **Update Check**: On each command, the tool silently checks GitHub for new releases
- **Endpoint**: `https://api.github.com/repos/daizongyu/learning-checkin/releases/latest`
- **Timeout**: 2 seconds
- **Behavior**: Fails silently if network is unavailable
- **Purpose**: Notifies you when a new version is available

**You can use all core features (init, checkin, status) completely offline.**

---

## Requirements

- **Python**: 3.8+
- **Dependencies**: None (uses Python standard library only)
- **Internet**: Optional (only for update notifications)

---

## Privacy

- ✅ No personal information collected
- ✅ No data sent to external servers (except optional update check)
- ✅ No account required
- ✅ All data stored locally
- ✅ Anonymous user ID (format: `local_{nickname}_{random}`)

---

## Updating

When a new version is available, you'll see a notification:

```
💡 New version available: v2.1.0 (current: v2.0.1)
   Update: git pull origin main
   Release: https://github.com/daizongyu/learning-checkin/releases/latest
```

To update:
```bash
git pull origin main
```

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
