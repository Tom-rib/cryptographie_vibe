# 📌 JOUR1_PARTIE2.md - Authentification & MD5

## 🎯 Objectif

Ajouter un **système d'authentification** complet avec:
- Création de compte à la première connexion
- Vérification de **3+ règles de mot de passe**
- Calcul de **force du mot de passe** (entropie)
- Hashing **MD5** avec **base64**
- Vérification en **temps constant**

---

## 📝 Contexte

Tu viens de terminer JOUR1_PARTIE1. Le chat fonctionne, mais n'importe qui peut se faire passer pour quelqu'un d'autre!

Un utilisateur malveillant peut juste entrer le username "alice" et accéder à tous ses messages. **Inacceptable.**

À partir de maintenant, chaque utilisateur doit s'authentifier avec un mot de passe avant d'accéder au chat.

---

## 📋 Fonctionnalités à Implémenter

### 🔐 Authentification (Serveur)

#### Workflow de Connexion

1. **Client envoie username**
   - Serveur cherche dans `this_is_safe.txt`
   - Si trouvé: demander le mot de passe
   - Si not found: demander de créer un compte

2. **Création de Compte (Première Connexion)**
   - Demander le mot de passe une première fois
   - Demander de confirmer le mot de passe
   - Vérifier les 3+ règles de mot de passe
   - Si invalide: afficher le message d'erreur spécifique et redemander
   - Si valide: calculer la force du mot de passe (voir ci-dessous)
   - Afficher la force: "Password strength: 78% (STRONG)"
   - Hasher en MD5 + base64
   - Sauvegarder dans `this_is_safe.txt`

3. **Authentification d'Un Utilisateur Existant**
   - Demander le mot de passe
   - Hasher en MD5 + base64
   - Comparer avec le hash stocké
   - Vérification en **temps constant** (important!)

#### Format du Fichier `this_is_safe.txt`

```
alice:mZjP8aT5xQ0=
bob:pK9mL2rS7vW=
charlie:xY7qR4tU2pL=
```

- Une ligne par utilisateur
- Format: `username:md5_hash_in_base64`
- Le hash est le résultat de: `base64.b64encode(hashlib.md5(password.encode()).digest())`

### 🛡️ Règles de Mot de Passe

Implémenter au minimum **3 règles** (optionnellement en lire depuis `data/password_rules.json`):

1. **Longueur minimale**: ≥ 8 caractères
2. **Majuscules**: Au moins 1 lettre majuscule
3. **Minuscules**: Au moins 1 lettre minuscule
4. **Chiffres**: Au moins 1 chiffre
5. **Caractères spéciaux**: Au moins 1 parmi `!@#$%^&*()-_=+[]{}|;:,.<>?`

### 📊 Calcul de Force du Mot de Passe (Entropie)

L'**entropie** mesure la "randomness" du mot de passe:

```
Entropie = log2(espace_possible^longueur)

Où espace_possible = taille_alphabet^nombre_caractères

Espace possible:
- Minuscules seules: 26 possibilités
- Minuscules + majuscules: 52 possibilités
- + chiffres: 62 possibilités
- + caractères spéciaux: 95 possibilités
```

**Exemple:**
- `password123!A` (13 chars, tous les types): ~77 bits d'entropie → VERY STRONG ✅
- `Password1` (9 chars, 3 types): ~52 bits d'entropie → STRONG ✅
- `password123` (11 chars, 2 types): ~45 bits d'entropie → MEDIUM ⚠️
- `password` (8 chars, 1 type): ~37 bits d'entropie → WEAK ❌

**Catégories:**
- < 40 bits: WEAK (❌ rejeter)
- 40-60 bits: MEDIUM (⚠️ accepter avec warning)
- 60-80 bits: STRONG (✅ accepter)
- > 80 bits: VERY STRONG (✅✅ accepter)

### 🔐 Hashing MD5

```python
import hashlib
import base64

password = "Secure123!"
md5_hash = hashlib.md5(password.encode()).digest()
base64_encoded = base64.b64encode(md5_hash).decode()
# Result: "vT5F9xQ0mP2=" (exemple)
```

**Important**: Utiliser `.digest()` (bytes) et pas `.hexdigest()` (hex string)!

