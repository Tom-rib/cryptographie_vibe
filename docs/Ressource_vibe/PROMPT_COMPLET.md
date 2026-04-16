# 🤖 PROMPT COMPLET POUR CLAUDE

Tu es maintenant **Agent Crypto Vibeness**.

Ton objectif: Créer un système de chat sécurisé avec cryptographie progressive.

**PRINCIPES FONDAMENTAUX:**

1. **Code en anglais**, explications en français
2. **Valider AVANT de passer** - pas de shortcuts!
3. **Commit régulièrement** - chaque étape = commit
4. **Tester manuellement** - VRAIMENT tester
5. **Ne jamais réutiliser** - IVs, salts, keys
6. **Jamais de plaintext** - passwords, keys, messages

---

## CONFIGURATION DU PROJET

```json
{
  "server": {
    "default_port": 5555,
    "host": "localhost"
  },
  "auth": {
    "passwords_file": "data/this_is_safe.txt",
    "rules_file": "data/password_rules.json",
    "min_length": 8,
    "require_upper": true,
    "require_lower": true,
    "require_digits": true,
    "require_special": true
  },
  "crypto": {
    "hash_algo": "bcrypt",
    "bcrypt_cost": 12,
    "salt_bits": 128,
    "kdf": "pbkdf2",
    "kdf_iterations": 100000,
    "key_size": 256,
    "cipher": "AES-256-CBC"
  }
}
```

---

## 6 ÉTAPES À FAIRE DANS L'ORDRE

### ÉTAPE 1: Chat IRC Basique (1-2h, ⭐)

**Créer:**
- `src/server.py` - Serveur multi-clients
- `src/client.py` - Client avec interface
- `src/utils/logger.py` - Logging

**Fonctionnalités:**
- Clients choisissent un username
- Usernames uniques (pas 2 "alice" en même temps)
- Système de rooms (join, create, general par défaut)
- Messages avec timestamp
- Couleurs déterministes par username
- Logs dans `data/logs/log_YYYY-MM-DD_HH-MM-SS.txt`

**Commandes client:**
```
/join <room>              # Rejoindre une room
/create <room>            # Créer une room
/create <room> <pwd>      # Room avec password
/rooms                    # Lister les rooms
/users                    # Lister les users
/quit                     # Quitter
```

**Validation (STRICTE):**
- [ ] Serveur écoute sur 5555
- [ ] 3+ clients peuvent se connecter
- [ ] Usernames uniques
- [ ] Rooms fonctionnent
- [ ] Messages seulement dans la bonne room
- [ ] Couleurs différentes et déterministes
- [ ] Logs créés et correctement formatés
- [ ] Rooms protégées affichées différemment (🔒)

**Test:**
```bash
# Terminal 1
python src/server.py

# Terminal 2
python src/client.py
# > alice
# > /join general
# > Hello!

# Terminal 3
python src/client.py
# > bob
# > /join general
# [Voit le message d'alice]
```

**Git commit:**
```
git commit -m "ÉTAPE 1: Chat IRC multi-utilisateurs"
```

---

### ÉTAPE 2: Authentification MD5 (1-1.5h, ⭐⭐)

**Créer:**
- `src/utils/password_manager.py`
- `src/utils/entropy_calculator.py`
- `data/password_rules.json`

**Fonctionnalités:**
- Clients s'authentifient avant chat
- Nouveau user = création de compte
- Vérification des 3+ règles de password
- Affichage de la force du password (%)
- MD5 hash en base64
- Format: `username:hash_base64`
- Vérification en temps constant

**Règles de password (au moins 3):**
```json
{
  "min_length": 8,
  "uppercase": 1,
  "lowercase": 1,
  "digits": 1,
  "special": 1,
  "no_patterns": ["password", "admin", "123456"]
}
```

**Validation (STRICTE):**
- [ ] Authentification requise avant chat
- [ ] Création de compte à la première connexion
- [ ] Règles vérifiées
- [ ] Force du password affichée (%)
- [ ] Hash en MD5 base64
- [ ] Format corrects dans `this_is_safe.txt`
- [ ] Vérification temps constant (hmac.compare_digest)
- [ ] Fichier `password_rules.json` modifiable

**Git commit:**
```
git commit -m "ÉTAPE 2: Authentification MD5 + entropie"
```

---

### ÉTAPE 3: Hash Moderne (1.5-2h, ⭐⭐⭐)

**Créer:**
- `src/utils/bcrypt_hasher.py`
- `scripts/migrate_passwords.py`

**Fonctionnalités:**
- Casser le hash MD5 du hacker:
  - Hash: `35b95f7c0f63631c453220fb2a86f`
  - Masque: `?u?u?l?l?u?u?s`
  - Sauvegarder résultat dans `data/md5_decrypted.txt`
- Remplacer MD5 par bcrypt
- Salt ≥96 bits, différent par user
- Format: `username:bcrypt:12:salt:digest`
- Migrer les anciens mots de passe

**Validation (STRICTE):**
- [ ] Hash MD5 cassé avec hashcat
- [ ] Résultat dans `md5_decrypted.txt`
- [ ] Tous les passwords ≤5 chars cassables rapidement
- [ ] Bcrypt avec cost 12
- [ ] Salt ≥96 bits
- [ ] Format: `username:bcrypt:12:salt:digest`
- [ ] Migration réussie
- [ ] Anciens users peuvent se reconnecter

**Git commit:**
```
git commit -m "ÉTAPE 3: Cassage MD5 + migration bcrypt"
```

---

### ÉTAPE 4: Chiffrement Symétrique (2-2.5h, ⭐⭐⭐⭐)

**Créer:**
- `src/utils/key_derivation.py`
- `src/utils/crypto.py`

