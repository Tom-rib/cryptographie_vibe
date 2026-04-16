# 🔐 Crypto Vibeness - Secure Chat System

A cryptographically secure IRC-style chat application with end-to-end encryption, message signatures, and modern authentication.

## 🎯 Features

### Security
- ✅ **Secure Authentication** - bcrypt password hashing with PBKDF2 key derivation
- ✅ **End-to-End Encryption** - AES-256-CBC symmetric encryption
- ✅ **Asymmetric Encryption** - RSA-2048 key exchange
- ✅ **Message Signatures** - RSA digital signatures for authenticity
- ✅ **Room Encryption** - Shared keys for group messaging
- ✅ **Secure Password Storage** - Never transmitted or logged

### Chat Features
- 💬 **Multi-user Chat** - Multiple rooms with different security levels
- 👥 **Room Management** - Create, join, and manage chat rooms
- 🔑 **Key Exchange** - Automatic RSA key registration and negotiation
- 🔒 **Visual Indicators** - See message signature status at a glance
- 📍 **Room Awareness** - Always know which room you're typing in

## 🚀 Quick Start

### Requirements
- Python 3.8+
- Linux/Mac (or WSL on Windows)

### Setup (One-time)
```bash
# Create virtual environment and install dependencies
# This automatically handles:
# - Installing python3-venv if needed (with sudo)
# - Updating apt-get if needed
# - Creating and configuring venv
# - Installing all Python dependencies
make setup
```

> **⚠️ On WSL?** If you see an error about `python3-venv`, don't worry! `make setup` now handles it automatically, including running `apt-get update` and retrying with `--fix-missing` if needed. See [docs/INSTALLATION_WSL.md](docs/INSTALLATION_WSL.md) for troubleshooting.

### Run the Application

**Terminal 1: Start Server**
```bash
make run
```

**Terminal 2: Start Client (Alice)**
```bash
make client
# Username: alice
# Password: [create a secure password]
```

**Terminal 3: Start Client (Bob)**
```bash
make client
# Username: bob
# Password: [create a secure password]
```

## 📖 Commands

All chat commands start with `/`. See [COMMANDS.md](COMMANDS.md) for the complete list.

### Common Commands
```
/help              - Show all available commands
/rooms             - List all chat rooms
/join room_name    - Join a room
/create room_name  - Create a new room
/users             - List connected users
/quit              - Disconnect and exit
```

For passwords and room creation:
```
/join secure_room password123    - Join password-protected room
/create my_room secret_pass      - Create password-protected room
```

## 🔐 Security Architecture

### Message Flow
```
User types "Hello Bob"
    ↓
[ENCRYPT] AES-256 with room/session key
[SIGN] RSA-2048 with private key
    ↓
Send to server with:
  - Plaintext (for signature verification)
  - Ciphertext (for E2EE)
  - Signature (for authenticity)
    ↓
[SERVER] Verifies signature, broadcasts to room
    ↓
Other users receive:
  - Message with signature status (🔒✓ or 🔓✗)
[DECRYPT] Using shared room key
[VERIFY] Signature matches sender's public key
    ↓
Display: [11:30:45] Bob 🔒✓: Hello Alice!
```

### Authentication Flow
```
1. User enters password
2. Password → PBKDF2 key derivation → encryption key
3. User → bcrypt password hash verification
4. Generate/load RSA keypair
5. Register public key with server
6. Ready to encrypt/sign/verify messages
```

## 📊 Project Structure

```
cryptographie_vibe/
├── README.md                 ← This file
├── COMMANDS.md              ← Chat commands reference
├── Makefile                 ← Quick commands
├── requirements.txt         ← Python dependencies
├── pyproject.toml          ← Project config
│
├── src/                     ← Main application
│   ├── server.py           ← Chat server
│   ├── client.py           ← Chat client
│   └── utils/              ← Cryptographic utilities
│       ├── crypto.py       ← AES-256 encryption
│       ├── signature.py    ← RSA signatures
│       ├── asymmetric_crypto.py ← RSA key management
│       ├── key_derivation.py ← Password key derivation
│       ├── bcrypt_hasher.py ← Password hashing
│       ├── password_manager.py ← Password validation
│       ├── entropy_calculator.py ← Entropy metrics
│       └── logger.py       ← Logging
│
├── tests/                   ← Test suite
│   ├── validate_jour*.py   ← Feature validation tests
│   └── test_*.py           ← Integration tests
│
├── docs/                    ← Documentation
│   ├── JOUR*.md            ← Development stages
│   ├── DEVELOPMENT.md      ← Developer guide
│   ├── ARCHITECTURE.md     ← System design
│   └── ...
│
└── data/                    ← Runtime data
    ├── logs/               ← Chat logs
    └── user_keys/          ← User RSA keys
```

