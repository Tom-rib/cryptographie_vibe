# Manual Testing Guide

Complete guide for manually testing the Crypto Vibeness project. This document walks you through all features step-by-step with detailed explanations.

## Quick Start

### Step 1: Setup Everything (First Time Only)

One command to create venv and install all dependencies:

```bash
make setup
```

This will:
- ✓ Create virtual environment (venv/)
- ✓ Install all dependencies (bcrypt, cryptography, etc.)
- ✓ Ready to use immediately

### Step 1 Alternative: Fast Start Server or Client

For quick testing, use one of these commands that setup + starts automatically:

```bash
# In Terminal 1 - Start server (with automatic setup)
make setup-serveur

# In Terminal 2 - Start client (with automatic setup)
make setup-client
```

### Step 2: Activate Virtual Environment (Every Session)

```bash
source venv/bin/activate
# Windows: venv\Scripts\activate
```

You'll see `(venv)` in your prompt:
```
(venv) $ _
```

### Step 3: Run Automated Validation (Verify Everything Works)

```bash
make test
```

Expected result: ✅ All 120 criteria passing

## Manual Test Setup

### Option 1: Using make commands (Easiest)

**Terminal 1: Server**
```bash
make setup-serveur
```

**Terminal 2: Client 1 (Alice)**
```bash
make setup-client
# Follow prompts: Username: alice, Password: [create password]
```

**Terminal 3: Client 2 (Bob)**
```bash
make setup-client
# Follow prompts: Username: bob, Password: [create password]
```

### Option 2: Manual setup with individual commands

You'll need **3 terminals** for manual testing:

**Terminal 1: Server**
```bash
# First time or new session
source venv/bin/activate  # Windows: venv\Scripts\activate

# Then start server
make run
# OR: python3 src/server.py
```

**Terminal 2: Client 1 (Alice)**
```bash
# First time or new session
source venv/bin/activate  # Windows: venv\Scripts\activate

# Then start client
make client
# OR: python3 src/client.py
# Follow prompts: Username: alice, Password: [create password]
```

**Terminal 3: Client 2 (Bob)**
```bash
# First time or new session
source venv/bin/activate  # Windows: venv\Scripts\activate

# Then start client
python3 src/client.py
# Follow prompts: Username: bob, Password: [create password]
```

**Note:** Each terminal is independent. Always activate venv in each terminal before running commands.

---

## Testing Stages

### Stage 1: Chat IRC (JOUR1_PARTIE1)

**Objective:** Basic IRC chat functionality without encryption

#### Test 1.1: Start Server
```
Terminal 1 - Server Output:
  ✓ Server started on localhost:5000
  ✓ Waiting for connections...
```

#### Test 1.2: Connect Clients
```
Terminal 2 (Alice):
  Username: alice
  ✓ Connected as alice
  >

Terminal 3 (Bob):
  Username: bob
  ✓ Connected as bob
  >
```

#### Test 1.3: Direct Messages
```
Terminal 2 (Alice):
  > msg bob Hello Bob!
  ✓ Message sent

Terminal 3 (Bob):
  [alice]: Hello Bob!
  > msg alice Hi Alice!
  ✓ Message sent

Terminal 2 (Alice):
  [bob]: Hi Alice!
```

**Expected Result:** ✅ Messages delivered in plaintext

#### Test 1.4: Join Room
```
Terminal 2 (Alice):
  > room general
  ✓ Joined room: general
  
Terminal 2 (Alice):
  > send Hello everyone!
  ✓ Message sent to room

Terminal 1 (Server):
  [alice in general]: Hello everyone!

Terminal 3 (Bob):
  > room general
  ✓ Joined room: general
  [alice in general]: Hello everyone!
  > send Hi there!
  
Terminal 2 (Alice):
  [bob in general]: Hi there!
```

**Expected Result:** ✅ Room chat working, all members see messages

---

### Stage 2: Authentication with MD5 (JOUR1_PARTIE2)

**Objective:** User authentication with MD5 hashing (legacy)

#### Test 2.1: First Login (Password Hashing)
```
Terminal 2 (Alice - First Time):
  Username: alice
  Password (will create new user): password123
  ✓ User 'alice' created with MD5 password
  ✓ Connected as alice
```

