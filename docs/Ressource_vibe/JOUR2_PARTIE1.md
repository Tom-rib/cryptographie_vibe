# 📌 JOUR2_PARTIE1.md - Hacker Marseillais (Hashcat & Bcrypt)

## 🎯 Objectif

1. **Casser un hash MD5** laissé par un hacker marseillais
2. **Remplacer MD5 par bcrypt/argon2** (hash moderne et sécurisé)
3. **Ajouter un salt** (≥96 bits, différent pour chaque utilisateur)
4. **Migrer** les anciens mots de passe hachés

---

## 📝 Contexte

L'hacker marseillais a laissé un indice sur ton serveur:

```
File: md5_yolo.txt
Content: 35b95f7c0f63631c453220fb2a86f
```

C'est un **hash MD5**. Ton objectif: le casser et découvrir le message!

Une fois cassé, tu réalises que MD5 n'est **pas assez sécurisé**. Un bon hacker peut casser **tous** les mots de passe de ≤5 caractères en quelques minutes. Tu décides de passer à une fonction de hash **moderne et robuste**.

---

## 📋 Fonctionnalités à Implémenter

### 🔨 Part 1: Cassage du Hash MD5

#### Casser avec hashcat

```bash
# Installation (Linux/Mac/Windows avec WSL)
apt-get install hashcat  # Ubuntu/Debian
brew install hashcat      # Mac

# La commande
hashcat -m 0 -a 3 35b95f7c0f63631c453220fb2a86f '?u?u?l?l?u?u?s'

# -m 0 = MD5
# -a 3 = Brute force attack
# '?u?u?l?l?u?u?s' = Masque (voir ci-dessous)
# ?u = uppercase letter
# ?l = lowercase letter
# ?d = digit
# ?s = special character
# ?a = all chars (lower, upper, digit, special)
```

#### Masque Utilisé
```
?u?u?l?l?u?u?s
= Deux majuscules, deux minuscules, deux majuscules, un caractère spécial
= Exemple: "HElLOwW!" ou "FRanCoIS!"
```

#### Résultat Attendu
Découvrir le message laissé par le hacker et le sauvegarder dans:

```
data/md5_decrypted.txt
```

Format:
```
Hash: 35b95f7c0f63631c453220fb2a86f
Message: HeLLouW!
Command used: hashcat -m 0 -a 3 35b95f7c0f63631c453220fb2a86f '?u?u?l?l?u?u?s'
Time to crack: 0.5 seconds
```

### 🔒 Part 2: Remplacement par Hash Moderne

#### Choisir bcrypt ou argon2

**Option 1: bcrypt**
```python
import bcrypt

# Hashing
salt = bcrypt.gensalt(rounds=12)  # rounds = cost factor
hashed = bcrypt.hashpw(password.encode(), salt)

# Verifying
bcrypt.checkpw(password.encode(), hashed)
```

**Option 2: argon2**
```python
from argon2 import PasswordHasher

ph = PasswordHasher()
hashed = ph.hash(password)
ph.verify(hashed, password)
```

Je recommande **bcrypt** (plus simple, plus standard).

#### Salt Requirements
- ≥ 96 bits (bcrypt génère 128 bits automatiquement)
- **Différent pour chaque utilisateur**
- Stocké avec le hash

### 📝 Nouveau Format de Stockage

```
data/this_is_safe.txt

Format: username:algo:cost:salt:digest

Exemple:
alice:bcrypt:12:xt8pd3xi:$2b$12$xt8pd3xiXXXXXXXXXXXXX...
bob:bcrypt:12:pK9mL2rS:$2b$12$pK9mL2rSXXXXXXXXXXXXX...
charlie:bcrypt:12:yZ1aB5cD:$2b$12$yZ1aB5cDXXXXXXXXXXXXX...
```

**Explication:**
- `alice` = username
- `bcrypt` = algorithm
- `12` = cost factor
- `xt8pd3xi` = salt (début du hash bcrypt en base64)
- `$2b$12$xt8pd3xi...` = hash bcrypt complet

**Note:** bcrypt intègre déjà le salt dans le hash. On l'extrait pour visibilité.

