# 🎯 ORCHESTRATION.md - Plan d'Exécution Complet

## 📋 Vue d'Ensemble du Projet

Ce projet est divisé en **6 étapes majeures** (2 par jour pendant 3 jours), chacune ajoutant une couche de sécurité/complexité.

### Progression Pédagogique

```
JOUR 1                        JOUR 2                      JOUR 3
┌─────────────────┐          ┌─────────────────┐         ┌─────────────────┐
│ Partie 1: YOLO  │          │ Partie 1: Hacker│         │ Partie 1: NSA   │
│ (Chat basique)  │          │ Marseillais     │         │ (Asymétrique)   │
└─────────────────┘          │ (Hash moderne)  │         └─────────────────┘
         │                    └─────────────────┘                  │
         │                            │                           │
         ▼                            ▼                           ▼
┌─────────────────┐          ┌─────────────────┐         ┌─────────────────┐
│ Partie 2: Auth  │          │ Partie 2: Hacker│         │ Partie 2: E2EE  │
│ (MD5 + Rules)   │          │ Russe           │         │ (Signatures)    │
└─────────────────┘          │ (Symétrique)    │         └─────────────────┘
                             └─────────────────┘
```

---

## 🚀 Workflow d'Exécution

### Avant de Commencer

```bash
# 1. Initialiser le projet
cd crypto-vibeness
git init
git config user.name "Crypto Agent"
git config user.email "agent@vibeness.crypto"

# 2. Créer la structure de répertoires
mkdir -p src/utils src/config data/logs tests

# 3. Créer les fichiers de configuration
touch data/config.json
touch data/password_rules.json

# 4. Initialiser le suivi Git
git add .
git commit -m "Initial commit: project structure"
```

---

## 📍 ÉTAPE 1: JOUR 1 - PARTIE 1 (YOLO)

### 🎯 Objectif
Créer un **chat multi-utilisateurs type IRC**, sans authentification ni chiffrement.

### 📂 Fichiers à Créer
- `src/server.py` (serveur de chat)
- `src/client.py` (client de chat)
- `src/utils/logger.py` (système de logging)
- `src/config/config.json` (configuration)

### 📋 Prompt à Utiliser
Fichier: `prompts/JOUR1_PARTIE1.md`

### ✅ Critères de Validation
- [ ] Le serveur écoute sur le port par défaut
- [ ] Plusieurs clients peuvent se connecter
- [ ] Chaque client choisit un username
- [ ] Les usernames ne peuvent pas être dupliqués simultanément
- [ ] Système de rooms fonctionnel (rejoindre, créer)
- [ ] Room "general" par défaut
- [ ] Messages affichés avec timestamp
- [ ] Couleurs déterministes pour les clients
- [ ] Logs créés dans `data/logs/log_YYYY-MM-DD_HH-MM-SS.txt`
- [ ] Rooms protégées visuellement distinctes

### 🧪 Test Manuel
```bash
# Terminal 1: Démarrer le serveur
python src/server.py

# Terminal 2: Premier client
python src/client.py

# Terminal 3: Deuxième client
python src/client.py

# Dans chaque client:
# > alice          (choix du username)
# > /join general  (ou appuyez sur entrée)
# > Hello!         (envoyer un message)
# > /rooms         (lister les rooms)
# > /create test   (créer une room)
# > /create secret password123  (créer une room protégée)
```

### 📊 État Après Validation
```
PROJECT_STATE.md doit indiquer:
- JOUR1_PARTIE1: ✅ VALIDÉE
- Fichiers créés: server.py, client.py, logger.py
- Prochaine étape: JOUR1_PARTIE2
```

### 📝 Commit Git
```
git add -A
git commit -m "JOUR1 PARTIE1: Chat IRC multi-utilisateurs sans authentification"
```

---

## 📍 ÉTAPE 2: JOUR 1 - PARTIE 2 (Authentification)

### 🎯 Objectif
Ajouter un **système d'authentification** avec MD5, règles de mot de passe et calcul d'entropie.

