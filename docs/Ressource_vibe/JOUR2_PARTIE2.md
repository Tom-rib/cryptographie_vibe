# 📌 JOUR2_PARTIE2.md - Hacker Russe (Chiffrement Symétrique)

## 🎯 Objectif

Implémenter le **chiffrement symétrique** de tous les messages entre utilisateurs.

Le hacker russe a enregistré tout votre trafic! Vous devez chiffrer les conversations pour qu'il ne puisse rien lire.

---

## 📝 Contexte

- Chaque utilisateur a une **clé dérivée** de son mot de passe
- Cette clé sert à chiffrer/déchiffrer les messages
- Les messages sont stockés chiffrés côté serveur
- Seul le destinataire avec la bonne clé peut déchiffrer

---

## 📋 Fonctionnalités à Implémenter

### 🔑 Part 1: Dérivation de Clé (KDF)

#### Générer la Clé à la Création du Compte

```
Password: "Secure123!"
Salt: random(128 bits)
KDF: PBKDF2 avec 100,000 itérations
Output: clé de 256 bits
```

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import os

password = "Secure123!"
salt = os.urandom(16)  # 128 bits
kdf = PBKDF2(
    algorithm=hashes.SHA256(),
    length=32,  # 256 bits
    salt=salt,
    iterations=100000,
)
key = kdf.derive(password.encode())
```

#### Sauvegarder la Clé

```
data/user_keys_do_not_steal_plz.txt

Format: username:kdf_algo:iterations:salt_b64:key_b64

alice:pbkdf2:100000:2+JW3K7p1Q8=:aBcD1eF2gH3iJ4kL5mN6oP7qR8sT9uV0=
bob:pbkdf2:100000:x9Y8z7W6v5U=:qR8sT9uV0wX1yZ2aB3cD4eF5gH6iJ7kL=
```

### 🔒 Part 2: Chiffrement des Messages

#### Cipher Utilisé: AES-256-CBC

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Pour chaque message:
key = derive_key_from_password(password)
iv = os.urandom(16)  # Nouveau IV pour chaque message!
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(message.encode()) + encryptor.finalize()

# Format à transmettre:
# {
#   "encrypted_content": base64(ciphertext),
#   "iv": base64(iv)
# }
```

#### IV (Initialization Vector)

- **Généré aléatoirement pour CHAQUE message**
- 128 bits (16 bytes)
- Stocké en clair avec le message (c'est okay!)
- Utiliser un nouvel IV à chaque fois = OBLIGATOIRE pour la sécurité

### 📝 Format des Messages Chiffrés

```json
{
  "type": "message",
  "from": "alice",
  "room": "general",
  "timestamp": "2026-04-14T10:23:45.123456",
  "encrypted_content": "aBcD1eF2gH3iJ4kL5mN6oP7qR8sT9uV0wX1yZ2aB3cD4eF5gH6iJ7kL8mN9oP0=",
  "iv": "1iJ4kL5mN6oP7qR8sT9uV0wX1yZ2aB3c=",
  "color": "\033[91m"
}
```

### 🛠️ Utilitaires à Créer/Modifier

#### src/utils/crypto.py (NEW)
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

class AES256Cipher:
    def __init__(self, key):
        """key must be 32 bytes (256 bits)"""
        self.key = key
    
    def encrypt(self, plaintext):
        """Encrypt with random IV"""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        
        return {
            'ciphertext': base64.b64encode(ciphertext).decode(),
            'iv': base64.b64encode(iv).decode()
        }
    
    def decrypt(self, ciphertext_b64, iv_b64):
        """Decrypt with provided IV"""
        ciphertext = base64.b64decode(ciphertext_b64)
        iv = base64.b64decode(iv_b64)
        
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        decryptor = cipher.encryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        return plaintext.decode()
```

#### src/utils/key_derivation.py (NEW)
```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import os
import base64

class KeyDerivation:
    ITERATIONS = 100000
    KEY_SIZE = 32  # 256 bits
    SALT_SIZE = 16  # 128 bits
    
    @staticmethod
    def derive(password, salt=None):
        """Derive key from password"""
        if salt is None:
            salt = os.urandom(KeyDerivation.SALT_SIZE)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=KeyDerivation.KEY_SIZE,
            salt=salt,
            iterations=KeyDerivation.ITERATIONS,
        )
        key = kdf.derive(password.encode())
        return key, salt
    
    @staticmethod
    def derive_with_salt(password, salt_b64):
        """Derive key using existing salt (for login)"""
        salt = base64.b64decode(salt_b64)
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=KeyDerivation.KEY_SIZE,
            salt=salt,
            iterations=KeyDerivation.ITERATIONS,
        )
        return kdf.derive(password.encode())
