# 📌 JOUR1_PARTIE1.md - YOLO (Chat IRC Basique)

## 🎯 Objectif

Créer un **système de chat multi-utilisateurs type IRC** sans authentification ni chiffrement. C'est le point de départ du projet.

---

## 📝 Contexte

Tu viens de lire `AGENT.md`, `CONFIG.md` et `ORCHESTRATION.md`. Tu as compris que ce projet va progresser en 6 étapes. Cette étape est la **plus simple** — juste faire marcher un chat de base.

**Aucun utilisateur n'est véritablement sécurisé à ce stade.** C'est complètement YOLO (You Only Live Once) — d'où le nom de cette partie!

---

## 📋 Fonctionnalités à Implémenter

### 🖥️ Serveur (src/server.py)

#### Configuration
- Écoute sur un **port par défaut** (5555) ou un port passé en paramètre
- Configuration stockée dans `src/config/config.json`
- Peut gérer **plusieurs clients simultanément** (threading ou asyncio)
- Timeout de 30 secondes par défaut

#### Gestion des Clients
- Chaque client choisit un **username** à la connexion
- Le serveur **garantit l'unicité** du username (pas 2 users avec le même nom en même temps)
- Si un username est déjà pris, demander à l'utilisateur d'en choisir un autre

#### Système de Rooms
- Les utilisateurs sont placés dans une room **"general"** par défaut
- Possibilité de **créer des rooms** (commande `/create room_name`)
- Possibilité de **rejoindre des rooms** (commande `/join room_name`)
- Certaines rooms peuvent être **protégées par mot de passe** (optionnel à ce stade, mais déjà préparé)
  - Format: `/create room_name password123`
  - Affichage différent dans la console (avec 🔒 ou `[PROTECTED]`)

#### Messages
- Chaque message envoyé reçoit un **timestamp** au serveur
- Format: `[HH:MM:SS] alice: Hello everyone!`
- Les messages ne sont vus que par les utilisateurs dans la **même room**
- Broadcast des messages à tous les clients de la room

#### Couleurs
- Chaque client reçoit une **couleur déterministe**
  - Couleur = `hash(username) % len(COLORS)` (voir CONFIG.md)
  - La couleur est **toujours la même** pour le même username
  - Affichée de façon identique chez tous les clients
- Utiliser les codes ANSI pour les couleurs en console

#### Logs
- Le serveur **produit des logs** pour chaque événement:
  - Connexion d'un client
  - Déconnexion d'un client
  - Création de room
  - Changement de room
  - Envoi de message
- Format du fichier de log: `data/logs/log_2026-04-14_10-23-45.txt`
- Format des entrées: `[HH:MM:SS] [EVENT_TYPE] [USERNAME] [DETAILS]`

### 👤 Client (src/client.py)

#### Connexion
- Demander le **hostname** du serveur (ou `localhost` par défaut)
- Demander le **port** (ou 5555 par défaut)
- Se connecter au serveur via socket
- Demander un **username** (validation simple: min 3 caractères, alphanumérique)

#### Interface
- **Boucle principale** : affichage + input utilisateur
- Deux threads:
  - Thread de réception (écoute les messages du serveur)
  - Thread d'envoi (lit les commandes de l'utilisateur)
- Affichage des messages avec couleur de l'expéditeur

#### Commandes
```
/help                  # Affiche l'aide
/rooms                 # Liste toutes les rooms
/join <room_name>      # Rejoindre une room
/create <room_name>    # Créer une room
/users                 # Lister les users connectés
/quit                  # Quitter le chat
```

#### Messages
- Tout ce qui n'est pas une commande (n'a pas `/`) est un message
- Envoyé à tous les utilisateurs de la room actuelle
- Affichage: `[COLOR]username[RESET]: message text`

### 🛠️ Utilitaires (src/utils/)

#### logger.py
- Classe `Logger` pour gérer les logs du serveur
- Créer un fichier log avec timestamp
- Méthode `log(event_type, username, details)` pour logger les événements
- Rotation des logs (un nouveau fichier par session)

#### Optionnel: room_manager.py
- Classe `Room` pour représenter une room
- Classe `RoomManager` pour gérer les rooms
- Méthodes: `create_room()`, `join_room()`, `leave_room()`, `broadcast_to_room()`

---

## 🏗️ Architecture Recommandée

### Serveur (Multi-threaded)
```
ServerSocket (écoute sur 5555)
    ├── Thread 1: ClientHandler (alice)
    │   ├── Reçoit: "Hello"
    │   └── Envoie à: [bob, charlie] (s'ils sont dans la même room)
    ├── Thread 2: ClientHandler (bob)
    │   └── ...
    └── Thread 3: ClientHandler (charlie)
        └── ...

RoomManager
├── Room: "general"
│   └── clients: [alice, bob, charlie]
└── Room: "private"
    └── clients: [bob, charlie]
```

### Client (Multi-threaded)
```
ClientSocket (connecté au 5555)
├── Thread 1: ReceiveThread
│   └── Écoute les messages du serveur
│       └── Affiche avec couleur
└── Thread 2: SendThread
    └── Lit l'input utilisateur
        └── Envoie au serveur
```

---

## 📦 Fichiers à Créer

```
src/
├── server.py                 # Serveur principal
├── client.py                 # Client principal
└── utils/
    ├── __init__.py
    ├── logger.py             # Système de logging
    └── config.py             # (optionnel) Lecture de config

src/config/
└── config.json              # Configuration serveur

data/
└── logs/                    # Dossier pour les logs
    └── (créé automatiquement)
```

---

## 🔐 Format des Messages (JSON)

Les messages seront en JSON pour faciliter le parsing:

