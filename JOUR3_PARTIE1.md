# 📌 JOUR3_PARTIE1.md - Hacker NSA (Crypto Asymétrique)

## 🎯 Objectif

Implémenter la **cryptographie asymétrique** (RSA) pour éliminer le besoin d'échanger les clés symétriques via un canal non-sécurisé.

---

## 📝 Contexte

**Problem avec Day 2:**
- Les utilisateurs ont besoin de partager une clé symétrique
- Mais ils ne se sont jamais rencontrés avant!
- Comment établir le secret sans qu'un espion ne l'intercepte?

**Solution: Cryptographie Asymétrique**
- Chaque user a une **paire de clés**: publique + privée
- Clé publique peut être partagée avec tout le monde
- Clé privée reste secrète
- Chiffrer avec public key = seul owner de private key peut déchiffrer

**Workflow:**
1. Alice génère clé publique/privée et l'envoie au serveur
2. Serveur distribue les clés publiques aux autres clients
3. Quand Alice veut parler à Bob:
   - Alice génère une clé de session symétrique
   - Alice chiffre la clé de session avec la clé publique de Bob
   - Alice envoie le tout chiffré à Bob
   - Bob déchiffre avec sa clé privée
   - Maintenant Alice et Bob ont un secret partagé (clé de session)
   - Ils peuvent communiquer en symétrique

---

## 📋 Fonctionnalités à Implémenter

### 🔑 Part 1: Génération de Paire RSA

```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Générer la paire
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# Sérialiser en PEM pour stockage
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
```

### 📁 Stockage des Clés

**Côté Client:**
```
~/.crypto-vibeness/alice/
├── alice.pub   # Clé publique (PEM)
└── alice.priv  # Clé privée (PEM)
```

