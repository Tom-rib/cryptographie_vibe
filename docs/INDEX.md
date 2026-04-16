# 📚 Documentation Index

Complete guide to all documentation files for the Crypto Vibeness project.

## 🚀 For Users (Start Here!)

**New to Crypto Vibeness? Start with the root directory:**

- [`README.md`](../README.md) - Project overview and quick start
- [`COMMANDS.md`](../COMMANDS.md) - Chat commands reference

---

## 👨‍💻 For Developers

### Project Development (How it was built)

| File | Purpose | Read When |
|------|---------|-----------|
| [`COMMENCER_ICI.md`](COMMENCER_ICI.md) | Quick start for development | First time setup |
| [`DEVELOPMENT.md`](DEVELOPMENT.md) | Developer guide and workflow | Getting started with code |
| [`crypto_vibeness.md`](crypto_vibeness.md) | Project context and goals | Understanding the vision |

### Implementation Stages (JOUR = Day)

Each day has 2 parts with detailed specifications:

| Day | Part 1 | Part 2 |
|-----|--------|--------|
| **Day 1: Auth** | [`JOUR1_PARTIE1.md`](JOUR1_PARTIE1.md) - Basic chat | [`JOUR1_PARTIE2.md`](JOUR1_PARTIE2.md) - MD5 to bcrypt |
| **Day 2: Encryption** | [`JOUR2_PARTIE1.md`](JOUR2_PARTIE1.md) - Password hashing | [`JOUR2_PARTIE2.md`](JOUR2_PARTIE2.md) - AES encryption |
| **Day 3: Advanced** | [`JOUR3_PARTIE1.md`](JOUR3_PARTIE1.md) - RSA keys | [`JOUR3_PARTIE2.md`](JOUR3_PARTIE2.md) - E2EE + signatures |

### Testing & Validation

| File | Purpose | Command |
|------|---------|---------|
| [`TESTING_QUICK_REFERENCE.md`](TESTING_QUICK_REFERENCE.md) | Quick test commands | Reference |
| [`MANUAL_TESTING.md`](MANUAL_TESTING.md) | Detailed testing guide | Step-by-step testing |

### Contributing

| File | Purpose |
|------|---------|
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Guidelines for contributors |

---

## 📖 Reading Paths

### Path 1: User (Just want to chat)
```
1. README.md (root)
2. COMMANDS.md (root)
3. Start chatting!
```

### Path 2: Developer (Want to understand the code)
```
1. README.md (root)
2. DEVELOPMENT.md
3. Pick a JOUR*.md stage to understand
4. Read the implementation
```

### Path 3: Full Deep Dive (Want to rebuild it)
```
1. COMMENCER_ICI.md
2. DEVELOPMENT.md
3. crypto_vibeness.md
4. JOUR1_PARTIE1.md → JOUR3_PARTIE2.md (in order)
5. TESTING_QUICK_REFERENCE.md
6. MANUAL_TESTING.md
```

---

## 🔍 File Descriptions

### COMMENCER_ICI.md
**Quick Start for Development**

Starting point for developers who want to get the project running quickly.
- Setup instructions
- Quick verification steps
- Common issues

**Read if:** You just want to get the project running locally

---

### DEVELOPMENT.md
**Developer Guide**

Comprehensive guide for developers working on the codebase.
- Code structure
- How to run tests
- Development workflow
- Debugging tips

**Read if:** You're modifying or extending the code

---

### crypto_vibeness.md
**Project Context**

Background and context for the entire project.
- Educational goals
- Security concepts covered
- Real-world applications
- Design philosophy

**Read if:** You want to understand why things are designed this way

---

### JOUR1_PARTIE1.md through JOUR3_PARTIE2.md
**Stage-by-Stage Implementation**

Detailed specifications for each development stage:

1. **JOUR1_PARTIE1** - Basic IRC chat (no security)
2. **JOUR1_PARTIE2** - Authentication with MD5 → bcrypt upgrade
3. **JOUR2_PARTIE1** - Modern password hashing (bcrypt + PBKDF2)
4. **JOUR2_PARTIE2** - AES-256-CBC encryption
5. **JOUR3_PARTIE1** - RSA asymmetric encryption
6. **JOUR3_PARTIE2** - Digital signatures + E2EE

Each file includes:
- Clear objectives
- Implementation details
- Architecture recommendations
- Validation checklists
- Manual testing procedures

**Read if:** You want to understand a specific security concept or rebuild a stage

---

### TESTING_QUICK_REFERENCE.md
**Quick Test Commands**

One-page reference of all test commands.
- `make test` - Run all tests
- `make validate` - Run specific validation
- Command examples

**Read if:** You need quick command reference

---

### MANUAL_TESTING.md
**Detailed Testing Guide**

Step-by-step manual testing procedures.
- Setup instructions
- Test scenarios
- Expected outputs
- Troubleshooting

**Read if:** You're testing features or debugging

---

### CONTRIBUTING.md
**Contribution Guidelines**

How to contribute to the project.
- Code style
- Git workflow
- Pull request process
- Testing requirements

**Read if:** You want to contribute improvements

---

## 📚 Quick Lookup

### "How do I...?"

