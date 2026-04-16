# 📋 System Prerequisites

Before you can use Crypto Vibeness, you need to install these tools on your system.

## 🛠️ Required Tools

| Tool | Purpose | Min Version |
|------|---------|------------|
| **git** | Clone the repository | 2.0+ |
| **make** | Run setup commands | 4.0+ |
| **python3** | Run the application | 3.8+ |
| **python3-venv** | Create virtual environments | Included with Python |

## 🔧 Installation by System

### Debian / Ubuntu / WSL

```bash
sudo apt-get update
sudo apt-get install -y git make python3 python3-venv python3-pip
```

Verify:
```bash
git --version           # Should show: git version 2.x.x
make --version          # Should show: GNU Make 4.x
python3 --version       # Should show: Python 3.8+
```

### AlmaLinux / Fedora / RHEL / CentOS

```bash
sudo dnf install -y git make python3 python3-venv
```

Verify:
```bash
git --version
make --version
python3 --version
```

### Arch Linux

```bash
sudo pacman -S git make python
```

Verify:
```bash
git --version
make --version
python --version
```

### macOS (with Homebrew)

```bash
brew install git make python3
```

Verify:
```bash
git --version
make --version
python3 --version
```

## ✅ Quick Check

Run this to verify everything is installed:

```bash
# Check all prerequisites
echo "Checking prerequisites..."
git --version && echo "✅ git installed" || echo "❌ git NOT installed"
make --version && echo "✅ make installed" || echo "❌ make NOT installed"
python3 --version && echo "✅ python3 installed" || echo "❌ python3 NOT installed"
python3 -m venv --help > /dev/null && echo "✅ python3-venv available" || echo "❌ python3-venv NOT available"
```

All should show ✅ before proceeding!

## 🚀 After Prerequisites

Once all prerequisites are installed, you can proceed with the project setup:

```bash
git clone https://github.com/Tom-rib/cryptographie_vibe.git
cd cryptographie_vibe
make setup
```

## ❓ Troubleshooting

### "make: command not found"
- On Ubuntu/Debian: `sudo apt-get install make`
- On Fedora: `sudo dnf install make`
- On Arch: `sudo pacman -S make`
- On macOS: `brew install make`

### "git: command not found"
- On Ubuntu/Debian: `sudo apt-get install git`
- On Fedora: `sudo dnf install git`
- On Arch: `sudo pacman -S git`
- On macOS: `brew install git`

### "python3: command not found"
- On Ubuntu/Debian: `sudo apt-get install python3`
- On Fedora: `sudo dnf install python3`
- On Arch: `sudo pacman -S python`
- On macOS: `brew install python3`

### "python3-venv not available"
- On Ubuntu/Debian: `sudo apt-get install python3-venv`
- On Fedora: `sudo dnf install python3-venv`
- On Arch: `sudo pacman -S python-venv`
- macOS: Already included with Python 3

## 📖 Next Steps

Once everything is installed:

1. Read [../README.md](../README.md) for project overview
2. Run `make setup` to install the project
3. See [INSTALLATION_WSL.md](INSTALLATION_WSL.md) for WSL-specific help
4. Run `make test` to verify the installation

---

**All prerequisites installed?** Let's go! 🚀