#### Test 2.2: Wrong Password
```
Terminal 2 (Alice):
  Username: alice
  Password: wrongpassword
  ✗ Authentication failed: Invalid password
  Connection closed
```

**Expected Result:** ✅ Wrong password rejected

---

### Stage 3: Bcrypt Password Hashing (JOUR2_PARTIE1)

**Objective:** Strong password hashing with Bcrypt

#### Test 3.1: Create User with Bcrypt
```
Terminal 2 (Charlie):
  Username: charlie
  Password: SecurePassword!
  ✓ User 'charlie' created with Bcrypt
  ✓ Connected as charlie
```

#### Test 3.2: Second Login
```
Terminal 2 (Charlie - Second Time):
  Username: charlie
  Password: SecurePassword!
  ✓ Bcrypt verification successful
  ✓ Connected as charlie
```

**Expected Result:** ✅ Bcrypt hash verified correctly

---

### Stage 4: AES-256 Encryption (JOUR2_PARTIE2)

**Objective:** Encrypted messages using AES-256-CBC

#### Test 4.1: Direct Encrypted Message
```
Terminal 2 (Alice):
  > msg bob Secret message!
  ✓ Message encrypted with AES-256
  ✓ Message sent with IV: [random hex]

Terminal 1 (Server):
  ✓ Received encrypted message from alice to bob
  [Encrypted data]: 8f2a3b4c5d6e7f...

Terminal 3 (Bob):
  ✓ Signature verified: alice
  ✓ Message decrypted
  [alice]: Secret message!
```

**Expected Result:** ✅ Message encrypted in transit, decrypted on receipt

#### Test 4.2: Room Encryption
```
Terminal 2 (Alice joins room):
  > room general
  ✓ Joined room: general
  Room encryption key: [256-bit key]

Terminal 2 (Alice in room):
  > send Room message
  ✓ Message encrypted with room key
  
Terminal 3 (Bob joins room):
  > room general
  ✓ Joined room: general
  ✓ Received room key
  ✓ Can decrypt all messages
```

**Expected Result:** ✅ All room members share same key, all can decrypt

---

### Stage 5: RSA Key Exchange (JOUR3_PARTIE1)

**Objective:** Asymmetric key exchange for session key establishment

#### Test 5.1: RSA Keypair Generation
```
Terminal 2 (Alice - First login):
  ✓ Generating RSA-2048 keypair...
  ✓ Public key registered on server
  ✓ Private key stored locally: ~/.crypto_vibe/alice_private.pem
```

**Expected Result:** ✅ RSA-2048 keypair generated

#### Test 5.2: Session Key Establishment
```
Terminal 2 (Alice to Bob):
  > msg bob Hello with RSA exchange
  ✓ Generating session key: [256-bit random]
  ✓ Encrypting session key with Bob's public key...

Terminal 3 (Bob):
  ✓ Received encrypted session key
  ✓ Decrypting with private key...
  ✓ Session key established and matches Alice's!
```

**Expected Result:** ✅ Session key encrypted, only Bob can decrypt

---

### Stage 6: E2EE with Digital Signatures (JOUR3_PARTIE2)

**Objective:** Complete encryption + authentication with non-repudiation

#### Test 6.1: Message Signing
```
Terminal 2 (Alice):
  > msg bob Authenticated message!
  ✓ Encrypting message with session key
  ✓ Signing plaintext with private key...
  ✓ Signature created: [RSA-PSS signature]
```

**Expected Result:** ✅ Message encrypted AND signed

#### Test 6.2: Signature Verification
```
Terminal 3 (Bob):
  ✓ Received message from alice
  ✓ Verifying signature with Alice's public key...
  ✓ Signature VALID ✓
  ✓ Message decrypted
  [alice]: Authenticated message!
```

**Expected Result:** ✅ Signature verified, message decrypted

#### Test 6.3: Tampering Detection
```
Scenario: Message is tampered with in transit

Terminal 3 (Bob):
  ✓ Received message from alice
  ✓ Verifying signature...
  ✗ Signature INVALID ✗
  ✗ Message rejected: Tampering detected
```

**Expected Result:** ✅ Tampered message rejected

---

## Commands Reference

### Basic Commands