| Question | Answer |
|----------|--------|
| ...use the chat? | Read [`COMMANDS.md`](../COMMANDS.md) |
| ...set up locally? | Read [`DEVELOPMENT.md`](DEVELOPMENT.md) |
| ...understand the architecture? | Read [`DEVELOPMENT.md`](DEVELOPMENT.md) |
| ...test my changes? | Read [`MANUAL_TESTING.md`](MANUAL_TESTING.md) |
| ...run all tests? | Read [`TESTING_QUICK_REFERENCE.md`](TESTING_QUICK_REFERENCE.md) |
| ...understand encryption? | Read [`JOUR2_PARTIE2.md`](JOUR2_PARTIE2.md) |
| ...understand signatures? | Read [`JOUR3_PARTIE2.md`](JOUR3_PARTIE2.md) |
| ...fix a bug? | Read [`DEVELOPMENT.md`](DEVELOPMENT.md) |

---

## 🎓 Learning Order

### For Cryptography Understanding
```
1. crypto_vibeness.md          ← Overview
2. JOUR1_PARTIE2.md            ← Hashing (MD5 → bcrypt)
3. JOUR2_PARTIE1.md            ← Password security
4. JOUR2_PARTIE2.md            ← Symmetric encryption (AES)
5. JOUR3_PARTIE1.md            ← Asymmetric encryption (RSA)
6. JOUR3_PARTIE2.md            ← Digital signatures + E2EE
```

### For Python/Implementation Understanding
```
1. DEVELOPMENT.md              ← Code structure
2. JOUR1_PARTIE1.md            ← Basic socket programming
3. JOUR1_PARTIE2.md            ← Authentication logic
4. JOUR2_PARTIE2.md            ← Encryption implementation
5. JOUR3_PARTIE1.md            ← Key management
6. JOUR3_PARTIE2.md            ← Signature verification
```

---

## 📊 Project Structure Visualization

```
Documentation Organization:

ROOT DIRECTORY (For Users)
├── README.md           ← What is this? How to use?
└── COMMANDS.md         ← Chat command reference

docs/ DIRECTORY (For Developers)
├── README_DEVELOPMENT.md ← Old README (archived)
├── DEVELOPMENT.md        ← Developer guide
├── crypto_vibeness.md    ← Project vision
├── COMMENCER_ICI.md      ← Quick start
│
├── Implementation Stages:
├── JOUR1_PARTIE1.md      ← Stage 1
├── JOUR1_PARTIE2.md      ← Stage 2
├── JOUR2_PARTIE1.md      ← Stage 3
├── JOUR2_PARTIE2.md      ← Stage 4
├── JOUR3_PARTIE1.md      ← Stage 5
├── JOUR3_PARTIE2.md      ← Stage 6
│
├── Testing:
├── TESTING_QUICK_REFERENCE.md
├── MANUAL_TESTING.md
│
├── Contributing:
├── CONTRIBUTING.md
│
└── archive/            ← Old documentation
```

---

## 🔗 Cross References

### By Topic

**Authentication & Passwords:**
- JOUR1_PARTIE2.md - Authentication
- JOUR2_PARTIE1.md - Password hashing
- DEVELOPMENT.md - Password security

**Encryption:**
- JOUR2_PARTIE2.md - AES encryption
- JOUR3_PARTIE1.md - RSA encryption
- JOUR3_PARTIE2.md - End-to-end encryption

**Testing:**
- TESTING_QUICK_REFERENCE.md - Quick reference
- MANUAL_TESTING.md - Detailed guide
- JOUR*.md files - Each has validation section

**Security:**
- All JOUR files - Security concepts
- DEVELOPMENT.md - Security considerations
- CONTRIBUTING.md - Secure coding practices

---

## 📝 Document Status

| File | Status | Last Updated |
|------|--------|--------------|
| README.md | ✅ Production Ready | 2026-04-16 |
| COMMANDS.md | ✅ Complete | 2026-04-16 |
| DEVELOPMENT.md | ✅ Complete | 2026-04-14 |
| JOUR1_PARTIE1.md | ✅ Complete | 2026-04-14 |
| JOUR1_PARTIE2.md | ✅ Complete | 2026-04-14 |
| JOUR2_PARTIE1.md | ✅ Complete | 2026-04-14 |
| JOUR2_PARTIE2.md | ✅ Complete | 2026-04-14 |
| JOUR3_PARTIE1.md | ✅ Complete | 2026-04-14 |
| JOUR3_PARTIE2.md | ✅ Complete | 2026-04-14 |
| MANUAL_TESTING.md | ✅ Complete | 2026-04-15 |
| TESTING_QUICK_REFERENCE.md | ✅ Complete | 2026-04-14 |

---

## 🎯 Getting Started Checklist

- [ ] Read `README.md` (root)
- [ ] Read `COMMANDS.md` (root)
- [ ] Run `make setup`
- [ ] Run `make test` to verify setup
- [ ] Try chatting with multiple clients
- [ ] Read `DEVELOPMENT.md` if you want to understand the code
- [ ] Read `JOUR*.md` files if you want to rebuild it

---

**Last Updated:** 2026-04-16  
**Version:** 1.0