### 🔄 Migration des Anciens Mots de Passe

Créer un script `scripts/migrate_passwords.py`:

```python
def migrate_passwords():
    """Migrer from MD5 old format to bcrypt new format"""
    old_file = "data/this_is_safe.txt"
    new_file = "data/this_is_safe_v2.txt"
    
    with open(old_file) as f:
        for line in f:
            username, old_hash = line.strip().split(':')
            # On ne peut pas "rehash" un old_hash (c'est pas réversible)
            # Donc les ancien utilisateurs doivent se reconnecter
            # OU: utiliser une "rehash on login" strategy
    
    # Strategy: rehash on login (better UX)
```

**Better Strategy: Rehash on Login**
- Garder une colonne `needs_rehash` ou `version`
- Au login d'un user MD5: detecter et rehash automatiquement
- Sauvegarder le nouveau hash bcrypt

### 🛠️ Utilitaires à Modifier/Créer

#### src/utils/password_manager.py (MODIFY)
```python
class PasswordManager:
    def __init__(self, rules_file="data/password_rules.json"):
        self.rules = load_rules(rules_file)
        self.hasher = BcryptHasher()  # NEW
    
    def hash_password(self, password):
        """Hasher with bcrypt (replaces MD5)"""
        return self.hasher.hash(password)
    
    def verify_password(self, password, stored_hash):
        """Verify with bcrypt"""
        return self.hasher.verify(password, stored_hash)
    
    def needs_rehash(self, hash_str):
        """Check if hash needs upgrading"""
        # Detect old MD5 format or old bcrypt cost
        if not hash_str.startswith('$2b$'):
            return True
        return False
```

#### src/utils/bcrypt_hasher.py (NEW)
```python
import bcrypt

class BcryptHasher:
    def __init__(self, cost_factor=12):
        self.cost_factor = cost_factor
    
    def hash(self, password):
        """Hash password with bcrypt"""
        salt = bcrypt.gensalt(rounds=self.cost_factor)
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    def verify(self, password, hashed):
        """Verify password (time-safe)"""
        return bcrypt.checkpw(password.encode(), hashed.encode())
    
    def extract_components(self, bcrypt_hash):
        """Extract algo, cost, salt from bcrypt hash"""
        # $2b$12$xt8pd3xi...
        parts = bcrypt_hash.split('$')
        return {
            'algo': 'bcrypt',
            'version': parts[1],
            'cost': parts[2],
            'salt': parts[3][:22],  # First 22 chars of salt+hash
            'digest': bcrypt_hash
        }
```

#### scripts/migrate_passwords.py (NEW)
```python
def migrate_passwords():
    """Migrate old MD5 to new bcrypt format"""
    old_path = "data/this_is_safe.txt"
    new_path = "data/this_is_safe_new.txt"
    
    # Read all old passwords
    users = {}
    with open(old_path) as f:
        for line in f:
            username, old_hash = line.strip().split(':')
            users[username] = {
                'old_hash': old_hash,
                'needs_rehash': True
            }
    
    # Save new format (note: we can't verify old hashes, 
    # so users need to login to trigger rehash)
    # Or we keep both formats until next login
    
    print(f"Migrated {len(users)} users")
    print("Users must login to upgrade to bcrypt")
```

---

## 🏗️ Architecture

### Fichiers à Modifier
- `src/utils/password_manager.py` - Remplacer MD5 par bcrypt
- `src/server.py` - Intégrer rehash on login
- `data/password_rules.json` - (optionnel) ajouter règles bcrypt

### Fichiers à Créer
- `src/utils/bcrypt_hasher.py` - Classe pour bcrypt
- `scripts/migrate_passwords.py` - Migration script
- `data/md5_decrypted.txt` - Résultat du cassage

---

## ✅ Checklist de Validation

### Part 1: Cassage MD5
- [ ] hashcat installé
- [ ] Hash `35b95f7c0f63631c453220fb2a86f` cassé avec masque `?u?u?l?l?u?u?s`
- [ ] Message découvert et sauvegardé dans `md5_decrypted.txt`
- [ ] Commande hashcat documentée
- [ ] Temps de cassage enregistré

