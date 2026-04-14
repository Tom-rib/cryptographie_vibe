# Development Guide

## Project Structure

```
cryptographie_vibe/
├── src/
│   ├── __init__.py
│   ├── server.py              # IRC server with crypto
│   ├── client.py              # IRC client with crypto
│   └── utils/
│       ├── crypto.py          # AES-256-CBC encryption
│       ├── key_derivation.py  # PBKDF2-HMAC-SHA256
│       ├── bcrypt_hasher.py   # Bcrypt password hashing
│       ├── asymmetric_crypto.py  # RSA-2048 key exchange
│       ├── signature.py       # RSA-PSS signatures
│       ├── password_manager.py # User auth
│       ├── entropy_calculator.py # Cryptographic entropy
│       └── logger.py          # Logging
├── tests/
│   ├── validate_jour1_partie1.py  # Chat validation
│   ├── validate_jour1_partie2.py  # Auth validation
│   ├── validate_jour2_partie1.py  # Bcrypt validation
│   ├── validate_jour2_partie2.py  # AES validation
│   ├── validate_jour3_partie1.py  # RSA keys validation
│   └── validate_jour3_partie2.py  # E2EE + Signatures
├── data/
│   └── users.db              # User database (sqlite)
├── JOUR1_PARTIE1.md          # Chat stage
├── JOUR1_PARTIE2.md          # Auth MD5 stage
├── JOUR2_PARTIE1.md          # Bcrypt stage
├── JOUR2_PARTIE2.md          # AES-256 stage
├── JOUR3_PARTIE1.md          # RSA keys stage
├── JOUR3_PARTIE2.md          # E2EE + Signatures stage
├── PROJECT_STATE.md          # Current status
├── README.md                 # Main documentation
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Modern Python config
├── Makefile                 # Development commands
├── .gitignore              # Git ignore rules
├── .env.example            # Environment template
├── .editorconfig           # Editor settings
├── .pylintrc               # Linter config
├── CONTRIBUTING.md         # Contributing guide
├── DEVELOPMENT.md          # This file
├── LICENSE                 # MIT License
└── .github/
    ├── CODEOWNERS          # Code ownership
    └── workflows/
        └── tests.yml       # CI/CD workflow
```

## Running the Project

### Start Server
```bash
make run
# or
python3 src/server.py
```

### Start Client (in another terminal)
```bash
make client
# or
python3 src/client.py
```

### Run Tests
```bash
make test              # All tests
make test-jour1p1      # Specific stage
make test-jour2p2
make test-jour3p2
```

## Development Commands

| Command | Purpose |
|---------|---------|
| `make install` | Install dependencies |
| `make test` | Run all validation tests |
| `make clean` | Clean cache/temp files |
| `make lint` | Run pylint |
| `make format` | Format code with Black |
| `make help` | Show all commands |

## Cryptographic Modules

### 1. Password Hashing (bcrypt_hasher.py)
- Uses Bcrypt for password storage
- Auto-upgrades from MD5 on login
- 60-character hash format

**Usage:**
```python
from src.utils.bcrypt_hasher import BcryptHasher
hasher = BcryptHasher()
hash = hasher.hash_password("password123")
is_valid = hasher.verify_password("password123", hash)
```

### 2. Key Derivation (key_derivation.py)
- PBKDF2-HMAC-SHA256 with 100k iterations
- Derives 256-bit keys from passwords
- Includes salt generation

**Usage:**
```python
from src.utils.key_derivation import KeyDerivation
kdf = KeyDerivation()
key = kdf.derive_key("password123", salt)
```

### 3. AES Encryption (crypto.py)
- AES-256-CBC symmetric encryption
- Random IV per message
- PKCS7 padding

**Usage:**
```python
from src.utils.crypto import AES256Crypto
crypto = AES256Crypto()
encrypted, iv = crypto.encrypt("plaintext", key)
plaintext = crypto.decrypt(encrypted, iv, key)
```

