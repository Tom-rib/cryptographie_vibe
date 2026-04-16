# 📌 JOUR3_PARTIE2.md - E2EE Complet (Signatures Numériques)

## 🎯 Objectif

Implémenter **End-to-End Encryption complet** avec **signatures numériques** pour:
- Assurer l'authenticité des messages (c'est bien Alice qui envoie?)
- Assurer l'intégrité (le message n'a pas été modifié?)
- Le serveur ne peut lire NI modifier les messages (honnête mais curieux)

---

## 📝 Contexte

Avec Day 3 Part 1, on a du chiffrement asymétrique. Mais il y a encore 2 problèmes:

1. **Authentification**: Comment être sûr qu'un message de "alice" vient réellement d'Alice?
   - Un attaquant pourrait se faire passer pour Alice auprès de Bob
   
2. **Intégrité**: Comment être sûr que Bob reçoit exactement ce qu'Alice a envoyé?
   - Un attaquant pourrait modifier un byte du message chiffré
   - Bob le déchiffre mais ne sait pas qu'il a été modifié

**Solution: Signatures Numériques**
- Alice **signe** le message avec sa **clé privée**
- Bob **vérifie** la signature avec la **clé publique d'Alice**
- Si la vérification échoue = message modifié ou faux sender = rejeter!

---

## 📋 Fonctionnalités à Implémenter

### ✍️ Part 1: Signature des Messages

#### Processus

**Alice envoie à Bob:**

1. Alice crée le message: `"Hello Bob!"`
2. Alice signe avec sa clé privée:
   ```python
   signature = alice_private_key.sign(
       message.encode(),
       padding.PSS(
           mgf=padding.MGF1(hashes.SHA256()),
           salt_length=padding.PSS.MAX_LENGTH
       ),
       hashes.SHA256()
   )
   ```
3. Alice envoie: `{message, signature}`

**Bob reçoit:**

1. Bob reçoit `{message, signature}`
2. Bob vérifie la signature avec la clé publique d'Alice:
   ```python
   alice_public_key.verify(
       signature,
       message.encode(),
       padding.PSS(
           mgf=padding.MGF1(hashes.SHA256()),
           salt_length=padding.PSS.MAX_LENGTH
       ),
       hashes.SHA256()
   )
   # Si ça lève une exception = signature invalide
   ```
3. Si vérification réussie = message authentique
4. Si vérification échoue = rejeter le message et avertir l'utilisateur

### 🔐 Part 2: Format des Messages E2EE

```json
{
  "type": "message_e2ee",
  "from": "alice",
  "to": "bob",
  "timestamp": "2026-04-14T10:24:00.123456",
  
  "encrypted_content": "base64(AES_encrypt(message))",
  "iv": "base64(iv)",
  
  "signature": "base64(sign_with_alice_private_key)",
  
  "color": "\033[91m"
}
```

### 🛠️ Utilitaires à Modifier/Créer

#### src/utils/asymmetric_crypto.py (MODIFY)
```python
class RSACrypto:
    # ... previous methods ...
    
    @staticmethod
    def sign_message(private_key, message):
        """Sign message with private key"""
        signature = private_key.sign(
            message.encode() if isinstance(message, str) else message,
            padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode()
    
    @staticmethod
    def verify_signature(public_key, message, signature_b64):
        """Verify message signature with public key"""
        try:
            signature = base64.b64decode(signature_b64)
            public_key.verify(
                signature,
                message.encode() if isinstance(message, str) else message,
                padding.PSS(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
```

#### src/utils/e2ee.py (NEW)
```python
class E2EEProtocol:
    """End-to-End Encryption Protocol"""
    
    def __init__(self, private_key, public_key, crypto_utils, aes_cipher):
        self.private_key = private_key
        self.public_key = public_key
        self.crypto = crypto_utils
        self.cipher = aes_cipher
    
    def prepare_message(self, recipient_public_key_pem, message, recipient_username):
        """Prepare a message for E2EE transmission"""
        
        # 1. Generate session key
        session_key = os.urandom(32)
        
        # 2. Encrypt message with session key (AES-CBC)
        encrypted_msg = self.cipher.encrypt(message)
        
        # 3. Encapsulate session key (encrypt with recipient's public key)
        recipient_public_key = self.crypto.pem_to_public_key(
            recipient_public_key_pem.encode()
        )
        encrypted_session_key = self.crypto.encrypt_session_key(
            recipient_public_key,
            session_key
        )
        
        # 4. Sign the encrypted message
        signature = self.crypto.sign_message(
            self.private_key,
            encrypted_msg['ciphertext']
        )
        
        return {
            'encrypted_content': encrypted_msg['ciphertext'],
            'iv': encrypted_msg['iv'],
            'encrypted_session_key': encrypted_session_key,
            'signature': signature
        }
    
    def receive_message(self, message_data, sender_public_key_pem):
        """Receive and verify an E2EE message"""
        
        # 1. Verify signature
        sender_public_key = self.crypto.pem_to_public_key(
            sender_public_key_pem.encode()
        )
        
        if not self.crypto.verify_signature(
            sender_public_key,
            message_data['encrypted_content'],
            message_data['signature']
        ):
            return None, "Signature verification failed!"
        
        # 2. Decrypt session key with our private key
        try:
            session_key = self.crypto.decrypt_session_key(
                self.private_key,
                message_data['encrypted_session_key']
            )
        except Exception as e:
            return None, f"Failed to decrypt session key: {e}"
        
        # 3. Decrypt message with session key
        try:
            plaintext = self.cipher.decrypt(
                message_data['encrypted_content'],
                message_data['iv'],
                session_key
            )
            return plaintext, None
        except Exception as e:
            return None, f"Failed to decrypt message: {e}"
```