```

### 🔄 Workflow Complet

1. **Création de compte**
   ```
   User: "alice"
   Password: "Secure123!"
   
   Server:
   - Generate salt: random(128 bits)
   - Derive key: PBKDF2(password, salt, 100000)
   - Save: alice:pbkdf2:100000:salt_b64:key_b64
   ```

2. **Envoi de message**
   ```
   Client Alice:
   - Load key from local storage
   - Create IV: random(128 bits)
   - Encrypt: AES-256-CBC(message, key, IV)
   - Send: {encrypted_content, iv}
   
   Server:
   - Log the encrypted message (not readable!)
   - Relay to room
   ```

3. **Réception de message**
   ```
   Client Bob:
   - Load key from local storage
   - Receive: {encrypted_content, iv}
   - Decrypt: AES-256-CBC(ciphertext, key, iv)
   - Display: plaintext message
   ```

### 📂 Fichiers à Créer/Modifier

#### Côté Serveur
- `src/server.py` - Générer clé à signup, relayer messages chiffrés
- `data/user_keys_do_not_steal_plz.txt` (NEW) - Stocker les clés

#### Côté Client
- `src/client.py` - Chiffrer/déchiffrer au send/receive
- `~/.crypto-vibeness/username/key.txt` (NEW) - Stocker la clé localement

#### Utilitaires
- `src/utils/crypto.py` (NEW)
- `src/utils/key_derivation.py` (NEW)

---

## ✅ Checklist de Validation

### Dérivation de Clé
- [ ] PBKDF2 avec SHA256 implémenté
- [ ] 100,000 itérations
- [ ] Clé de 256 bits
- [ ] Salt de 128 bits, différent par user
- [ ] Salt sauvegardé pour pouvoir re-dériver à login

### Chiffrement Symétrique
- [ ] AES-256-CBC implémenté
- [ ] IV généré aléatoirement pour chaque message
- [ ] Encryption fonctionne
- [ ] Decryption fonctionne
- [ ] Ciphertext en base64

### Stockage de Clé
- [ ] Clé sauvegardée côté serveur dans `user_keys_do_not_steal_plz.txt`
- [ ] Format: `username:algo:iterations:salt:key`
- [ ] Clé sauvegardée côté client localement
- [ ] Clé recréée au login via PBKDF2

### Messages Chiffrés
- [ ] Tous les messages chiffrés (même en room "general")
- [ ] Messages jamais stockés en clair
- [ ] Logs serveur ne contiennent que du chiffré
- [ ] Clients peuvent communiquer et décrypter

### Interopérabilité
- [ ] Alice envoie à Bob dans "general"
- [ ] Bob peut déchiffrer (même clé dérivée du même algo)
- [ ] Charlie dans la même room voit du chiffré (n'a pas la clé)

### Sécurité
- [ ] Jamais le même IV deux fois
- [ ] Clés jamais loggées
- [ ] Passwords jamais stockés
- [ ] Temps constant pour comparaison

---

## 🧪 Test Manuel

```bash
# 1. Démarrer le serveur
python src/server.py
# [Server] Keys file will be created at: data/user_keys_do_not_steal_plz.txt

# 2. Alice se crée un compte
python src/client.py  # Terminal 2
# > Choose username: alice
# > Enter password: SecureP@ss123!
# > [Generated encryption key...]
# > [Saved key locally to ~/.crypto-vibeness/alice/key.txt]

# Vérifier côté serveur:
cat data/user_keys_do_not_steal_plz.txt
# alice:pbkdf2:100000:2+JW3K7p1Q8=:aBcD1eF2gH3iJ4kL5mN6oP7qR8sT9uV0=

# 3. Bob se crée un compte
python src/client.py  # Terminal 3
# > Choose username: bob
# > Enter password: BobSecure456!@
# > [Generated encryption key...]

# 4. Alice envoie un message
alice> /join general
alice> Hello Bob!
# Client Alice chiffre le message
# Message envoyé au serveur chiffré

# 5. Vérifier dans les logs serveur
cat data/logs/log_*.txt | grep "Hello Bob"
# [10:23:45] [MESSAGE] alice -> general: aBcD1eF2gH3iJ4kL5mN6oP7qR8sT9uV0wX1yZ2aB...
# (message chiffré, pas lisible!)

# 6. Bob reçoit et déchiffre
bob> /join general
# Bob reçoit le message chiffré
# Client Bob déchiffre avec sa clé... 
# WAIT! Bob ne peut pas déchiffrer! (clé différente)

# Alice et Bob ont des clés DIFFÉRENTES!
# Donc ce n'est pas bon pour multi-user rooms...
# À la prochaine étape (Day 3), on va fixer ça avec E2EE
```

---

## 💡 Astuces

1. **Installation**: `pip install cryptography`
2. **IV**: Générer un nouveau IV à CHAQUE message (pas réutiliser!)
3. **Base64**: Tous les bytes doivent être encodés en base64 pour JSON
4. **PBKDF2 iterations**: Plus = plus sécurisé mais plus lent. 100k est bon.
5. **Clés locales**: Les stocker de manière sécurisée (chiffrer avec master password?)

---

## ⚠️ Problem: Shared Keys dans Multi-User Rooms

**À ce stade, il y a un problème architecturel:**
- Chaque user a sa propre clé dérivée du mot de passe
- Mais dans une room "general", multiple users veulent se parler
- Comment partager la clé?

**Solution temporaire (Day 2):**
- Générer une clé de session UNIQUE par room
- Tous les users de la room la reçoivent au join
- Problème: serveur connaît la clé (peut lire!)

**Solution finale (Day 3):**
- E2EE par paire (alice ↔ bob)
- Chaque paire a sa propre clé de session
- Chiffrée avec la clé asymétrique de l'autre
- Serveur ne peut jamais lire

---

## 🎓 Concepts à Valider

- ✅ Dérivation de clé (KDF, PBKDF2)
- ✅ Chiffrement par bloc (AES-CBC)
- ✅ IV et son importance
- ✅ Base64 encoding
- ✅ Stockage sécurisé de clés

---

## 🚀 Prochaine Étape

Une fois cette étape ✅ **VALIDÉE**, tu passeras à **JOUR3_PARTIE1** qui ajoutera:
- Crypto asymétrique (RSA)
- Key encapsulation
- Éliminer le besoin de clés partagées

---

Étape: **JOUR 2 - PARTIE 2**  
Durée estimée: 2-2.5h  
Complexité: ⭐⭐⭐⭐ (difficile)