```json
{
  "type": "message",
  "from": "alice",
  "room": "general",
  "content": "Hello everyone!",
  "timestamp": "2026-04-14T10:23:45.123456",
  "color": "\033[91m"
}
```

Les commandes serveur/client:
```json
{
  "type": "command",
  "command": "join",
  "args": ["general"]
}
```

---

## ✅ Checklist de Validation

Avant de dire "C'est bon!", vérifier:

### Fonctionnalités de Base
- [ ] Serveur démarre et écoute sur le port
- [ ] Client peut se connecter
- [ ] Client choisit un username
- [ ] Usernames uniques (pas 2 "alice" en même temps)
- [ ] Messages affichés dans la console

### Rooms
- [ ] Room "general" existe par défaut
- [ ] `/join general` fonctionne
- [ ] `/create newroom` fonctionne
- [ ] `/rooms` liste les rooms
- [ ] Messages ne vont que dans la bonne room

### Couleurs
- [ ] Alice a toujours la même couleur
- [ ] Bob a une couleur différente d'Alice
- [ ] Les couleurs sont correctes dans tous les clients

### Users
- [ ] `/users` affiche les users connectés
- [ ] Le compte à jour quand quelqu'un se connecte/déconnecte

### Rooms Protégées
- [ ] `/create secretroom password123` crée une room protégée
- [ ] La room protégée s'affiche avec 🔒 ou `[PROTECTED]`
- [ ] Essayer de rejoindre sans password: refusé
- [ ] Rejoindre avec le bon password: accepté

### Logs
- [ ] Fichier créé dans `data/logs/log_*.txt`
- [ ] Chaque événement est loggé
- [ ] Timestamps corrects

### Performances
- [ ] Au moins 3 clients peuvent communiquer
- [ ] Pas de freeze ou lag
- [ ] Déconnexion propre avec `/quit`

### Code Quality
- [ ] Code en anglais (variables, fonction, etc.)
- [ ] Commentaires clairs
- [ ] Pas d'hardcoding (utiliser la config)
- [ ] Gestion d'erreurs basique

---

## 🧪 Test Manuel Complet

```bash
# 1. Démarrer le serveur
python src/server.py
# Attendu: "Server listening on localhost:5555"

# 2. Ouvrir 3 terminaux pour 3 clients
python src/client.py  # Terminal 2
# > Connected to localhost:5555
# > Choose username: alice
# > Welcome to Crypto Vibeness!

python src/client.py  # Terminal 3
# > Connected to localhost:5555
# > Choose username: bob
# > Welcome to Crypto Vibeness!

python src/client.py  # Terminal 4
# > Connected to localhost:5555
# > Choose username: charlie
# > Welcome to Crypto Vibeness!

# 3. Tester les commandes
# Client Alice:
alice> /users
# Affiche: alice, bob, charlie

alice> /rooms
# Affiche: general (*)

alice> /create private_chat
# Créé la room

alice> /join private_chat
# Alice change de room

alice> Hello from private room!
# Le message n'est VU QUE par les users dans private_chat
# Bob et Charlie ne le voient PAS

# Client Bob:
bob> /rooms
# Affiche: general (*), private_chat

bob> Hello from general!
# Alice ne voit pas ce message (elle est dans private_chat)

bob> /join private_chat
# Bob rejoint Alice

bob> Hi Alice!
# Alice voit le message avec la couleur de Bob

alice> Welcome Bob!
# Bob voit le message avec la couleur d'Alice

# 4. Tester les rooms protégées
charlie> /create secret mypassword
# Créé une room protégée

charlie> /rooms
# Affiche: general, private_chat, secret [PROTECTED]

alice> /join secret
# Erreur: "Room is password protected"

alice> /join secret mypassword
# Erreur: "Wrong password"

alice> /join secret mypassword123
# Erreur: "Wrong password"

charlie> (affiche le bon password quelque part)

alice> /join secret mypassword
# Succès: Alice rejoint la room secrète

# 5. Vérifier les logs
# Terminal 1 (serveur): affiche chaque action
# Fichier: data/logs/log_2026-04-14_10-23-45.txt contient:
# [10:23:45] [CONNECT] alice
# [10:23:50] [CONNECT] bob
# [10:24:00] [CREATE_ROOM] charlie secret
# ...

# 6. Graceful shutdown
charlie> /quit
# Client se ferme proprement
# Serveur affiche: "[10:24:30] [DISCONNECT] charlie"
```

---

## 💡 Conseils d'Implémentation

1. **Sockets**: Utiliser Python `socket` standard, pas de librairie externe
2. **Threading**: Utiliser `threading.Thread` pour multi-clients
3. **JSON**: `json.dumps()` / `json.loads()` pour messages
4. **Couleurs ANSI**: Codes standards (voir CONFIG.md)
5. **Gestion d'erreurs**: Try/except pour connexion réseau
6. **Config**: Charger depuis `config.json` au démarrage

---

## 🎓 Concepts à Valider

- ✅ Socket TCP en Python
- ✅ Multi-threading
- ✅ Architecture client/serveur
- ✅ Parsing de commandes
- ✅ Gestion d'état (rooms, users)
- ✅ Logging et timestamps

---

## 🚀 Prochaine Étape

Une fois cette étape ✅ **VALIDÉE** complètement, tu passeras à **JOUR1_PARTIE2** qui ajoutera:
- Authentification par mot de passe
- Hashing en MD5
- Vérification de règles de mot de passe
- Calcul d'entropie

---

## 📞 En cas de Doute

- Relis le CONFIG.md pour les détails de config
- Relis l'ORCHESTRATION.md pour le plan global
- Demande des clarifications sur les critères de validation

---

**C'est parti! 🚀 Bonne chance!**

Étape: **JOUR 1 - PARTIE 1**  
Durée estimée: 1-2h  
Complexité: ⭐ (très facile)