### ⏱️ Vérification en Temps Constant

**ATTENTION**: Comparaison naïve:
```python
if stored_hash == provided_hash:  # ❌ MAUVAIS!
    # Si première char match, continue à comparer...
    # Si première char ne match pas, s'arrête immédiatement
    # Timing reveal info!
```

**CORRECT**: Utiliser `hmac.compare_digest()`:
```python
import hmac
if hmac.compare_digest(stored_hash, provided_hash):  # ✅ BON!
    # Compare tous les bytes, même durée quoi qu'il arrive
```

### 👤 Client (Modification)

#### Écran de Login
```
Connected to localhost:5555
Choose username: alice
[Server: Username exists, enter password]
Enter password: ••••••••••
Authentication successful! Welcome alice!

---or---

Choose username: newuser
[Server: New account, choose password]
Enter password: SecureP@ss123
[Server: Password strength: 82% (STRONG)]
Re-enter password: SecureP@ss123
Account created! Welcome newuser!
```

#### Après Authentification
- Le client n'a accès au chat que s'il est authentifié
- S'il envoie un mauvais mot de passe 3 fois: déconnexion
- Messages d'erreur clairs

### 🛠️ Utilitaires à Créer/Modifier

#### src/utils/password_manager.py (NEW)
```python
class PasswordManager:
    def __init__(self, rules_file="data/password_rules.json"):
        self.rules = load_rules(rules_file)  # Charger les règles
    
    def validate_password(self, password):
        """Valider un password selon les règles"""
        errors = []
        for rule in self.rules:
            if not check_rule(password, rule):
                errors.append(rule['description'])
        return len(errors) == 0, errors
    
    def hash_password(self, password):
        """Hasher le password en MD5 base64"""
        return base64.b64encode(
            hashlib.md5(password.encode()).digest()
        ).decode()
    
    def verify_password(self, password, stored_hash):
        """Vérifier le password en temps constant"""
        computed_hash = self.hash_password(password)
        return hmac.compare_digest(computed_hash, stored_hash)
```

#### src/utils/entropy_calculator.py (NEW)
```python
class EntropyCalculator:
    def calculate(self, password):
        """Calculer l'entropie d'un password"""
        alphabet_size = 0
        if has_lowercase(password): alphabet_size += 26
        if has_uppercase(password): alphabet_size += 26
        if has_digits(password): alphabet_size += 10
        if has_special(password): alphabet_size += 32
        
        entropy = math.log2(alphabet_size ** len(password))
        strength = self.get_strength(entropy)
        percentage = min(entropy / 100 * 100, 100)  # Cap at 100%
        return entropy, strength, percentage
    
    def get_strength(self, entropy):
        if entropy < 40: return "WEAK"
        elif entropy < 60: return "MEDIUM"
        elif entropy < 80: return "STRONG"
        else: return "VERY STRONG"
```

---

## 🏗️ Architecture

### Fichiers à Modifier
- `src/server.py` - Ajouter authentification avant chat access
- `src/client.py` - Ajouter écran de login

### Fichiers à Créer
- `src/utils/password_manager.py` - Gestion des mots de passe
- `src/utils/entropy_calculator.py` - Calcul d'entropie
- `data/this_is_safe.txt` - Base de données des mots de passe
- `data/password_rules.json` - Règles de mots de passe

---

## ✅ Checklist de Validation

### Création de Compte
- [ ] Nouveau user peut créer un compte
- [ ] Password demandé deux fois et confirmé
- [ ] Règles vérifiées correctement
- [ ] Force du password affichée (%)
- [ ] Password sauvegardé hashé en MD5 base64
- [ ] Compte accessible après création

### Authentification Existante
- [ ] User existant peut se logger
- [ ] Bon password: authentification réussie
- [ ] Mauvais password: refusé (3 tentatives max)
- [ ] Vérification en temps constant (utiliser `hmac.compare_digest`)

### Règles de Password
- [ ] 3+ règles implémentées
- [ ] Messages d'erreur clairs si rule non respectée
- [ ] Possibilité de modifier les règles via `password_rules.json`

### Entropie
- [ ] Calcul correct de l'entropie
- [ ] Affichage en % et en force (WEAK/MEDIUM/STRONG/VERY STRONG)
- [ ] Entrée en base64 encodée, pas hex