### 4. RSA Key Exchange (asymmetric_crypto.py)
- RSA-2048 keypair generation
- OAEP padding for session key encryption
- Public key registry on server

**Usage:**
```python
from src.utils.asymmetric_crypto import RSAKeyExchange
rsa = RSAKeyExchange()
pub, priv = rsa.generate_keypair()
encrypted = rsa.encrypt_session_key(session_key, pub)
session_key = rsa.decrypt_session_key(encrypted, priv)
```

### 5. RSA Signatures (signature.py)
- RSA-PSS signatures with SHA256
- Non-repudiation: signer cannot deny
- Semantic security: different signatures for same message

**Usage:**
```python
from src.utils.signature import RSASignature
sig = RSASignature()
signature = RSASignature.sign(private_key, plaintext)
is_valid = RSASignature.verify(public_key, plaintext, signature)
```

## Security Considerations

### For Developers

1. **Private Keys**: Never commit private keys. Use `.gitignore` and `.env`
2. **Entropy**: Always use `os.urandom()` for cryptographic randomness
3. **Time Attacks**: Use `secrets.compare_digest()` for password comparison
4. **Logging**: Never log plaintext passwords or private keys
5. **Validation**: Always validate input before cryptographic operations

### For Users

1. **Session Keys**: Generated fresh for each 1-on-1 conversation
2. **Room Keys**: Shared among room members (symmetric)
3. **Private Keys**: Stored locally with restricted permissions (0o600)
4. **Signatures**: Verify sender authenticity before trusting messages

## Testing Strategy

### Validation Tests
- Each stage has comprehensive validation
- Run with: `python3 tests/validate_journN_partieX.py`
- Tests verify both functionality and security properties

### Manual Testing

```bash
# Terminal 1: Start server
python3 src/server.py

# Terminal 2: Start client (Alice)
python3 src/client.py
# Choose username: alice
# Join room or start direct message

# Terminal 3: Start another client (Bob)
python3 src/client.py
# Choose username: bob
# Send message to alice

# Terminal 4 (optional): Monitor server logs
tail -f server.log
```

## Adding New Features

### Example: Add new crypto algorithm

1. **Create module** in `src/utils/new_crypto.py`
2. **Implement class** with clear interface
3. **Add tests** in `tests/validate_journX_partieY.py`
4. **Document** in relevant `JOURNX_PARTIEY.md`
5. **Update** `PROJECT_STATE.md`
6. **Commit** with detailed message

## Debugging

### Enable Debug Logging
```python
# In src/utils/logger.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspect Encrypted Data
```python
import base64
print(base64.b64encode(encrypted_data).decode())
```

### Trace Key Exchange
- Add print statements in `asymmetric_crypto.py`
- Log public keys being exchanged
- Verify session keys match both clients

## Performance Tuning

### Optimization Points
- Bcrypt rounds: default 12 (security vs speed trade-off)
- PBKDF2 iterations: default 100k (increase for higher security)
- RSA key size: default 2048 (increase to 4096 for max security)
- AES mode: currently CBC (consider GCM for authenticated encryption)

### Profiling
```bash
python3 -m cProfile -s cumtime src/server.py
```

## CI/CD Pipeline

GitHub Actions runs:
1. Tests on Python 3.9, 3.10, 3.11
2. Linting with pylint
3. Builds Python package
4. Uploads artifacts

See `.github/workflows/tests.yml` for configuration.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError" | Run `pip install -r requirements.txt` |
| "Permission denied on private key" | Check file permissions: `chmod 0o600` |
| "Connection refused" | Ensure server is running on correct port |
| "Signature verification failed" | Check message wasn't tampered; verify sender's public key |
| "Decryption error" | Ensure correct session key; check IV wasn't corrupted |

## Contributing Code

1. Follow PEP 8 style
2. Add docstrings for public functions
3. Include security considerations
4. Run all tests: `make test`
5. Format code: `make format`
6. Update documentation
7. Write clear commit messages

---

Happy developing! 🚀
