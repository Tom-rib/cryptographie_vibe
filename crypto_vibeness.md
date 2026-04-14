# Crypto Vibeness 🔐
## Découvrir le monde merveilleux de la crypto grâce au vibe coding

---

## 📚 Introduction

La crypto(-graphie) est un domaine absolument passionnant... plus encore que les crypto(-monnaies)!

Elle se compose en gros de **trois branches** :

### 1️⃣ **Les Hash** (md5, sha256...)
Un outil essentiel que l'on retrouve dans :
- L'indexation de données
- Toutes les blockchains
- La gestion de mots de passe
- Git... et même les RIB!

### 2️⃣ **La Crypto Symétrique**
Utilisée dans :
- L'intégralité des conversations numériques sécurisées (HTTPS, VPNs, WiFi protégés, emails d'un même provider, Signal...)
- Le chiffrement de backups (iCloud, etc.)
- Les paiements électroniques...

### 3️⃣ **La Crypto Asymétrique**
*La plus grande invention cryptographique du XXe siècle.*

Permet de :
- Communiquer de façon sécurisée avec n'importe qui sans secret commun préalable
- Échanger des clés pour le trafic HTTPS
- Utiliser des signatures et certificats numériques
- Établir des connexions SSH...

⚠️ Plus complexe, elle nécessite une paire **"clé publique/clé privée"**.

---

## 🎯 Le But du Projet

Faire un **système de chat sécurisé en Python** en utilisant progressivement ces trois branches.

### Points clés :
- ✅ Vous n'aurez rien à coder vous-mêmes (c'est presque impossible)
- ✅ Vous devrez **comprendre** les concepts essentiels pour valider l'output de votre agent
- ✅ Utiliser un **agent IA** (Claude Code, Copilot CLI, etc.), pas un vulgaire chatbot
- ✅ **Valider à chaque étape** avant de passer à la suivante
- ✅ **Commit régulièrement** quand votre travail progresse

### La clé :
> Un LLM moderne peut sortir une implémentation d'un algo en quelques secondes, ce qui ne nous intéresse pas vraiment. Ce qui nous intéresse, c'est de **construire un système cryptographique complet**, prompt après prompt, **en validant régulièrement** votre avancement.

---

## 🚨 Avertissement sur la Crypto

> ⚠️ **IMPORTANT**: La cryptographie est un domaine ardu et subtil qu'on a tôt fait de mal utiliser.

- Le but n'est **PAS** de concevoir un système réellement sécurisé
- Ce n'est **PAS** du code utilisable en production
- L'objectif est de **manipuler concrètement** les concepts fondamentaux

> **"Don't roll your own crypto"** — sauf si c'est pour apprendre!

---

## 👿 Votre Système Cryptographique

Durant votre quête, vous allez rencontrer des personnes mal intentionnées :

1. 🇫🇷 **Un hacker marseillais** (Day 2)
2. 🇷🇺 **Un hacker russe** (Day 2)
3. 🕵️ **Un hacker de la NSA** (Day 3)

Votre objectif : **Sécuriser votre système** contre ces adversaires... si vous le pouvez!

---

## 📋 Indications Générales

- ✅ Lisez le **sujet de la semaine entière** avant de vous lancer
- ✅ Utilisez un **agent IA**, pas un vulgaire chatbot
- ✅ Réfléchissez à votre fichier `.md` de configuration — chaque élément de contexte est important
- ✅ Communiquez avec votre agent en **français**, mais le code en **anglais**

---

# 📅 JOUR 1

## Partie 1️⃣ : YOLO
> *"From a security perspective, if you're connected, you're screwed."* — Daniel "DJB" J. Bernstein

Un système de chat multi-utilisateurs type IRC, **sans authentification, ni chiffrement**.

### Fichiers à créer :
- `server.py`
- `client.py`

### Fonctionnalités attendues :

#### 🖥️ Serveur
- Écoute sur un port passé en paramètre (ou port par défaut en configuration)
- Gère plusieurs clients simultanément
- Les clients se connectent au même port (ou port par défaut)

#### 👤 Authentification (basique)
- Chaque client choisit un **username** au démarrage
- Le serveur s'assure qu'un même username ne peut pas se connecter 2 fois en même temps

#### 🏠 Système de Rooms
- Utilisateurs peuvent créer et rejoindre des rooms
- Certaines rooms sont **protégées par mot de passe**
- Par défaut, tout le monde dans la room `general`
- Les rooms protégées s'affichent **différemment** dans la console

#### 💬 Messagerie
- Chaque client ne voit que les messages de sa room actuelle
- Messages associés d'un **timestamp**

#### 🎨 Couleurs
- Couleur affectée automatiquement et **déterministe** (basée sur IP+port ou username)
- Même couleur pour tous les clients, toute la durée du chat

#### 📝 Logs
- Le serveur produit des logs de chaque événement client
- Format : `log_2026-04-14_10-23-45.txt`