### 📂 Fichiers à Modifier/Créer
- `src/server.py` (ajouter authentification)
- `src/client.py` (ajouter écran de login)
- `src/utils/password_manager.py` (NEW - gestion des MDP)
- `src/utils/entropy_calculator.py` (NEW - calcul d'entropie)
- `data/this_is_safe.txt` (NEW - stockage des MDP)
- `data/password_rules.json` (utiliser celui de CONFIG.md)

### 📋 Prompt à Utiliser
Fichier: `prompts/JOUR1_PARTIE2.md`

### ✅ Critères de Validation
- [ ] Authentification requise avant accès au chat
- [ ] Création de compte à la première connexion
- [ ] Vérification des 3+ règles de mot de passe
- [ ] Retour indicateur de force du mot de passe (entropie)
- [ ] Mots de passe hashés en MD5
- [ ] Hash encodé en base64 (pas hex)
- [ ] Format: `username:hashed_password` dans `this_is_safe.txt`
- [ ] Vérification en temps constant
- [ ] Règles lues depuis `password_rules.json`
- [ ] Clients non-authentifiés ne reçoivent pas les messages

### 🧪 Test Manuel
```bash
# Terminal 1: Serveur
python src/server.py

# Terminal 2: Nouveau client
python src/client.py
# > Choose username: alice
# > Choose password: Secure123!
# > Password strength: 78% (exemple)
# > Re-enter password: Secure123!
# > Successfully authenticated!

# Terminal 3: Client existant
python src/client.py
# > Choose username: alice
# > Enter password: Secure123!
# > Successfully authenticated!

# Terminal 4: Client avec mauvais MDP
python src/client.py
# > Choose username: alice
# > Enter password: wrong123
# > Authentication failed
```

### 📊 État Après Validation
```
PROJECT_STATE.md doit indiquer:
- JOUR1_PARTIE2: ✅ VALIDÉE
- Fichiers créés: password_manager.py, entropy_calculator.py
- Fichiers modifiés: server.py, client.py
- Prochaine étape: JOUR2_PARTIE1
```

### 📝 Commit Git
```
git add -A
git commit -m "JOUR1 PARTIE2: Authentification avec MD5 et vérification d'entropie"
```

---

## 📍 ÉTAPE 3: JOUR 2 - PARTIE 1 (Hacker Marseillais)

### 🎯 Objectif
Remplacer MD5 par un **hash moderne avec salt**, et casser le hash laissé par le hacker.

### 📂 Fichiers à Modifier/Créer
- `src/utils/password_manager.py` (remplacer MD5 par bcrypt/argon2)
- `src/utils/hashcat_cracker.py` (NEW - intégration hashcat)
- `data/this_is_safe.txt` (migrer vers nouveau format)
- `data/md5_decrypted.txt` (NEW - résultat du cassage)
- `scripts/migrate_passwords.py` (NEW - migration MD5 → bcrypt)

### 📋 Prompt à Utiliser
Fichier: `prompts/JOUR2_PARTIE1.md`

### ✅ Critères de Validation
- [ ] Hash MD5 du hacker cassé: `35b95f7c0f63631c453220fb2a86f`
- [ ] Masque utilisé: `?u?u?l?l?u?u?s`
- [ ] Résultat stocké dans `md5_decrypted.txt`
- [ ] Tous les mots de passe ≤ 5 caractères cassés en temps raisonnable
- [ ] Remplacement par bcrypt/argon2 implémenté
- [ ] Facteur de coût inclus (ex: 12 pour bcrypt)
- [ ] Salt ≥ 96 bits, différent par MDP
- [ ] Format: `username:algo:cost:salt:digest` dans `this_is_safe.txt`
- [ ] Salt stocké à gauche du digest en base64
- [ ] Migration des anciens MDP réussie

### 🧪 Test Manuel
```bash
# 1. Casser le hash du hacker
python -m hashcat \
  -m 0 \
  -a 3 \
  35b95f7c0f63631c453220fb2a86f \
  '?u?u?l?l?u?u?s'

# 2. Vérifier le résultat dans md5_decrypted.txt

# 3. Lancer le serveur (qui migre automatiquement les MDP)
python src/server.py

# 4. Tester que les anciens comptes fonctionnent toujours
# Les MDP doivent maintenant être en bcrypt
```

### 📊 État Après Validation
```
PROJECT_STATE.md doit indiquer:
- JOUR2_PARTIE1: ✅ VALIDÉE
- Hash cassé: [le message trouvé]
- Tous les mots de passe ≤5 chars cassés
- Migration MD5 → bcrypt complète
- Prochaine étape: JOUR2_PARTIE2
```

### 📝 Commit Git
```
git add -A
git commit -m "JOUR2 PARTIE1: Cassage MD5 et migration vers bcrypt avec salt"
```

---

## 📍 ÉTAPE 4: JOUR 2 - PARTIE 2 (Hacker Russe)

### 🎯 Objectif
Ajouter le **chiffrement symétrique** des messages avec une clé dérivée du mot de passe.

### 📂 Fichiers à Modifier/Créer
- `src/utils/crypto.py` (NEW - chiffrement/déchiffrement)
- `src/utils/key_derivation.py` (NEW - KDF)
- `src/server.py` (stocker clés utilisateur)
- `src/client.py` (chiffrer/déchiffrer messages)
- `data/user_keys_do_not_steal_plz.txt` (NEW - clés utilisateur)

### 📋 Prompt à Utiliser
Fichier: `prompts/JOUR2_PARTIE2.md`

### ✅ Critères de Validation
- [ ] Clé de chiffrement générée à la création du compte
- [ ] Dérivation de clé (PBKDF2 ou équivalent)
- [ ] Clé ≥ 128 bits
- [ ] Salt dédié ≥ 96 bits
- [ ] Stockée côté serveur dans `user_keys_do_not_steal_plz.txt`
- [ ] Format: `username:algo:iterations:salt:key`
- [ ] Tous les messages chiffrés en symétrique
- [ ] Chiffrement par bloc (AES-CBC)
- [ ] IV généré aléatoirement à chaque message
- [ ] Clients peuvent communiquer entre eux
- [ ] Messages en clair jamais stockés/transmis

### 🧪 Test Manuel
```bash
# Terminal 1: Serveur
python src/server.py

# Terminal 2: Alice
python src/client.py
# > alice / Secure123! / /join general / Hello Bob!

# Terminal 3: Bob
python src/client.py
# > bob / Secure456! / /join general
# [Reçoit le message d'Alice, déchiffré]

# Vérifier les logs serveur: les messages doivent être en chiffré
```

### 📊 État Après Validation
```
PROJECT_STATE.md doit indiquer:
- JOUR2_PARTIE2: ✅ VALIDÉE
- Chiffrement symétrique implémenté
- Tous les messages de toutes les rooms chiffrés
- Prochaine étape: JOUR3_PARTIE1
```

### 📝 Commit Git
```
git add -A
git commit -m "JOUR2 PARTIE2: Chiffrement symétrique des messages avec KDF"
```

---

## 📍 ÉTAPE 5: JOUR 3 - PARTIE 1 (Hacker NSA)

### 🎯 Objectif
Implémenter la **crypto asymétrique** pour éliminer le besoin d'échanger les clés préalablement.

### 📂 Fichiers à Modifier/Créer
- `src/utils/asymmetric_crypto.py` (NEW - RSA/ECC)
- `src/server.py` (annuaire public keys, key encapsulation)
- `src/client.py` (générer paire de clés, échanger clés de session)
- `~/.crypto-vibeness/[username]/[username].pub` (clés publiques)
- `~/.crypto-vibeness/[username]/[username].priv` (clés privées)

### 📋 Prompt à Utiliser
Fichier: `prompts/JOUR3_PARTIE1.md`

### ✅ Critères de Validation
- [ ] Paire RSA/ECC générée avant connexion
- [ ] Réutilisation de paires existantes
- [ ] Clés stockées en `.pub` et `.priv`
- [ ] Échange de clé de session asymétrique
- [ ] Key encapsulation fonctionne
- [ ] Serveur ne connaît pas les clés privées
- [ ] Annuaire public keys maintenu sur serveur
- [ ] Distribution des public keys aux clients
- [ ] Chiffrement de session symétrique réutilisé
- [ ] Plus de fichier `user_keys_do_not_steal_plz.txt`

### 🧪 Test Manuel
```bash
# Terminal 1: Serveur
python src/server.py

# Terminal 2: Alice (première connexion)
python src/client.py
# > alice / Secure123!
# [Génère paire RSA 2048]
# [Envoie public key au serveur]
# [Serveur maintient l'annuaire]

# Terminal 3: Bob
python src/client.py
# > bob / Secure456!
# [Génère paire RSA 2048]
# [Reçoit public key d'Alice du serveur]

# Alice et Bob peuvent maintenant communiquer sans secret partagé préalable
```

### 📊 État Après Validation
```
PROJECT_STATE.md doit indiquer:
- JOUR3_PARTIE1: ✅ VALIDÉE
- Crypto asymétrique implémentée
- Annuaire public keys fonctionnel
- Prochaine étape: JOUR3_PARTIE2
```

### 📝 Commit Git
```
git add -A
git commit -m "JOUR3 PARTIE1: Crypto asymétrique et key encapsulation"
```

---

## 📍 ÉTAPE 6: JOUR 3 - PARTIE 2 (E2EE Complet)

### 🎯 Objectif
Implémenter l'**End-to-End Encryption** avec signatures numériques pour les messages 1-1.

### 📂 Fichiers à Modifier/Créer
- `src/utils/e2ee.py` (NEW - distribution clés pub, key setup, signatures)
- `src/server.py` (modifications pour passer les blobs, logs chiffrés)
- `src/client.py` (signature et vérification des messages)

### 📋 Prompt à Utiliser
Fichier: `prompts/JOUR3_PARTIE2.md`

### ✅ Critères de Validation (4 étapes)

**Étape 1: Distribution des Clés Publiques**
- [ ] Annuaire {username: public_key} sur serveur
- [ ] Distribué aux clients
- [ ] Clients stockent localement les clés publiques

**Étape 2: Key Setup par Paire**
- [ ] Alice génère clé de session
- [ ] Chiffre avec clé publique de Bob
- [ ] Envoie via serveur
- [ ] Bob déchiffre avec sa clé privée
- [ ] Secret partagé inconnu du serveur

**Étape 3: Chiffrement des Messages**
- [ ] Messages 1-1 chiffrés en symétrique
- [ ] Réutilise code Jour 2 Partie 2
- [ ] Serveur relaye blobs opaques

**Étape 4: Signature des Messages**
- [ ] Chaque message signé avec clé privée expéditeur
- [ ] Destinataire vérifie avec public key expéditeur
- [ ] Message rejeté si signature invalide
- [ ] Client averti en cas d'échec

### 🧪 Test Manuel
```bash
# Terminal 1: Serveur
python src/server.py

# Terminal 2: Alice
python src/client.py
# > alice / Secure123!
# > /msg bob Hello Bob! (message chiffré et signé)

# Terminal 3: Bob
python src/client.py
# > bob / Secure456!
# > /public_key alice (affiche la clé publique)
# [Reçoit message d'Alice, vérifie signature]

# Test: Intercepter et modifier un message
# -> Bob doit rejeter le message modifié
```

### 📊 État Après Validation
```
PROJECT_STATE.md doit indiquer:
- JOUR3_PARTIE2: ✅ VALIDÉE
- E2EE complet et fonctionnel
- Signatures numériques validées
- Logs serveur contiennent du chiffré uniquement
- PROJET COMPLET! 🎉
```

### 📝 Commit Git
```
git add -A
git commit -m "JOUR3 PARTIE2: E2EE avec signatures et vérification d'intégrité"
```

---

## 📄 Fichier PROJECT_STATE.md

À maintenir tout au long du projet:

```markdown
# État du Projet Crypto Vibeness

## Résumé Exécutif
- Date de démarrage: 2026-04-14
- État actuel: [EN COURS]
- Étape actuelle: [JOUR X PARTIE Y]
- Progression: [X%]

## Étapes Complétées
- [X] JOUR1 PARTIE1 ✅
- [X] JOUR1 PARTIE2 ✅
- [ ] JOUR2 PARTIE1 ⬜
- [ ] JOUR2 PARTIE2 ⬜
- [ ] JOUR3 PARTIE1 ⬜
- [ ] JOUR3 PARTIE2 ⬜

## Fichiers Créés
- src/server.py
- src/client.py
- src/utils/logger.py
- src/utils/password_manager.py
- ... [liste complète]

## Problèmes Rencontrés & Solutions
- [Description des bugs, solutions]

## Notes Techniques
- [Décisions d'architecture]
- [Librairies utilisées]
- [Améliorations futures]
```

---

## 🎓 Résumé de la Progression Pédagogique

| Jour | Partie | Focus | Concept Clé |
|------|--------|-------|-------------|
| 1 | 1 | Architecture réseau | Socket, multi-threading |
| 1 | 2 | Authentification | Hashing, entropie |
| 2 | 1 | Attaques par force brute | Hashcat, salt |
| 2 | 2 | Chiffrement symétrique | AES, KDF, IV |
| 3 | 1 | Crypto asymétrique | RSA, key encapsulation |
| 3 | 2 | Sécurité bout-à-bout | Signatures, E2EE |

---

## 📞 Commande pour Démarrer

```bash
# 1. Lire le AGENT.md (ce qui te guide toi)
# 2. Lire le CONFIG.md (toutes les configurations)
# 3. Lire ce fichier ORCHESTRATION.md (ton plan d'action)
# 4. Commencer JOUR1_PARTIE1.md
```

**Tu es prêt? C'est parti! 🚀**

---

**Version:** 1.0  
**Dernière mise à jour:** 2026-04-14
