# ⚙️ CONFIG.md - Configuration Globale du Projet

## 🎯 Paramètres Généraux

### Ports & Réseau
```json
{
  "server": {
    "default_port": 5555,
    "host": "localhost",
    "max_clients": 100,
    "timeout": 30
  }
}
```

### Logging
```json
{
  "logs": {
    "directory": "./data/logs",
    "format": "log_%Y-%m-%d_%H-%M-%S.txt",
    "level": "INFO",
    "max_size_mb": 50
  }
}
```

### Authentification (Day 1 Part 2+)
```json
{
  "auth": {
    "passwords_file": "./data/this_is_safe.txt",
    "rules_file": "./data/password_rules.json",
    "min_password_length": 8,
    "require_upper": true,
    "require_lower": true,
    "require_digits": true,
    "require_special": true,
    "max_failed_attempts": 3,
    "lockout_duration_seconds": 300
  }
}
```

### Cryptographie - Hash (Day 1 Part 2)
```json
{
  "password_hashing": {
    "algorithm": "md5",
    "encoding": "base64"
  }
}
```

### Cryptographie - Hash Moderne (Day 2 Part 1+)
```json
{
  "password_hashing_v2": {
    "algorithm": "bcrypt",
    "cost_factor": 12,
    "salt_bits": 128,
    "encoding": "base64"
  }
}
```

### Clés Utilisateur (Day 2 Part 2)
```json
{
  "user_keys": {
    "keys_file": "./data/user_keys_do_not_steal_plz.txt",
    "kdf_algorithm": "pbkdf2",
    "key_size_bits": 256,
    "salt_bits": 128,
    "iterations": 100000,
    "encoding": "base64"
  }
}
```

### Chiffrement Symétrique (Day 2 Part 2)
```json
{
  "symmetric_encryption": {
    "cipher": "AES",
    "mode": "CBC",
    "key_size_bits": 256,
    "block_size_bits": 128,
    "iv_bits": 128
  }
}
```

### Crypto Asymétrique (Day 3 Part 1+)
```json
{
  "asymmetric_encryption": {
    "algorithm": "RSA",
    "key_size_bits": 2048,
    "padding": "OAEP",
    "hash_algorithm": "SHA256"
  }
}
```

### Signatures Numériques (Day 3 Part 2)
```json
{
  "digital_signatures": {
    "algorithm": "RSA",
    "hash_algorithm": "SHA256",
    "padding": "PSS"
  }
}
```

---

## 📊 Règles de Mots de Passe (password_rules.json)

Fichier à créer dans `./data/password_rules.json` :

```json
{
  "rules": [
    {
      "id": 1,
      "name": "Minimum length",
      "type": "length",
      "min": 8,
      "description": "Au moins 8 caractères"
    },
    {
      "id": 2,
      "name": "Uppercase letters",
      "type": "character_class",
      "class": "uppercase",
      "min_count": 1,
      "description": "Au moins 1 lettre majuscule"
    },
    {
      "id": 3,
      "name": "Lowercase letters",
      "type": "character_class",
      "class": "lowercase",
      "min_count": 1,
      "description": "Au moins 1 lettre minuscule"
    },
    {
      "id": 4,
      "name": "Digits",
      "type": "character_class",
      "class": "digit",
      "min_count": 1,
      "description": "Au moins 1 chiffre"
    },
    {
      "id": 5,
      "name": "Special characters",
      "type": "character_class",
      "class": "special",
      "min_count": 1,
      "special_chars": "!@#$%^&*()-_=+[]{}|;:,.<>?",
      "description": "Au moins 1 caractère spécial"
    },
    {
      "id": 6,
      "name": "No common patterns",
      "type": "forbidden_pattern",
      "patterns": ["password", "123456", "qwerty", "admin", "letmein"],
      "description": "Ne pas contenir de patterns courants"
    }
  ]
}
```

---

## 🎨 Couleurs pour les Clients

Schéma déterministe basé sur hash du username:

```python
COLORS = {
    0: '\033[91m',   # Red
    1: '\033[92m',   # Green
    2: '\033[93m',   # Yellow
    3: '\033[94m',   # Blue
    4: '\033[95m',   # Magenta
    5: '\033[96m',   # Cyan
    6: '\033[97m',   # White
    7: '\033[36m',   # Dark Cyan
    8: '\033[35m',   # Dark Magenta
    9: '\033[34m',   # Dark Blue
}
RESET = '\033[0m'
```

La couleur est déterminée par : `hash(username) % len(COLORS)`

---