**Côté Serveur:**
- Plus de fichier `user_keys_do_not_steal_plz.txt` (les clés symmétriques n'existent plus!)
- Annuaire en mémoire: `{username: public_key_pem}`

### 📚 Annuaire des Clés Publiques

Maintenu sur le serveur et distribué aux clients:

```json
{
  "public_keys": {
    "alice": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgk...",
    "bob": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBg..."
  }
}
```

#### Distribution aux Clients
Quand un client se connecte:
1. Il envoie sa clé publique au serveur
2. Serveur la stocke dans l'annuaire
3. Serveur distribue tout l'annuaire à **TOUS** les clients
4. Chaque client stocke localement les clés publiques des autres

### 🔐 Key Encapsulation (Échange de Clé de Session)

**Quand Alice veut parler à Bob:**

1. **Alice génère une clé de session**
   ```python
   session_key = os.urandom(32)  # 256 bits
   ```

2. **Alice chiffre la session_key avec la clé publique de Bob**
   ```python
   from cryptography.hazmat.primitives.asymmetric import padding
   
   bob_public_key = load_public_key(...)  # Load from annuaire
   encrypted_session_key = bob_public_key.encrypt(
       session_key,
       padding.OAEP(
           mgf=padding.MGF1(algorithm=hashes.SHA256()),
           algorithm=hashes.SHA256(),
           label=None
       )
   )
   ```

3. **Alice envoie au serveur**
   ```json
   {
     "type": "key_exchange",
     "from": "alice",
     "to": "bob",
     "encrypted_session_key": "base64(encrypted_session_key)"
   }
   ```

4. **Serveur relaye à Bob**

5. **Bob reçoit et déchiffre avec sa clé privée**
   ```python
   bob_private_key = load_private_key(...)  # Load locally
   session_key = bob_private_key.decrypt(
       encrypted_session_key,
       padding.OAEP(
           mgf=padding.MGF1(algorithm=hashes.SHA256()),
           algorithm=hashes.SHA256(),
           label=None
       )
   )
   ```

6. **Maintenant Alice et Bob ont le même session_key!**
   - Utilisé pour AES-256-CBC (comme Day 2)
   - Serveur ne peut pas déchiffrer (n'a pas la clé privée de Bob)

### 🛠️ Utilitaires à Créer/Modifier

#### src/utils/asymmetric_crypto.py (NEW)
```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import os
import base64

class RSACrypto:
    @staticmethod
    def generate_keypair(key_size=2048):
        """Generate RSA keypair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    @staticmethod
    def private_to_pem(private_key):
        """Convert to PEM format"""
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    
    @staticmethod
    def public_to_pem(public_key):
        """Convert to PEM format"""
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    @staticmethod
    def pem_to_public_key(pem_bytes):
        """Load public key from PEM"""
        return serialization.load_pem_public_key(pem_bytes)
    
    @staticmethod
    def pem_to_private_key(pem_bytes):
        """Load private key from PEM"""
        return serialization.load_pem_private_key(pem_bytes, password=None)
    
    @staticmethod
    def encrypt_session_key(public_key, session_key):
        """Encrypt session key with public key (key encapsulation)"""
        ciphertext = public_key.encrypt(
            session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(ciphertext).decode()
    
    @staticmethod
    def decrypt_session_key(private_key, encrypted_session_key_b64):
        """Decrypt session key with private key"""
        encrypted_session_key = base64.b64decode(encrypted_session_key_b64)
        session_key = private_key.decrypt(
            encrypted_session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return session_key
```

### 🔄 Modifications à Faire

#### src/server.py
- À la connexion: recevoir et stocker la clé publique du client
- Distribuer l'annuaire des clés publiques à tous les clients
- Relayer les messages `key_exchange` chiffrés

#### src/client.py
- Générer la paire RSA au premier lancement
- Charger ou générer au lancement
- Recevoir et stocker l'annuaire des clés publiques
- Implémenter le handshake de key exchange

---

## 📂 Fichiers à Créer/Modifier

```
src/
├── utils/
│   └── asymmetric_crypto.py  (NEW)
└── (modifications à server.py, client.py)

~/.crypto-vibeness/
└── alice/
    ├── alice.pub   (NEW - clé publique)
    └── alice.priv  (NEW - clé privée)

data/
└── (plus de user_keys_do_not_steal_plz.txt - pas besoin!)
```

---

## ✅ Checklist de Validation

### Génération de Paire
- [ ] RSA 2048 bits générée au premier lancement
- [ ] Clés stockées en PEM
- [ ] Clés persistées (réutilisées au redémarrage)
- [ ] Clés jamais loggées

### Annuaire de Clés Publiques
- [ ] Serveur maintient un annuaire en mémoire
- [ ] Distribué à tous les clients à la connexion
- [ ] Clés mises à jour quand nouveaux clients se connectent
- [ ] Format JSON correct

### Key Exchange
- [ ] Alice génère session_key (256 bits)
- [ ] Alice chiffre avec clé publique de Bob
- [ ] Bob déchiffre avec sa clé privée
- [ ] Alice et Bob ont le même session_key
- [ ] Serveur ne peut pas décrypter (pas la clé privée de Bob)

### Chiffrement des Messages
- [ ] Réutilise l'AES-256-CBC de Day 2
- [ ] Session_key utilisée au lieu d'une clé dérivée
- [ ] Tous les messages 1-1 chiffrés

### Stockage de Clé
- [ ] Fichier `user_keys_do_not_steal_plz.txt` SUPPRIMÉ
- [ ] Clés privées stockées côté client uniquement
- [ ] Clés publiques distribuées via serveur

### Sécurité
- [ ] Clés privées jamais transmises
- [ ] Clés privées jamais loggées
- [ ] RSA OAEP avec SHA256
- [ ] Key encapsulation robuste

---

## 🧪 Test Manuel

```bash
# 1. Démarrer le serveur
python src/server.py
# [Server] Public key registry initialized

# 2. Alice se connecte
python src/client.py  # Terminal 2
# > Choose username: alice
# > Enter password: SecureP@ss123!
# > [Generated RSA 2048 keypair]
# > [Stored at ~/.crypto-vibeness/alice/]
# > [Sent public key to server]
# > [Received 1 public keys from server]

# Vérifier le fichier
cat ~/.crypto-vibeness/alice/alice.pub
# -----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBIjANBg...

# 3. Bob se connecte
python src/client.py  # Terminal 3
# > Choose username: bob
# > Enter password: BobSecure456!@
# > [Generated RSA 2048 keypair]
# > [Received 2 public keys from server]

# 4. Alice affiche la clé publique de Bob
alice> /public_key bob
# -----BEGIN PUBLIC KEY-----
# MIIBIjANBgk...

# 5. Alice envoie un message privé à Bob
alice> /msg bob Hello Bob!
# Client Alice:
# - Génère session_key
# - Chiffre session_key avec clé publique de Bob
# - Chiffre "Hello Bob!" avec AES et session_key
# - Envoie au serveur

# 6. Vérifier dans les logs que c'est chiffré
cat data/logs/log_*.txt | grep "alice" | grep "bob"
# [10:24:00] [KEY_EXCHANGE] alice -> bob: [ENCRYPTED_SESSION_KEY]
# [10:24:05] [MESSAGE] alice -> bob: [ENCRYPTED_MESSAGE]

# 7. Bob reçoit et déchiffre
bob> 
# [alice] Hello Bob!

# Success!
```

---

## 💡 Astuces

1. **Installation**: `pip install cryptography`
2. **RSA key size**: 2048 bits est standard. 4096 plus sécurisé mais plus lent.
3. **OAEP padding**: Plus sécurisé que PKCS1v15 (c'est celui par défaut maintenant)
4. **Session keys**: Générer une nouvelle pour chaque conversation Alice-Bob
5. **Persistent keys**: Charger les clés au lancement, pas générer à chaque fois

---

## 🎓 Concepts à Valider

- ✅ Cryptographie asymétrique (RSA)
- ✅ Key encapsulation
- ✅ Hybride crypto (asymétrique + symétrique)
- ✅ Annuaire de clés publiques
- ✅ Distribution sécurisée de clés

---

## ⚠️ Attention aux Pièges

- ❌ Ne **JAMAIS** transmettre les clés privées
- ❌ Ne **JAMAIS** logguer les clés privées
- ❌ Ne **JAMAIS** stocker les clés privées côté serveur
- ❌ Ne **JAMAIS** réutiliser la même session_key pour 2 messages
- ❌ Ne **JAMAIS** oublier le padding OAEP

---

## 🚀 Prochaine Étape

Une fois cette étape ✅ **VALIDÉE**, tu passeras à **JOUR3_PARTIE2** qui ajoutera:
- Signatures numériques (pour authentifier les messages)
- Vérification d'intégrité
- E2EE complet et sécurisé

---

Étape: **JOUR 3 - PARTIE 1**  
Durée estimée: 2-3h  
Complexité: ⭐⭐⭐⭐⭐ (très difficile)
