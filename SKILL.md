# Learning Check-in Skill

**Simple • Local • Offline**

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
| `checkin --note` | Check-in with note |
| `status` | View status |

---

## Installation

### Direct Use

```bash
git clone https://github.com/daizongyu/learning-checkin.git
cd learning-checkin
python checkin_cli.py init --nickname YourName --country CN
```

### As Package

```bash
pip install .
learning-checkin init --nickname YourName --country CN
```

---

## Data Storage

- **Windows**: `%APPDATA%\learning-checkin\`
- **Linux/macOS**: `~/.learning-checkin/`

All data stored locally. No network required.

---

## Requirements

- Python 3.8+
- No external dependencies
- No internet connection

---

## License

MIT License

---

**Learn every day!** 🦐📚✨