## 🧪 Testing

### Run All Tests
```bash
make test
```

### Run Specific Feature Tests
```bash
# Test basic chat
python tests/validate_jour1_partie1.py

# Test authentication
python tests/validate_jour1_partie2.py

# Test password hashing
python tests/validate_jour2_partie1.py

# Test encryption
python tests/validate_jour2_partie2.py

# Test key exchange
python tests/validate_jour3_partie1.py

# Test signatures & E2EE
python tests/validate_jour3_partie2.py
```

## 📈 Features by Stage

### Day 1: Basic Chat & Authentication
- ✅ Multi-user IRC-style chat
- ✅ MD5 to bcrypt authentication upgrade
- ✅ Password strength validation

### Day 2: Encryption
- ✅ Modern password hashing (bcrypt + PBKDF2)
- ✅ AES-256-CBC symmetric encryption
- ✅ Room-level encryption with shared keys
- ✅ Per-user session encryption

### Day 3: Advanced Cryptography
- ✅ RSA-2048 asymmetric encryption
- ✅ RSA-PSS digital signatures
- ✅ End-to-end encryption
- ✅ Public key registration system
- ✅ Visual signature verification indicators

## 🔍 Example Session

```
$ source venv/bin/activate
$ python src/client.py

Choose username: alice
[SIGNUP] ✅ Account created
🔐 Encryption key derived from password
🔑 RSA keypair generated

[general] > hello bob
[11:30:45] Alice 🔒✓: hello bob

[general] > /join secret password123
✓ Joined room: secret
🔐 Received room key for 'secret'

[secret] > only bob can read this
[11:31:12] Alice 🔒✓: only bob can read this

[secret] > /users
👥 Connected users:
  - alice
  - bob

[secret] > /quit
✓ Goodbye!
```

## ⚙️ Configuration

### Server Settings (src/server.py)
- Default room: `general` (no password)
- Port: 5555 (TCP)
- Buffer size: 4096 bytes
- Max key derivation time: 1 second

### Cryptographic Settings
- **Password Hashing**: bcrypt (cost factor 12)
- **Key Derivation**: PBKDF2 (SHA256, 100,000 iterations)
- **Symmetric**: AES-256-CBC
- **Asymmetric**: RSA-2048
- **Signatures**: RSA-PSS with SHA256

## 🐛 Troubleshooting

### Can't connect to server
```bash
# Make sure server is running in a separate terminal
make run

# Check if port 5555 is available
lsof -i :5555
```

### Wrong password
```bash
# Just try again - client will stay connected
[general] > /join room correct_password
```

### Messages not decrypting
```bash
# Make sure you're in the same room as the sender
# Room keys are only shared among room members
/rooms  # List available rooms
/join room_name  # Join the room
```

## 📚 Documentation

For more information, see:
- [COMMANDS.md](COMMANDS.md) - Complete command reference
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - Developer guide
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design details
- [docs/JOUR*.md](docs/) - Implementation stages

## 🎓 Learning Path

This project teaches cryptography concepts through implementation:

1. **Authentication** - Password hashing, PBKDF2, bcrypt
2. **Hashing** - MD5, SHA256, security vulnerabilities
3. **Symmetric Encryption** - AES-256, block modes, IVs
4. **Asymmetric Encryption** - RSA, key exchange, key encapsulation
5. **Digital Signatures** - Non-repudiation, PSS padding, verification
6. **End-to-End Encryption** - Multi-key encryption, forward secrecy

## 📝 License

Educational project for cryptography learning.

## ✨ Latest Updates

### Session 2026-04-16
- ✅ Fixed message signature validation display
- ✅ Added room indicator to input prompt
- ✅ Improved error handling (non-critical errors don't crash client)
- ✅ Better visual feedback for message authentication

## 🚀 Next Steps

Try these scenarios:

1. **Test Signature Verification**
   - Send messages as alice
   - Look for 🔒✓ indicator
   - Messages are cryptographically signed

2. **Test Room Isolation**
   - Create a password-protected room
   - Send messages in different rooms
   - Only room members can decrypt

3. **Test Authentication**
   - Try wrong password (recovers)
   - Create account twice (error handled)
   - Reset password (not implemented, would require server)

---

**Status**: ✅ Production Ready  
**Version**: 1.0  
**Last Updated**: 2026-04-16
