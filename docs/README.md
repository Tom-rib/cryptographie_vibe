# Documentation

This folder contains the project documentation organized for different audiences.

## Quick Links

### 🚀 For Getting Started
- **[../COMMENCER_ICI.md](../COMMENCER_ICI.md)** - Start here! Quick setup guide

### 📚 For Learning
- **[../README.md](../README.md)** - Complete project overview
- **[../crypto_vibeness.md](../crypto_vibeness.md)** - Project description and features
- **[../PROJECT_STATE.md](../PROJECT_STATE.md)** - Current project status

### 👨‍💻 For Development
- **[../DEVELOPMENT.md](../DEVELOPMENT.md)** - Development guide and architecture
- **[../CONTRIBUTING.md](../CONTRIBUTING.md)** - Contributing guidelines
- **[../Makefile](../Makefile)** - Available development commands

### 📖 Implementation Stages
- **[../JOUR1_PARTIE1.md](../JOUR1_PARTIE1.md)** - Stage 1: Chat IRC
- **[../JOUR1_PARTIE2.md](../JOUR1_PARTIE2.md)** - Stage 2: Authentication MD5
- **[../JOUR2_PARTIE1.md](../JOUR2_PARTIE1.md)** - Stage 3: Bcrypt Hashing
- **[../JOUR2_PARTIE2.md](../JOUR2_PARTIE2.md)** - Stage 4: AES-256 Encryption
- **[../JOUR3_PARTIE1.md](../JOUR3_PARTIE1.md)** - Stage 5: RSA Key Exchange
- **[../JOUR3_PARTIE2.md](../JOUR3_PARTIE2.md)** - Stage 6: E2EE + Signatures

### 📦 Project Files
- **[../LICENSE](../LICENSE)** - MIT License
- **[../requirements.txt](../requirements.txt)** - Python dependencies
- **[../pyproject.toml](../pyproject.toml)** - Python project config

## Archive

The **[archive/](archive/)** folder contains development documentation and guides used during the project implementation. See [archive/README.md](archive/README.md) for details.

## Project Status

✅ **6/6 Stages Complete**
✅ **120/120 Validation Criteria Passed**
✅ **100% Project Completion**

## Key Features

### Cryptography Stack
- 🔐 Bcrypt password hashing with auto-upgrade from MD5
- 🔑 PBKDF2-HMAC-SHA256 key derivation (100k iterations)
- 🔒 AES-256-CBC symmetric encryption with random IVs
- 🔓 RSA-2048 asymmetric key exchange (OAEP)
- ✍️ RSA-PSS digital signatures with SHA256 (non-repudiation)

### Architecture
- 💬 Full IRC chat server with authentication
- 🚀 Real-time encrypted messaging
- 🏠 Room support with shared encryption
- 📱 1-on-1 private conversations with end-to-end encryption
- ✅ Message authentication and non-repudiation

## Quick Start

```bash
# 1. Install dependencies
make install

# 2. Run validation tests
make test

# 3. Start server (Terminal 1)
make run

# 4. Start client (Terminal 2)
make client
```

## Need Help?

1. **Getting started?** → Read [../COMMENCER_ICI.md](../COMMENCER_ICI.md)
2. **Want to develop?** → Read [../DEVELOPMENT.md](../DEVELOPMENT.md)
3. **Contributing?** → Read [../CONTRIBUTING.md](../CONTRIBUTING.md)
4. **Need commands?** → Run `make help`

---

*Complete documentation for Crypto Vibeness educational cryptography project*