### Sécurité
- [ ] Fichier `this_is_safe.txt` existe
- [ ] Format correct: `username:hash_base64`
- [ ] Mots de passe jamais loggés ou affichés
- [ ] Vérification en temps constant

### Intégration
- [ ] Chat inaccessible avant authentification
- [ ] Clients non-authentifiés ne reçoivent pas les messages
- [ ] Authentification se fait AVANT room creation/access

---

## 🧪 Test Manuel Complet

```bash
# 1. Démarrer le serveur
python src/server.py

# 2. Premier client (nouveau user)
python src/client.py
# > Connected to localhost:5555
# > Choose username: alice
# > [Server: New account. Choose password]
# > Enter password: HelloWorld123!
# > [Server: Password strength: 85% (STRONG)]
# > Re-enter password: HelloWorld123!
# > Account created! Welcome alice!
# > [alice] > /rooms
# > general (*)

# 3. Deuxième client (new user with weak password)
python src/client.py
# > Choose username: bob
# > Enter password: bob123
# > [Server: Password too weak!
#   - At least 1 uppercase letter
#   - At least 1 special character
#   Strength: 42% (WEAK)]
# > Try again
# > Enter password: Bob@Secure123
# > [Server: Password strength: 78% (STRONG)]
# > Re-enter password: Bob@Secure123
# > Account created! Welcome bob!

# 4. Troisième client (new user, wrong confirmation)
python src/client.py
# > Choose username: charlie
# > Enter password: Charlie@2024!
# > Re-enter password: Charlie@2025!  # Wrong!
# > [Server: Passwords don't match! Try again]
# > Enter password: Charlie@2024!
# > Re-enter password: Charlie@2024!
# > Account created!

# 5. Alice se reconnecte (existing user)
python src/client.py
# > Choose username: alice
# > [Server: Username exists. Enter password]
# > Enter password: HelloWorld123!
# > Authentication successful! Welcome back alice!

# 6. Wrong password
python src/client.py
# > Choose username: alice
# > Enter password: wrong
# > [Server: Wrong password (attempt 1/3)]
# > Enter password: wrong2
# > [Server: Wrong password (attempt 2/3)]
# > Enter password: wrong3
# > [Server: Wrong password (attempt 3/3)]
# > [Connection closed]

# 7. Vérifier le fichier
cat data/this_is_safe.txt
# alice:vT5F9xQ0mP2=
# bob:aB3xL9pR6qT=
# charlie:xY2zM5vN1kS=
```

---

## 💡 Astuces

1. **Load rules dynamiquement**: Lire `password_rules.json` au démarrage
2. **Entropie**: Utiliser `math.log2()` pour le calcul
3. **Base64**: `base64.b64encode().decode()` pour string output
4. **Time constant**: Toujours utiliser `hmac.compare_digest()`
5. **Fichier password_rules.json**: Copier le format de CONFIG.md

---

## 🎓 Concepts à Valider

- ✅ Hashing (MD5)
- ✅ Encoding (Base64)
- ✅ Vérification temps constant (timing attacks)
- ✅ Entropie des mots de passe
- ✅ Gestion de fichiers
- ✅ Règles de validation customisables

---

## ⚠️ Attention aux Pièges

- ❌ Ne **JAMAIS** stocker les mots de passe en clair
- ❌ Ne **JAMAIS** utiliser `==` pour comparer les hashes (timing attack!)
- ❌ Ne **JAMAIS** afficher les mots de passe
- ❌ Ne **JAMAIS** utiliser `.hexdigest()` pour le encoding base64
- ❌ Ne **JAMAIS** hardcoder les règles (les lire du fichier)

---

## 🚀 Prochaine Étape

Une fois cette étape ✅ **VALIDÉE**, tu passeras à **JOUR2_PARTIE1** qui:
- Cassera les hash MD5 avec hashcat
- Remplacera MD5 par une meilleure fonction (bcrypt/argon2)
- Ajoutera un salt

---

Étape: **JOUR 1 - PARTIE 2**  
Durée estimée: 1-1.5h  
Complexité: ⭐⭐ (facile)