```
# User Management
> users                    List all online users
> whoami                   Show current user

# Direct Messages
> msg <username> <text>    Send private message
> history <username>       Show conversation history

# Room Management
> room <name>              Join or create room
> rooms                    List available rooms
> send <text>              Send message to current room
> room-users               List users in current room
> leave                    Leave current room

# System
> help                     Show help menu
> exit                     Disconnect
```

### What to Observe

During each test, check:

1. **Terminal Output**
   - Messages appear without errors
   - Timestamps are correct
   - User names are accurate

2. **Server Logs**
   - Connections are logged
   - Messages are processed
   - Errors are reported

3. **Data Flow**
   - Messages reach intended recipients
   - No plaintext in server logs (when encrypted)
   - Signatures are validated

---

## Security Checks During Testing

### Check 1: Password Hashing
```bash
# Inspect database
sqlite3 data/users.db "SELECT username, password FROM users LIMIT 1;"

# Should see:
# alice|$2b$12$...  (60-char Bcrypt hash, NOT plaintext)
```

### Check 2: Encryption in Transit
```
Server logs should show:
  ✓ [Encrypted data]: 8f2a3b4c5d6e7f... (hex, not readable)
  NOT: plaintext message content
```

### Check 3: Signature Verification
```
Server logs should show:
  ✓ Signature verification: alice → bob [VALID]
  Messages have signature field with base64 data
```

### Check 4: RSA Keys
```
Terminal 2 (Alice):
  > keys
  Public key: -----BEGIN PUBLIC KEY-----
              MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...
              [RSA-2048 public key content]
```

---

## Troubleshooting

### Problem: "Connection refused"
```
Solution:
  1. Make sure server is running in Terminal 1
  2. Check port 5000 is not in use
  3. Use: lsof -i :5000 (Linux/Mac) or netstat -ano | findstr :5000 (Windows)
```

### Problem: "ModuleNotFoundError"
```
Solution:
  1. Activate virtual environment: source venv/bin/activate
  2. Install dependencies: make install
  3. Verify: python3 -c "import bcrypt"
```

### Problem: "Wrong password even though it's correct"
```
Solution:
  1. Password is case-sensitive
  2. No leading/trailing spaces
  3. On first login, password is being set (created, not checked)
```

### Problem: "Cannot decrypt message"
```
Solution:
  1. Session key not established yet (wait for key exchange)
  2. Wrong recipient (message sent to wrong user)
  3. Session expired (reconnect and try again)
```

### Problem: "Signature verification failed"
```
Solution:
  1. Message may have been tampered
  2. Public key on server may be outdated
  3. User may have reconnected (new keys)
```

---

## Test Checklist

Print this and check off as you test:

### Functionality Tests
- [ ] Stage 1: Connect and chat in plaintext
- [ ] Stage 1: Join rooms and broadcast
- [ ] Stage 2: Create users and authenticate
- [ ] Stage 2: Wrong password rejected
- [ ] Stage 3: Bcrypt password creation
- [ ] Stage 3: Bcrypt password verification
- [ ] Stage 4: Encrypted messages between users
- [ ] Stage 4: Room messages encrypted
- [ ] Stage 5: RSA keypair generated
- [ ] Stage 5: Session keys established
- [ ] Stage 6: Messages are signed
- [ ] Stage 6: Signatures are verified
- [ ] Stage 6: Tampered messages rejected

### Security Tests
- [ ] Password not stored in plaintext
- [ ] Session key not in server logs
- [ ] Encrypted message looks like random data
- [ ] Signature format is base64
- [ ] Wrong password rejected
- [ ] Wrong signer cannot verify
- [ ] Private key file protected (0o600)

### Performance Tests
- [ ] Encryption/decryption completes quickly
- [ ] Key exchange doesn't hang
- [ ] Signature verification instant
- [ ] Room messages broadcast promptly

---

## Next Steps

1. **Run manual tests** following this guide
2. **Cross-reference** with automated tests (`make test`)
3. **Check** docs in `JOUR1_PARTIE1.md` through `JOUR3_PARTIE2.md`
4. **Report** any issues or unexpected behavior

---

## For Developers

See:
- `DEVELOPMENT.md` - Architecture and code details
- `CONTRIBUTING.md` - Contributing guidelines
- `docs/` - Complete documentation

---

**Questions?** Check the relevant JOUR*.md file or review the test code in `tests/validate_jour*.py`

**Happy testing!** 🧪✅