### ✅ Validation :
Chaque fonctionnalité doit être testée et validée. **Ne passez pas à la suite si ça ne marche pas!**

---

## Partie 2️⃣ : Ô temps!... tification
> *"Rule 1 of cryptanalysis: check for plaintext."* — Robert Morris

Impossible de savoir qui se cache derrière ces pseudos! Vous implémentez un **système d'authentification**.

### Fonctionnalités attendues :

#### 🔐 Authentification
- Clients doivent s'authentifier par mot de passe
- Clients non-authentifiés ne reçoivent **pas** les messages
- Authentification faite **avant** l'accès au chat, création de rooms, etc.

#### 👥 Enregistrement
- Utilisateur reconnu → authentification directe
- Utilisateur nouveau → création compte avec mot de passe confirmé

#### 🛡️ Règles de Mot de Passe
- Implémenter **au moins 3 règles** pour le choix du mot de passe
- Si valides → retourner un **indicateur de force du mot de passe** (basé sur l'entropie)

#### 🔑 Stockage des Mots de Passe
- Tous les mots de passe **hashés** — jamais en clair
- Utiliser **MD5** pour le hash (pour cette étape)
- Hash encodé en **base64** (pas hexadécimal)

#### 📄 Fichier de Mots de Passe
- Fichier : `this_is_safe.txt`
- Format : `username:hashed_password`
- Une ligne par utilisateur

#### ⚙️ Règles Modifiables
- Règles conservées dans un fichier à part (format libre)
- Modifiables
- Relues à chaque lancement du serveur

#### ⏱️ Sécurité
- Vérification du mot de passe en **temps constant**

### ✅ Validation :
Testez et validez chaque fonctionnalité. **Ne passez pas à la suite si ça ne marche pas!**

---

# 📅 JOUR 2

## Partie 1️⃣ : Le Hacker Marseillais 🇫🇷
> *"When in doubt, use brute force."* — Ken Thompson (Turing Award 1983)

Un hacker marseillais récupère votre fichier `this_is_safe.txt`. Vous décidez de vous mettre à sa place pour **casser les mots de passe**.

### 🔨 Outils
- Utiliser **hashcat** (via apt-get, brew, Docker...)
- Le hacker a laissé un mystérieux fichier : `md5_yolo.txt`

```
35b95f7c0f63631c453220fb2a86f
```

### Fonctionnalités attendues :

#### 🎯 Cassage de Hash
- Déterminer le message du hacker avec hashcat
- Masque : `?u?u?l?l?u?u?s`
- Mode : brute force
- Résultat dans : `md5_decrypted.txt`

#### 🔓 Cassage de Mots de Passe
- Casser tous les mots de passe **≤ 5 caractères** en temps raisonnable

#### 🔄 Amélioration du Hash
- Remplacer **MD5 par un hash moderne** et sécurisé
- Options : algos récents finalistes du NIST, ciphers de DJB, etc.
- **Doit avoir un facteur de coût**

#### 🧂 Salage
- Ajouter un **sel** avant le hash
- Minimum **96 bits**
- **Différent** pour chaque mot de passe
- Stocké en **base64**, à gauche du digest

#### 📋 Format de Stockage
Séparation visuelle entre `user`, `algo`, `salt` et `mdp` :

```
jeanmichel:bcrypt:12:xt8pd3xi:ab4%x...
```

Signification :
- `jeanmichel` = username
- `bcrypt` = algorithme
- `12` = facteur de coût
- `xt8pd3xi` = salt
- `ab4%x...` = digest du hash

---

## Partie 2️⃣ : Le Hacker Russe 🇷🇺
> *"There are only a few hard problems in cryptography — one of them is correctly implementing cryptography."* — Adi Shamir (Turing Award 2002)

Un hacker russe a enregistré **tout le trafic**! Vous implémentez le **chiffrement symétrique** des conversations.

### Fonctionnalités attendues :

#### 🔑 Génération de Clé
- **Clé de chiffrement** générée à la création du compte
- Dérivée d'un **secret saisi par l'utilisateur**
- Utiliser une **fonction de dérivation de clé** (KDF)
- Utiliser un **sel dédié par utilisateur** (mêmes contraintes qu'avant)

#### 💾 Stockage de Clé
**Côté serveur :**
- Fichier : `user_keys_do_not_steal_plz.txt`
- Format : même que les mots de passe
- Conservée avec le sel

**Côté client :**
- Libre (exemple : `./users/babar/key.txt`)

#### 📏 Taille de Clé
- Minimum **128 bits**

#### 🔐 Chiffrement des Messages
- Chaque utilisateur chiffre ses messages avec sa clé
- Envoie au serveur
- Le serveur peut communiquer avec tous les utilisateurs connectés

#### 🔒 Cipher
Deux options :
1. Implémenter le **TEA**
2. Utiliser les ciphers de **libsodium/openssl** et binder

**Contrainte :** Utiliser du **chiffrement par bloc**

---

# 📅 JOUR 3

## Partie 1️⃣ : Do you have anything to hide? 🕵️
> *"Anyone, from the most clueless amateur to the best cryptographer, can create an algorithm that he himself can't break. It's not even hard. What is hard is creating an algorithm that no one else can break, even after years of analysis."* — Bruce Schneier

Problème : échanger les clés de chiffrement via des canaux non-sécurisés = annule l'intérêt!

**La NSA s'intéresse à vous.** Il est temps de muscler votre jeu.

### Solution : Crypto Asymétrique (Diffie-Hellman / RSA)
- Clé privée / clé publique
- Échanger un secret
- L'utiliser pour chiffrement symétrique (encapsulation de clé)

### Fonctionnalités attendues :

#### 🔐 Génération de Paire
- Client génère une **paire de clés** avant la connexion
- Ou réutilise une paire existante

#### 🔑 Échange de Clé Symétrique
- Utiliser **crypto asymétrique** pour s'échanger une clé de chiffrement symétrique
- Utiliser ensuite cette clé pour communiquer (modèle Jour 2 Partie 2)

#### 📁 Stockage des Clés
- ❌ **Pas de** `user_keys_do_not_steal_plz.txt` côté serveur
- ✅ Côté client : deux fichiers avec même nom
  - `.priv` = clé privée
  - `.pub` = clé publique

---

## Partie 2️⃣ : Des Bouts de Bout en Bout 🔐
> *"If you are designing cryptosystems, you've got to think about long-term applications. You've got to try to figure out how to build something that is secure against technology in the next century that you cannot even imagine."* — Whitfield Diffie (Turing Award 2015)

La NSA a noyauté le groupe! Vous ne pouvez plus faire confiance au serveur.

### Solution : End-to-End Encryption (E2EE)
- Messages signés et vérifiés par chaque partie
- Serveur = "honnête-mais-curieux" (route fidèlement les messages, essaie de lire le contenu)
- E2EE **uniquement pour échanges 1-1** (pas pour les rooms)

### 📍 Étape 1 : Distribution des Clés Publiques

#### Processus :
1. Client se connecte → envoie sa clé publique au serveur
2. Serveur maintient un **annuaire** : `{username: public_key}`
3. Serveur distribue cet annuaire aux autres clients
4. Chaque client stocke **localement** les clés publiques des gens avec qui il a déjà parlé

#### ✅ Validation :
Un client peut afficher la clé publique d'un autre client sans que le serveur ait accès aux clés privées.

---

### 🔄 Étape 2 : Établissement d'une Clé de Session par Paire

#### Processus :
1. **Alice** veut parler à **Bob**
2. Alice génère une **clé symétrique de session**
3. Alice la chiffre avec la **clé publique de Bob**
4. Alice l'envoie via le serveur
5. **Bob** la déchiffre avec sa **clé privée**
6. Tous deux ont un **secret partagé** que le serveur ne connaît pas

#### ✅ Validation :
Loguer côté serveur le message chiffré qui transite. Montrer qu'il est **illisible**.

---

### 💬 Étape 3 : Chiffrement des Messages avec la Clé de Session

#### Processus :
- Tous les messages entre **Alice** et **Bob** sont chiffrés **en symétrique** avec cette clé de session
- Réutiliser le code du Jour 2 Partie 2
- Le serveur ne fait que relayer des **blobs opaques**

#### ✅ Validation :
Les logs serveur ne contiennent que du **chiffré**.

---

### ✍️ Étape 4 : Signature des Messages

#### Processus :
1. Chaque message est signé avec la **clé privée** de l'expéditeur
2. Le destinataire **vérifie** la signature avec la **clé publique** de l'expéditeur
3. Si vérification échoue → **rejeter le message** et avertir le client

#### 🔧 Altération Manuelle :
Tester en modifiant manuellement un octet dans un message en transit (via un petit proxy).

#### ✅ Validation :
Le destinataire rejette le message altéré.

---

# 🎓 Compétences Visées

- 🚀 **Prompt engineering**
- 🔐 **Cryptographie**
- 🌐 **Réseau**

---

# 📚 Base de Connaissances

### Outils & Ressources

- 🔨 **hashcat** — Le programme pour casser les hash
- 📖 **Crypto 101** — Cours essentiel sur les primitives cryptographiques
- 🔒 **How Secure Is My Password?** — Pour tester l'entropie
- 🎮 **The Password Game** — Pour des idées de règles de mots de passe
- 📋 **ANSSI Guidelines** — Règles officielles de mots de passe
- 📊 **xkcd sur l'entropie** — Compréhension de l'entropie des mots de passe
- 🛡️ **Première collision SHA-1** — Histoire de la crypto
- ✅ **Bonnes Pratiques Crypto par Latacora** — Réflexes essentiels
- 🤖 **System Prompt "Study Mode" ChatGPT** — À copier dans une conversation

---

# 🎯 Rendu

Votre travail sera évalué en soutenance avec :
- 📊 Un support
- 👀 Une revue de code

---

**Bon courage! 🚀**