### 🔄 Workflow Complet

**Alice → Bob:**

```
1. Alice: "Hello Bob!" → [SIGN] → signature
2. Alice: "Hello Bob!" → [AES encrypt with session_key] → ciphertext
3. Alice: session_key → [RSA encrypt with Bob's public key] → encrypted_session_key
4. Alice sends to Server: {
     encrypted_content,
     iv,
     encrypted_session_key,
     signature
   }
```

**Server:**
```
Logs the entire blob (all encrypted, can't read!)
Relays to Bob
```

**Bob ← Server:**

```
1. Bob receives: {
     encrypted_content,
     iv,
     encrypted_session_key,
     signature
   }
2. Bob: [VERIFY signature with Alice's public key]
   - If fails → REJECT message
3. Bob: [RSA decrypt with his private key] → session_key
4. Bob: [AES decrypt with session_key] → plaintext
5. Bob displays the message
```

### 📂 Fichiers à Modifier/Créer

#### Modifications
- `src/server.py` - Relayer messages E2EE, logs chiffrés
- `src/client.py` - Utiliser E2EE pour messages 1-1
- `src/utils/asymmetric_crypto.py` - Ajouter sign/verify

#### Créer
- `src/utils/e2ee.py` - Classe E2EEProtocol

---

## ✅ Checklist de Validation (4 Étapes)

### Étape 1: Distribution des Clés Publiques
- [ ] Client envoie sa clé publique au serveur
- [ ] Serveur maintient annuaire: `{username: public_key}`
- [ ] Annuaire distribué à tous les clients
- [ ] Clients stockent localement les clés publiques
- [ ] Un client peut afficher la clé publique d'un autre
- [ ] Serveur n'a pas accès aux clés privées

### Étape 2: Key Setup par Paire
- [ ] Alice génère une clé de session
- [ ] Alice chiffre avec clé publique de Bob (key encapsulation)
- [ ] Alice envoie au serveur (relayé à Bob)
- [ ] Bob déchiffre avec sa clé privée
- [ ] Alice et Bob ont le même secret (session_key)
- [ ] Serveur NE CONNAÎT PAS la session_key

### Étape 3: Chiffrement des Messages
- [ ] Messages 1-1 chiffrés en symétrique avec session_key
- [ ] Logs serveur contiennent du chiffré uniquement
- [ ] IV généré aléatoirement pour chaque message
- [ ] Clients peuvent déchiffrer les messages reçus
- [ ] Messa jamais stockés en clair

### Étape 4: Signature des Messages
- [ ] Chaque message signé avec clé privée de l'expéditeur
- [ ] Destinataire vérifie avec clé publique de l'expéditeur
- [ ] Signature invalide = message rejeté
- [ ] Client averti si signature échoue
- [ ] Modification d'un byte du chiffré = signature invalide

### Sécurité Globale
- [ ] Serveur ne peut pas lire les messages (chiffrés)
- [ ] Serveur ne peut pas modifier les messages (signatures)
- [ ] Serveur ne peut pas personnifier Alice (pas sa clé privée)
- [ ] Attaquant qui capture le trafic = blobs opaques

---

## 🧪 Test Manuel Complet

