# Quick Testing Reference Card

Print this page and keep it handy while testing!

## Terminal Setup (Copy-Paste Ready)

### Terminal 1 - Server
```bash
cd /path/to/cryptographie_vibe
source venv/bin/activate  # Windows: venv\Scripts\activate
python3 src/server.py
```

### Terminal 2 - Client (Alice)
```bash
cd /path/to/cryptographie_vibe
source venv/bin/activate  # Windows: venv\Scripts\activate
python3 src/client.py
# Username: alice
# Password: (first time creates user, then creates password)
```

### Terminal 3 - Client (Bob)
```bash
cd /path/to/cryptographie_vibe
source venv/bin/activate  # Windows: venv\Scripts\activate
python3 src/client.py
# Username: bob
# Password: (first time creates user)
```

---

## Quick Commands

```
# View Online Users
users

# Send Direct Message
msg bob Hello Bob!

# Create/Join Room
room general

# Send Room Message
send Hello everyone!

# Leave Room
leave

# Show Help
help

# Disconnect
exit
```

---

## Testing Scenarios

### Test 1: Basic Chat
```
Alice: msg bob Hello!
Bob:   [alice]: Hello!
Bob:   msg alice Hi!
Alice: [bob]: Hi!
```

### Test 2: Room Chat
```
Alice: room general
Alice: send Room message!
Bob:   room general
Bob:   [alice in general]: Room message!
```

### Test 3: Authentication
```
First login:
  Username: alice
  Password: mypassword
  → Creates account

Second login:
  Username: alice
  Password: mypassword
  → Verifies with Bcrypt
```

### Test 4: Encryption
```
Alice: msg bob Secret!
Server: [Encrypted data]
Bob:   ✓ Signature verified
Bob:   ✓ Message decrypted
Bob:   [alice]: Secret!
```

### Test 5: Signatures
```
Alice: msg bob Authenticated!
Bob:   ✓ Signature VALID
Bob:   [alice]: Authenticated!

(Modified message):
Bob:   ✗ Signature INVALID
Bob:   ✗ Message rejected
```

---

## What to Look For

### In Terminal 1 (Server)
```
✓ "User alice connected"
✓ "[alice to bob]: [encrypted data]"
✓ "Signature verification: alice → bob [VALID]"
```

### In Terminal 2/3 (Clients)
```
✓ "Connected as alice"
✓ "[bob]: Message text here"
✓ "Joined room: general"
```

### In Database
```bash
# Check password hashing
sqlite3 data/users.db "SELECT username, password FROM users LIMIT 1;"
# Should show: alice|$2b$12$... (60-char Bcrypt hash)
```

---

## Security Verification

### 1. Password Not Plaintext
```bash
sqlite3 data/users.db "SELECT password FROM users LIMIT 1;"
# ✓ Should see: $2b$12$... (Bcrypt hash)
# ✗ Should NOT see: password123 (plaintext)
```

### 2. Encryption in Use
```
Server logs should show:
  ✓ [Encrypted data]: 8f2a3b4c5d6e7f...
  ✗ Should NOT show: plaintext messages
```

### 3. Signatures Verified
```
Server logs should show:
  ✓ Signature verification: alice → bob [VALID]
  ✓ Messages have signature field (base64)
```

---

## Common Issues & Quick Fixes

| Issue | Fix |
|-------|-----|
| Connection refused | Make sure Terminal 1 server is running |
| ModuleNotFoundError | Run: `make install` |
| Password doesn't work | Password is case-sensitive, no spaces |
| Cannot decrypt | Wait for key exchange to complete first |
| Signature invalid | Message may have been tampered |

---

## Test Checklist (Mini Version)

Functionality:
- [ ] Chat works (Test 1)
- [ ] Rooms work (Test 2)
- [ ] Auth works (Test 3)
- [ ] Encryption works (Test 4)
- [ ] Signatures work (Test 5)

Security:
- [ ] Passwords hashed (Bcrypt)
- [ ] Messages encrypted
- [ ] Server can't decrypt
- [ ] Signatures validated

Performance:
- [ ] Messages send quickly
- [ ] Encryption instant
- [ ] No lag or hangs

---

## Next Test Steps

1. **Read:** `MANUAL_TESTING.md` for detailed steps
2. **Setup:** 3 terminals as shown above
3. **Execute:** Copy commands from this card
4. **Verify:** Check outputs match expected results
5. **Cross-check:** With `MANUAL_TESTING.md` details

---

## Full Documentation

- **MANUAL_TESTING.md** - Complete testing guide
- **JOUR1_PARTIE1.md - JOUR3_PARTIE2.md** - Stage details
- **DEVELOPMENT.md** - Architecture & code
- **CONTRIBUTING.md** - Development workflow

---

**Happy Testing!** 🧪✅
