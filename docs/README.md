# Documentation

This folder contains the project documentation organized for different audiences.

## Quick Links

### 🚀 For Getting Started
- **[PREREQUISITES.md](PREREQUISITES.md)** - ⭐ START HERE! System requirements and installation
- **[../README.md](../README.md)** - Project overview and quick start
- **[INSTALLATION_WSL.md](INSTALLATION_WSL.md)** - ⚠️ Having venv issues on WSL? Read this!
- **[../COMMANDS.md](../COMMANDS.md)** - Chat commands reference

### 📚 For Learning
- **[../crypto_vibeness.md](../crypto_vibeness.md)** - Project description and vision
- **[MANUAL_TESTING.md](MANUAL_TESTING.md)** - How to test the application
- **[TESTING_QUICK_REFERENCE.md](TESTING_QUICK_REFERENCE.md)** - Quick test commands

### 👨‍💻 For Development
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributing guidelines
- **[../Makefile](../Makefile)** - Available development commands
- **[Ressource_vibe/](Ressource_vibe/)** - Implementation details and stages

### 📖 Implementation Stages
Located in **[Ressource_vibe/](Ressource_vibe/)**:
- **JOUR1_PARTIE1.md** - Stage 1: Chat IRC
- **JOUR1_PARTIE2.md** - Stage 2: Authentication MD5
- **JOUR2_PARTIE1.md** - Stage 3: Bcrypt Hashing
- **JOUR2_PARTIE2.md** - Stage 4: AES-256 Encryption
- **JOUR3_PARTIE1.md** - Stage 5: RSA Key Exchange
- **JOUR3_PARTIE2.md** - Stage 6: E2EE + Signatures

## ✅ Project Status

✅ **6/6 Stages Complete**
✅ **24/24 Validation Tests Passing**
✅ **100% Project Completion**

## Key Features

### Cryptography Stack
- 🔐 Bcrypt password hashing with auto-upgrade from MD5
- 🔑 PBKDF2-HMAC-SHA256 key derivation (100k iterations)
- 🔒 AES-256-CBC symmetric encryption with random IVs
- 🔓 RSA-2048 asymmetric key exchange (OAEP)
- ✍️ RSA-PSS digital signatures with SHA256 (non-repudiation)

### Chat Features
- 💬 Full IRC chat server with authentication
- 🚀 Real-time encrypted messaging
- 🏠 Room support with shared encryption
- 📱 1-on-1 private conversations with end-to-end encryption
- ✅ Message authentication and non-repudiation
- 🔒✓ Visual signature indicators

## 🚀 Quick Start

```bash
# 1. Setup everything (auto-installs system deps)
make setup

# 2. Run validation tests
make test

# 3. Start server (Terminal 1)
make run

# 4. Start client (Terminal 2)
make client
```

## ❓ Need Help?

1. **Getting started?** → Read [../README.md](../README.md)
2. **Issues with venv on WSL?** → Read [INSTALLATION_WSL.md](INSTALLATION_WSL.md)
3. **Want to test?** → Read [MANUAL_TESTING.md](MANUAL_TESTING.md)
4. **Need all commands?** → Run `make help`

---

*Complete documentation for Crypto Vibeness - Educational cryptography project*