## 🏠 Rooms Spéciales

```json
{
  "default_room": "general",
  "special_rooms": [
    {
      "name": "general",
      "protected": false,
      "description": "Salle générale, accessible à tous"
    }
  ]
}
```

Rooms protégées par mot de passe :
- Affichage avec préfixe : 🔒 `[room_name]` (pour le distinguer visuellement)
- Format stockage: `room_name:password_hash`

---

## 📝 Format des Fichiers Data

### `this_is_safe.txt` (Day 1 Part 2)
```
username:hashed_password_in_base64
alice:mZjP8aT5xQ0=
bob:pK9mL2rS7vW=
```

### `this_is_safe.txt` (Day 2 Part 1+) - Format Amélioré
```
username:algo:cost_factor:salt:digest
alice:bcrypt:12:xt8pd3xi:$2b$12$xt8pd3xiABCDEFGHIJKLMNO...
bob:bcrypt:12:pK9mL2rS:$2b$12$pK9mL2rSABCDEFGHIJKLMNO...
```

### `user_keys_do_not_steal_plz.txt` (Day 2 Part 2)
```
username:kdf_algo:iterations:salt:key
alice:pbkdf2:100000:salt_base64:key_base64
bob:pbkdf2:100000:salt_base64:key_base64
```

### Clés Asymétriques Côté Client (Day 3 Part 1+)
```
~/.crypto-vibeness/alice/
├── alice.pub     # Clé publique (PEM)
└── alice.priv    # Clé privée (PEM, chiffrée avec la clé dérivée du MDP)
```

---

## 📋 Annuaire des Clés Publiques (Day 3 Part 2)

Stocké en mémoire sur le serveur, envoyé aux clients :

```json
{
  "public_keys": {
    "alice": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBg...",
    "bob": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBg...",
    "charlie": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBg..."
  }
}
```

---

## 🔐 Types de Messages

### Format JSON Standard (tous les jours)
```json
{
  "type": "message",
  "from": "alice",
  "room": "general",
  "timestamp": "2026-04-14T10:23:45.123456",
  "content": "Plain text or encrypted depending on day",
  "color": "\033[91m"
}
```

### Day 2 Part 2+ (Avec chiffrement symétrique)
```json
{
  "type": "message",
  "from": "alice",
  "room": "general",
  "timestamp": "2026-04-14T10:23:45.123456",
  "encrypted_content": "base64_encoded_ciphertext",
  "iv": "base64_encoded_iv"
}
```

### Day 3 Part 1+ (Avec signature)
```json
{
  "type": "message",
  "from": "alice",
  "to": "bob",
  "timestamp": "2026-04-14T10:23:45.123456",
  "encrypted_content": "base64_encoded_ciphertext",
  "iv": "base64_encoded_iv",
  "signature": "base64_encoded_signature"
}
```

---

## 🔌 Commandes Client

```
/help                      # Affiche l'aide
/join <room_name>         # Rejoindre une room
/join <room_name> <pwd>   # Rejoindre une room protégée
/create <room_name>       # Créer une room
/create <room_name> <pwd> # Créer une room protégée
/rooms                    # Lister les rooms
/users                    # Lister les users connectés
/msg <username> <text>    # Envoyer un message privé (Day 3)
/public_key <username>    # Afficher la clé publique (Day 3)
/quit                     # Quitter
```

---

## 📊 Variables d'Environnement (Optional)

```bash
export CRYPTO_VIBENESS_PORT=5555
export CRYPTO_VIBENESS_LOG_LEVEL=INFO
export CRYPTO_VIBENESS_DATA_DIR=./data
export CRYPTO_VIBENESS_DEBUG=false
```

---

## 🧪 Structure de Test

Pour chaque étape, préparer des tests:

```python
# tests/test_dayX_partY.py
def test_feature_A():
    # Arrange
    # Act
    # Assert
    pass

def test_feature_B():
    pass
```

---

## 📈 Progression de la Sécurité

| Jour | Partie | Sécurité | Status |
|------|--------|----------|--------|
| 1 | 1 | Aucune (YOLO) | ⬜ |
| 1 | 2 | Authentification + MD5 | ⬜ |
| 2 | 1 | Hash moderne + salt | ⬜ |
| 2 | 2 | + Chiffrement symétrique | ⬜ |
| 3 | 1 | + Crypto asymétrique | ⬜ |
| 3 | 2 | + E2EE + Signatures | ⬜ |

---

**Version:** 1.0  
**Dernière mise à jour:** 2026-04-14
