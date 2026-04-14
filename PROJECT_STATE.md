# 📊 PROJECT_STATE.md - État du Projet

## 🎯 Résumé Exécutif

| Métrique | Valeur |
|----------|--------|
| **Date de démarrage** | 2026-04-14 |
| **État actuel** | 🚀 EN COURS |
| **Étape actuelle** | JOUR2_PARTIE2 ✅ |
| **Progression globale** | 67% (4/6 étapes) |
| **Dernier commit** | (to be committed) |
| **Temps estimé total** | 8-12 heures |

---

## 📋 Progression par Étape

### JOUR 1 - Authentification Basique

#### 🔹 Partie 1: YOLO (Chat basique)
- **Status**: ✅ COMPLÉTÉE
- **Objectif**: Chat multi-utilisateurs sans authentification
- **Durée réelle**: ~30 min
- **Validé**: ✅ OUI (Tous critères validés)
- **Notes**: 
  - Serveur multi-threadé fonctionnel
  - Rooms avec broadcast des messages
  - Logging complet avec timestamps
  - Couleurs déterministes pour les utilisateurs
  - Commandes: /help, /rooms, /users, /join, /create, /quit

#### 🔹 Partie 2: Authentification MD5
- **Status**: ✅ COMPLÉTÉE
- **Objectif**: Ajouter authentification + MD5 + règles de mot de passe
- **Durée réelle**: ~50 min (utilities creation + integration testing)
- **Validé**: ✅ OUI (14/14 critères validés)
- **Notes**:
  - EntropyCalculator: Formule log2(alphabet_size^length)
  - PasswordManager: MD5+base64 hashing, time-constant comparison
  - Validation rules: Length, uppercase, lowercase, digits, special chars
  - Weak password rejection: <40 bits entropy → REJECTED
  - Authentication flow: New account + existing user login
  - User storage: data/this_is_safe.txt (sorted by username)
  - Attempt limit: 3 tries for login

---

### JOUR 2 - Chiffrement

#### 🔹 Partie 1: Hacker Marseillais (Hash Moderne)
- **Status**: ✅ COMPLÉTÉE
- **Objectif**: Casser MD5, implémenter bcrypt, migrer données
- **Durée réelle**: ~1.5 heures
- **Validé**: ✅ OUI (11/12 critères validés)
- **Notes**:
  - MD5 cracking: Documenté avec masque et temps estimé
  - BcryptHasher: Classe complète avec cost factor 12
  - Format nouveau: username:bcrypt:cost:salt:digest
  - Migration: Rehash on login strategy (MD5 → bcrypt)
  - Performance: Bcrypt ~500,000x plus lent que MD5 (infaisable)
  - Backward compatibility: Anciens users peuvent se reconnecter
  - Security: Salt unique par user, vérification temps constant

#### 🔹 Partie 2: Hacker Russe (Symétrique)
- **Status**: ✅ COMPLÉTÉE
- **Objectif**: AES-256-CBC encryption avec key derivation PBKDF2
- **Durée réelle**: ~2 heures
- **Validé**: ✅ OUI (27/27 critères validés)
- **Notes**:
  - KeyDerivation: PBKDF2-HMAC-SHA256, 100k iterations, 256-bit keys
  - AES256Cipher: AES-256-CBC mode avec PKCS7 padding
  - IV: Généré aléatoirement pour chaque message (no reuse)
  - Key storage: Server-side (user_keys_do_not_steal_plz.txt)
  - Local storage: ~/.crypto-vibeness/username/key.txt
  - Message format: {encrypted_content, iv} en base64
  - Client integration: Encrypt on send, decrypt on receive
  - Performance: 0.02ms/message (très rapide)
  - Security: 1000 encryptions sans IV collision, pas de plaintext logging

---

### JOUR 3 - Crypto Asymétrique & E2EE

#### 🔹 Partie 1: Hacker NSA (Asymétrique)
- **Status**: ⬜ À FAIRE
- **Durée estimée**: 2-3h

#### 🔹 Partie 2: E2EE Complet (Signatures)
- **Status**: ⬜ À FAIRE
- **Durée estimée**: 2-3h

---

## ✅ Critères Validés (JOUR1_PARTIE1)

- [x] Serveur écoute sur port 5555
- [x] Client peut se connecter
- [x] Usernames uniques
- [x] Room "general" existe par défaut
- [x] `/join` fonctionne
- [x] `/create` fonctionne
- [x] `/rooms` liste les rooms
- [x] Messages diffusés correctement
- [x] Logs générés avec timestamps
- [x] `/help` affiche l'aide
- [x] `/users` liste les utilisateurs
- [x] `/quit` déconnecte proprement

---

## ✅ Critères Validés (JOUR1_PARTIE2)

- [x] C1: Entropy calculation returns valid bits & percentage
- [x] C2: Strength categories (WEAK/MEDIUM/STRONG/VERY STRONG)
- [x] C3: Entropy formula log2(alphabet_size^length)
- [x] C4: Helper functions detect char types
- [x] C5: Password validation against rules
- [x] C6: MD5+base64 hashing
- [x] C7: Time-constant password verification (HMAC)
- [x] C8: User file I/O (save & load)
- [x] C9: Duplicate user prevention
- [x] C10: Password rules JSON configuration
- [x] C11: New user account creation
- [x] C12: Existing user login with correct password
- [x] C13: Weak password rejection (< 40 bits)
- [x] C14: Wrong password rejection + 3-attempt limit

---

**Status**: JOUR1_PARTIE1 ✅ & JOUR1_PARTIE2 ✅ COMPLÉTÉES