### Part 2: Brute Force Efficacité
- [ ] Tous les mots de passe ≤5 caractères peuvent être cassés rapidement
- [ ] Exemple: `password`, `admin123`, `test1`, etc.
- [ ] Bcrypt avec cost 12 rend les attaques beaucoup plus lentes

### Part 3: Bcrypt Implementation
- [ ] bcrypt installé (`pip install bcrypt`)
- [ ] Hash bcrypt générés avec cost factor 12
- [ ] Salt ≥96 bits
- [ ] Vérification fonctionne
- [ ] Ancien format MD5 ne fonctionne plus

### Part 4: Nouveau Format
- [ ] Fichier `this_is_safe.txt` au nouveau format
- [ ] Format: `username:bcrypt:12:salt:digest`
- [ ] Tous les champs présents et corrects
- [ ] Séparation visuelle avec `:` entre les composants

### Part 5: Migration
- [ ] Stratégie de migration implémentée
- [ ] Anciens users peuvent se reconnecter
- [ ] Leurs mots de passe sont upgradés à bcrypt
- [ ] Pas de perte de données

### Part 6: Sécurité
- [ ] MD5 complètement supprimé
- [ ] Mots de passe jamais en clair
- [ ] Vérification en temps constant
- [ ] Salt différent pour chaque user

---

## 🧪 Test Manuel

```bash
# 1. Casser le hash du hacker
hashcat -m 0 -a 3 35b95f7c0f63631c453220fb2a86f '?u?u?l?l?u?u?s'

# Attend le résultat...
# Result: HeLLouW! (ou autre)

# Sauvegarder dans data/md5_decrypted.txt
echo "HeLLouW!" > data/md5_decrypted.txt

# 2. Lancer le server (migration automatique)
python src/server.py
# [Server] Migrating passwords to bcrypt...
# [Server] Upgraded 3 users to bcrypt

# 3. Tester avec ancien user (alice)
python src/client.py
# > Choose username: alice
# > [Server: Username exists. Enter password]
# > Enter password: HelloWorld123!
# > Authentication successful!
# [Server logs: User alice upgraded to bcrypt]

# 4. Vérifier nouveau format
cat data/this_is_safe.txt
# alice:bcrypt:12:xt8pd3xi:$2b$12$xt8pd3xiXXXXXXXXXX...

# 5. Essayer de casser un mot de passe bcrypt
# Cette fois, c'est BEAUCOUP plus lent!
# Le coût 12 veut dire 2^12 = 4096 itérations par tentative
# Donc 1000 fois plus lent que MD5
```

---

## 💡 Astuces

1. **hashcat sur Mac**: Peut être lent, utiliser GPU si disponible
2. **Installation bcrypt**: `pip install bcrypt`
3. **Extraction du salt**: Le salt bcrypt est déjà dans le hash, on l'extrait juste pour visibilité
4. **Cost factor**: 12 est bon pour 2024. Peut être augmenté à 13+ en cas d'attaque future
5. **Rehash on login**: La meilleure stratégie pour UX

---

## 🎓 Concepts à Valider

- ✅ Attaques par brute force
- ✅ Importance du salt
- ✅ Fonction de hash itérative (bcrypt)
- ✅ Cost factor et ses implications
- ✅ Hashcat et masques
- ✅ Migration de données

---

## ⚠️ Attention aux Pièges

- ❌ Ne **JAMAIS** revenir à MD5
- ❌ Ne **JAMAIS** hard-coder le cost factor (le mettre en config)
- ❌ Ne **JAMAIS** perdre les anciens salts pendant la migration
- ❌ Ne **JAMAIS** supposer que bcrypt est inviolable (c'est juste mieux que MD5)

---

## 🚀 Prochaine Étape

Une fois cette étape ✅ **VALIDÉE**, tu passeras à **JOUR2_PARTIE2** qui ajoutera:
- Chiffrement symétrique des messages
- Dérivation de clé (KDF)
- Le serveur ne pourra pas lire les messages

---

Étape: **JOUR 2 - PARTIE 1**  
Durée estimée: 1.5-2h  
Complexité: ⭐⭐⭐ (moyen)
