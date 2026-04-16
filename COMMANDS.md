# 🎮 Chat Commands Reference

Complete guide to all available commands in Crypto Vibeness chat.

## Command Format

All commands start with `/` followed by the command name and optional arguments:

```
/command [argument1] [argument2] ...
```

## Core Commands

### `/help`
Show all available commands with descriptions.

**Usage:**
```
/help
```

**Output:**
```
❓ Commands:
  /help - Show this help
  /rooms - List all rooms
  /join <room> [password] - Join a room
  /create <room> [password] - Create a room
  /users - List all connected users
  /quit - Disconnect
```

---

### `/rooms`
List all available chat rooms on the server.

**Usage:**
```
/rooms
```

**Output:**
```
📌 Available rooms:
  - general (public)
  - secret (password protected)
  - dev-team (password protected)
```

---

### `/join <room> [password]`
Join an existing chat room.

**Arguments:**
- `room` (required) - Name of the room to join
- `password` (optional) - Password if room is protected

**Usage Examples:**

Join public room:
```
/join general
```

Join password-protected room:
```
/join secret mypassword123
```

**Output on Success:**
```
→ Joined room: general
🔐 Received room key for 'general'
```

**Output on Failure:**
```
✗ Error: Wrong password
```

**Then you can retry:**
```
[general] > /join secret correctpassword
→ Joined room: secret
```

---

### `/create <room> [password]`
Create a new chat room.

**Arguments:**
- `room` (required) - Name for the new room
- `password` (optional) - Set a password if you want a private room

**Usage Examples:**

Create public room:
```
/create my_team
```

Create password-protected room:
```
/create secret_project mypassword456
```

**Output:**
```
→ Created room: my_team
→ Joined room: my_team
```

**Notes:**
- You automatically join the room you create
- Room names are case-sensitive
- Use underscores for spaces (e.g., `dev_team` not `dev team`)

---

### `/users`
List all users currently connected to the server.

**Usage:**
```
/users
```

**Output:**
```
👥 Connected users:
  - alice
  - bob
  - charlie
```

---

### `/quit`
Disconnect from the server and exit the client.

**Usage:**
```
/quit
```

**Output:**
```
✓ Goodbye!
[Client exits]
```

**Keyboard Shortcut:**
```
Ctrl+C  (Send SIGINT)
```

---

## Message Sending

### Regular Text Messages

Simply type your message without any `/` prefix:

```
[general] > hello everyone!
[11:30:45] Alice 🔒✓: hello everyone!
```

### Message Features

**Encryption:**
- Messages are automatically encrypted using the room's shared key
- If no room key is available, messages are sent as plaintext

**Signatures:**
- Messages are digitally signed with your private key
- Signature status appears as an indicator:
  - 🔒✓ = Valid signature (authentic)
  - 🔓✗ = Invalid signature (tampered)
  - No icon = Unsigned message

**Example:**
```
[general] > my encrypted message
[11:30:50] Alice 🔒✓: my encrypted message

[general] > message from unsigned client  
[11:30:55] Bob: message from unsigned client
```

---

## Advanced Scenarios

### Scenario 1: Private Team Channel

```bash
# Alice creates a private team room
[general] > /create dev_team team_password123
→ Created room: dev_team
→ Joined room: dev_team

# Bob joins the same room
[general] > /join dev_team team_password123
→ Joined room: dev_team
🔐 Received room key for 'dev_team'

# Now they chat (only in this room, encrypted)
[dev_team] > alice: let's discuss the security update
[11:35:20] Alice 🔒✓: let's discuss the security update

[dev_team] > bob: sure, meet you in 5
[11:35:25] Bob 🔒✓: sure, meet you in 5

# Check who else is in the room
[dev_team] > /users
👥 Connected users:
  - alice
  - bob

# Switch back to general chat
[dev_team] > /join general
→ Joined room: general

[general] > I'm back in general
[11:35:50] Alice 🔒✓: I'm back in general
```

### Scenario 2: Retrying Failed Commands

```bash
# Wrong password
[general] > /join secure wrong_pass
✗ Error: Wrong password
[general] >   ← Client stays active!

# Try again with correct password
[general] > /join secure correct_pass
→ Joined room: secure
🔐 Received room key for 'secure'
[secure] > now I'm in!
```