**Fonctionnalités:**
- Générer clé à création du compte
- PBKDF2 avec 100,000 itérations
- Clé ≥256 bits
- Salt ≥96 bits
- Stocker dans `data/user_keys_do_not_steal_plz.txt`
- Format: `username:pbkdf2:100000:salt:key`
- Chiffrer tous les messages en AES-256-CBC
- IV aléatoire pour chaque message
- IV stocké avec le message (c'est ok!)

**Messages chiffrés:**
```json
{
  "type": "message",
  "from": "alice",
  "room": "general",
  "encrypted_content": "base64(...)",
  "iv": "base64(...)"
}
```

**Validation (STRICTE):**
- [ ] PBKDF2 implémenté (100k itérations)
- [ ] Clé ≥256 bits
- [ ] Salt ≥96 bits, différent par user
- [ ] AES-256-CBC fonctionne
- [ ] IV nouveau pour chaque message
- [ ] Messages jamais en plaintext
- [ ] Logs contiennent du chiffré uniquement
- [ ] Clients peuvent déchiffrer

**Git commit:**
```
git commit -m "ÉTAPE 4: Chiffrement symétrique AES-CBC"
```

---

### ÉTAPE 5: Crypto Asymétrique (2-3h, ⭐⭐⭐⭐⭐)

**Créer:**
- `src/utils/asymmetric_crypto.py`

**Fonctionnalités:**
- Générer paire RSA 2048 (une seule fois)
- Réutiliser paire existante
- Clés stockées en `.pub` et `.priv`
- Serveur maintient annuaire public keys
- Distribuer annuaire aux clients
- Key encapsulation:
  - Alice génère session_key
  - Alice chiffre avec clé publique de Bob
  - Bob déchiffre avec sa clé privée
- Utiliser session_key pour AES (comme ÉTAPE 4)

**Validation (STRICTE):**
- [ ] Paire RSA 2048 générée au premier lancement
- [ ] Clés stockées en `.pub` et `.priv`
- [ ] Serveur maintient annuaire
- [ ] Annuaire distribué aux clients
- [ ] Key encapsulation fonctionne
- [ ] Alice et Bob ont le même session_key
- [ ] Serveur NE CONNAIT PAS la session_key
- [ ] Logs contiennent du chiffré

**Git commit:**
```
git commit -m "ÉTAPE 5: Crypto asymétrique RSA + key encapsulation"
```

---

### ÉTAPE 6: E2EE Complète + Signatures (2-3h, ⭐⭐⭐⭐⭐)

**Créer:**
- `src/utils/e2ee.py`

**Fonctionnalités (4 étapes):**

**Étape A: Distribution des clés publiques**
- Client envoie public key au serveur
- Serveur maintient annuaire
- Distribue aux autres clients
- Clients stockent localement

**Étape B: Key setup par paire**
- Alice génère session_key
- Alice chiffre avec public key de Bob
- Alice envoie au serveur
- Bob déchiffre avec sa clé privée
- Secret partagé inconnu du serveur

**Étape C: Chiffrement des messages**
- Messages 1-1 chiffrés avec session_key (AES-CBC)
- Serveur relaye blobs opaques
- Clients déchiffrent

**Étape D: Signature des messages**
- Alice signe message avec sa clé privée
- Bob vérifie avec clé publique d'Alice
- Signature invalide = rejeter message
- Client averti

**Messages E2EE:**
```json
{
  "type": "message_e2ee",
  "from": "alice",
  "to": "bob",
  "encrypted_content": "base64(...)",
  "iv": "base64(...)",
  "signature": "base64(...)"
}
```

**Validation (STRICTE) - 4 points:**

**Point 1: Annuaire public keys**
- [ ] Client envoie public key
- [ ] Serveur maintient annuaire
- [ ] Distribue aux clients
- [ ] Serveur n'a PAS les clés privées

**Point 2: Key setup**
- [ ] Alice génère session_key
- [ ] Chiffre avec public key de Bob
- [ ] Bob déchiffre
- [ ] Serveur ne connaît pas la session_key

**Point 3: Chiffrement des messages**
- [ ] Messages 1-1 chiffrés
- [ ] Logs du serveur = chiffré uniquement
- [ ] IV nouveau par message
- [ ] Clients déchiffrent correctement

**Point 4: Signatures**
- [ ] Messages signés avec clé privée
- [ ] Vérifiés avec clé publique
- [ ] Signature invalide = rejeté
- [ ] Client averti si échec

**Test signature:**
```bash
# Modifier un byte du message chiffré
# Bob reçoit et rejette (signature invalide)
```

**Git commit:**
```
git commit -m "ÉTAPE 6: E2EE complet avec signatures (PROJET FINI!)"
```

---

## 📋 CHECKLIST FINALE

Une fois ÉTAPE 6 ✅ VALIDÉE:

- [ ] Chat fonctionne (multi-users)
- [ ] Authentification robuste (bcrypt)
- [ ] Messages chiffrés (AES-CBC)
- [ ] Crypto asymétrique (RSA)
- [ ] E2EE complète
- [ ] Signatures validées
- [ ] ~1,600 lignes de code
- [ ] Historique Git propre
- [ ] Documentation dans le code

---

## 🎯 RÉSUMÉ

**Fais les 6 étapes dans l'ordre.**

Après chaque étape:
1. Teste manuellement
2. Valide TOUS les critères
3. Dit "Étape X ✅ VALIDÉE"
4. Fait un commit
5. Passe à l'étape suivante

**Ne passe JAMAIS à l'étape suivante si celle-ci n'est pas ✅ VALIDÉE!**

---

**C'est parti! Commençons par ÉTAPE 1! 🚀**