```bash
# 1. Démarrer le serveur
python src/server.py
# [Server] E2EE mode enabled

# 2. Alice se connecte
python src/client.py  # Terminal 2
# > Choose username: alice
# > Enter password: SecureP@ss123!
# > [Generated RSA keypair]
# > [Sent public key to server]

# 3. Bob se connecte
python src/client.py  # Terminal 3
# > Choose username: bob
# > Enter password: BobSecure456!@
# > [Generated RSA keypair]
# > [Received public key of alice]

# 4. Alice envoie un message privé à Bob
alice> /msg bob Hello Bob, this is confidential!
# Client Alice:
# - Génère session_key
# - Chiffre message avec session_key (AES)
# - Chiffre session_key avec clé publique de Bob (RSA)
# - Signe le chiffré avec sa clé privée
# - Envoie {encrypted_msg, iv, encrypted_session_key, signature}

# Vérifier les logs
cat data/logs/log_*.txt | tail -5
# [10:25:00] [E2EE_MESSAGE] alice -> bob: [ENCRYPTED_BLOB]
# (le message est COMPLÈTEMENT illisible!)

# 5. Bob reçoit et déchiffre
bob> 
# Alice: Hello Bob, this is confidential!
# [Message signature verified ✓]

# 6. Tester: intercepter et modifier un message

# D'un autre terminal, lire le message envoyé au serveur
# Par exemple dans les logs, trouver le ciphertext et modifier un byte

# Modifier le fichier temporaire du message (simulating an attacker)
# Ou utiliser un proxy pour modifier le message en transit

# Résultat: Bob reçoit
bob>
# [ERROR] Message signature verification failed!
# [WARNING] Possible tampering detected for message from alice

# 7. Tester une fausse signature
# Alice envoie un message
# Charlie (un attaquant) essaie d'envoyer avec le signature d'Alice
# (mais Charlie n'a pas la clé privée d'Alice)
# Résultat: Signature échoue

charlie> /msg bob I'm alice!
# Client Charlie signe avec sa propre clé
# Bob reçoit avec signature de Charlie (pas Alice)
# Signature échoue!
bob>
# [ERROR] Sender verification failed: expected alice but signature is from charlie

# 8. Final Test: Rooms publiques (sans E2EE)
# Les rooms publiques pourraient rester NON-chiffrées
# OU être chiffrées mais avec une clé partagée
# (Pour cette version, on ne chiffre que les messages 1-1)

# Room "general" (sans E2EE, optionnel)
alice> /join general
alice> Hello everyone!
bob> /join general
bob> Hi Alice!

# Ces messages sont chiffrés en SYMÉTRIQUE avec une clé de room
# (ou pas du tout, c'est du plaintext)
```

---

## 💡 Astuces

1. **Erreurs de signature**: Très strictes! Même un byte modifié = fail
2. **RSA PSS padding**: Meilleur pour la sécurité que PKCS1v15
3. **Session keys**: Une nouvelle pour chaque conversation Alice-Bob
4. **Logs du serveur**: Aucun plaintext ne doit apparaître
5. **Error handling**: Ne jamais révéler pourquoi une signature a échoué (information leak!)

---

## 🎓 Concepts Finaux Validés

- ✅ Cryptographie asymétrique complète
- ✅ Signatures numériques (authenticité)
- ✅ Key encapsulation (confidentialité)
- ✅ End-to-End Encryption
- ✅ Intégrité des messages
- ✅ Non-repudiation (Alice ne peut nier avoir envoyé)

---

## ⚠️ Attention aux Pièges

- ❌ Ne **JAMAIS** oublier de vérifier les signatures
- ❌ Ne **JAMAIS** accepter un message si signature échoue
- ❌ Ne **JAMAIS** révéler la raison spécifique de l'échec (timing attacks)
- ❌ Ne **JAMAIS** réutiliser les session keys
- ❌ Ne **JAMAIS** logguer les plaintext messages

---

## 🎉 Le Projet est COMPLET!

Une fois cette étape ✅ **VALIDÉE**, vous avez:

✅ Chat multi-utilisateurs sécurisé
✅ Authentification robuste
✅ Hashing modern (bcrypt)
✅ Chiffrement symétrique des messages
✅ Crypto asymétrique
✅ End-to-End Encryption
✅ Signatures numériques
✅ Serveur honnête-mais-curieux ne peut rien lire

**Vous maîtrisez maintenant les 3 branches de la cryptographie!**

---

## 📝 Checklist Finale du Projet

### Architecture
- [ ] Code en anglais, commentaires clairs
- [ ] Structure modulaire et réutilisable
- [ ] Configuration externalisée (JSON files)
- [ ] Gestion d'erreurs complète

### Sécurité
- [ ] Aucun plaintext password jamais stocké
- [ ] Mots de passe vérifiés en temps constant
- [ ] Clés privées jamais transmises
- [ ] Messages chiffrés de bout en bout
- [ ] Signatures vérifiées
- [ ] Logs du serveur sans plaintext

### Git
- [ ] Commits réguliers et descriptifs
- [ ] Historique complet du projet
- [ ] Tags pour chaque étape majeure

### Tests
- [ ] Chat multi-utilisateurs fonctionne
- [ ] Authentification fonctionne
- [ ] Hashing moderne fonctionne
- [ ] Chiffrement symétrique fonctionne
- [ ] Crypto asymétrique fonctionne
- [ ] E2EE complet fonctionne
- [ ] Signatures vérifiées

### Documentation
- [ ] Fichiers README
- [ ] Commentaires dans le code
- [ ] Architecture documentée
- [ ] Instructions de lancement

---

## 🚀 Soutenance

Être prêt à expliquer:
1. **L'architecture** du projet
2. **Les choix cryptographiques** (pourquoi bcrypt? pourquoi RSA?)
3. **Le workflow complet** (d'une connexion à un message chiffré)
4. **Les attaques évitées** (brute force, tampering, man-in-the-middle)
5. **Les limitations** (key management client-side, key recovery, etc.)

---

Étape: **JOUR 3 - PARTIE 2 (FINAL)**  
Durée estimée: 2-3h  
Complexité: ⭐⭐⭐⭐⭐ (très difficile)

**Bravo! Vous avez complété Crypto Vibeness! 🎉**