### Scenario 3: Multi-room Monitoring

```bash
# Join general
[general] > hello
[11:40:15] Alice 🔒✓: hello

# Switch to announcements
[general] > /join announcements
→ Joined room: announcements

[announcements] > any news?
[11:40:25] Alice 🔒✓: any news?

# Go back to general
[announcements] > /join general
→ Joined room: general

# Messages are room-specific
[general] > message in general
[11:40:35] Alice 🔒✓: message in general
```

---

## Input Features

### Room Indicator

The input prompt always shows your current room:

```
[general] >        ← You're in 'general' room
[secret] >         ← You switched to 'secret' room
[dev_team] >       ← You're in 'dev_team' room
```

### Command Errors

Non-critical errors (like wrong password) don't crash the client:

```
[general] > /join secret wrong_password
✗ Error: Wrong password
[general] >  ← You can try again immediately
```

---

## Visual Indicators

### Message Authenticity

```
🔒✓  = Message has valid signature (authentic)
🔓✗  = Message has invalid signature (tampered/forged)
(empty) = Message is not signed
```

Example:
```
[11:50:10] Alice 🔒✓: I definitely sent this message
[11:50:15] Eve 🔓✗: This message was forged
[11:50:20] Bob: No signature on this message
```

### Status Messages

```
→ System message (status update)
✗ Error message (command failed)
⚠️ Warning message (recoverable issue)
✓ Success message (operation completed)
🔐 Security message (encryption/key update)
🔑 Key message (public key registered)
👥 User list
📌 Room list
❓ Help message
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Quit chat (same as `/quit`) |
| `Arrow Up` | Previous command (if supported) |
| `Arrow Down` | Next command (if supported) |
| `Enter` | Send message/command |

---

## Troubleshooting

### "Wrong password" error

The room exists but your password is incorrect.

```
[general] > /join secure_room wrong_password
✗ Error: Wrong password

[general] >  ← Try again with correct password
[general] > /join secure_room correct_password
→ Joined room: secure_room
```

### Can't find a room

The room doesn't exist on the server.

```
[general] > /join nonexistent_room
✗ Error: Wrong password  ← Usually means room not found

[general] > /rooms   ← Check available rooms
📌 Available rooms:
  - general
```

### No users listed

Either you're alone or the command failed.

```
[general] > /users
👥 Connected users:
  - alice
```

### Message not decrypted

You're in a different room than the sender, or rooms were created at different times.

```
# Solution: Join the same room
[general] > /join shared_room
→ Joined room: shared_room
🔐 Received room key for 'shared_room'
```

---

## Security Notes

⚠️ **Important Security Information:**

1. **Passwords are never shown or logged**
   - Used only to derive encryption keys
   - Stored as bcrypt hash on server (one-way)

2. **Room passwords vs encryption**
   - Room password = Required to join the room
   - Room key = Shared with all room members for encryption
   - These are different mechanisms

3. **Messages are encrypted end-to-end**
   - Server cannot read them
   - Only room members with the key can decrypt

4. **Signatures verify authenticity**
   - 🔒✓ means message is from the claimed sender
   - 🔓✗ means signature doesn't match (possible tampering)
   - No icon means message wasn't signed

5. **No private messages**
   - All messages go to the current room
   - Switch rooms to change who receives messages

---

## Tips & Tricks

### Tip 1: Use descriptive room names
```
Good:  /create backend_api_dev
Bad:   /create bak_ap_d
```

### Tip 2: Remember the room indicator
```
[room_name] >  ← Shows your current room
```

### Tip 3: List rooms before joining
```
/rooms  ← See what's available
/join room_name  ← Then join
```

### Tip 4: Check who's in the room
```
/users  ← See all connected users
```

### Tip 5: Create room, then share password
```
/create myroom password123
→ Tell others: "Join 'myroom' with password 'password123'"
```

---

## Command Summary

| Command | Purpose | Example |
|---------|---------|---------|
| `/help` | Show commands | `/help` |
| `/rooms` | List rooms | `/rooms` |
| `/join` | Join room | `/join general` |
| `/create` | Create room | `/create dev` |
| `/users` | List users | `/users` |
| `/quit` | Exit | `/quit` |
| text | Send message | `hello everyone!` |

---

**Last Updated:** 2026-04-16  
**Version:** 1.0
