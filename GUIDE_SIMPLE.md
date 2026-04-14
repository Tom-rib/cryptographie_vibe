# 🎯 GUIDE SIMPLE - Démarrage Rapide

## CE QUE TU DOIS FAIRE (4 étapes)

---

## ✅ ÉTAPE 1: TÉLÉCHARGER LES FICHIERS

**Garde SEULEMENT ces fichiers dans ton répertoire:**

```
crypto-vibeness/
├── crypto_vibeness.md          (sujet du projet)
├── PROMPT_COMPLET.md           (À DONNER À CLAUDE)
├── README.md                   (pour comprendre)
└── .gitignore                  (à créer)
```

**Crée un fichier `.gitignore`:**
```
__pycache__/
*.pyc
*.pyo
.env
data/logs/*
data/*.txt
!data/password_rules.json
~/.crypto-vibeness/
```

---

## ✅ ÉTAPE 2: LIRE D'ABORD (5 min)

Lis **README.md** en entier (c'est important!)

---

## ✅ ÉTAPE 3: INITIALISER LE PROJET

```bash
# Ouvre un terminal dans le répertoire
cd crypto-vibeness

# Initialise Git
git init
git config user.name "Your Name"
git config user.email "your@email.com"

# Crée la structure
mkdir -p src/utils src/config data/logs tests scripts

# Crée un commit initial
git add .
git commit -m "Initial commit: project setup"
```

---

## ✅ ÉTAPE 4: DONNER À CLAUDE

**Copie TOUT le contenu de `PROMPT_COMPLET.md`**

Envoie à Claude Haiku 4.5 avec ce message:

```
Je vais te donner un prompt complet pour créer un système
de chat sécurisé avec cryptographie. 

Lis entièrement le prompt, puis crée les fichiers Python
en suivant chaque étape strictement.

À chaque étape:
1. Crée les fichiers
2. Code la fonctionnalité
3. Teste manuellement
4. Valide TOUS les critères
5. Fais un commit Git
6. Me dis "Étape X ✅ VALIDÉE"

ATTENTION: Ne passe JAMAIS à l'étape suivante 
si l'étape actuelle n'est pas ✅ VALIDÉE!

Voici le prompt:
```

**Puis colle tout le contenu de PROMPT_COMPLET.md**

---

## 📁 FICHIERS QUE CLAUDE VA CRÉER

Claude créera automatiquement:

```
src/
├── server.py
├── client.py
└── utils/
    ├── logger.py
    ├── password_manager.py
    ├── entropy_calculator.py
    ├── bcrypt_hasher.py
    ├── key_derivation.py
    ├── crypto.py
    ├── asymmetric_crypto.py
    └── e2ee.py

src/config/
├── config.json
└── password_rules.json

data/
├── this_is_safe.txt
├── user_keys_do_not_steal_plz.txt
├── md5_decrypted.txt
└── logs/

scripts/
└── migrate_passwords.py

tests/
└── test_*.py
```

---

## 🎯 RÉSUMÉ EXACT

```
1. Lis README.md (5 min)
   ↓
2. Crée la structure (mkdir + git init)
   ↓
3. Copie PROMPT_COMPLET.md
   ↓
4. Envoie à Claude avec le message ci-dessus
   ↓
5. Claude crée tout (8-12 heures)
   ↓
✅ PROJET COMPLET!
```

---

## ⏸️ SI QUELQUE CHOSE ÉCHOUE

**Claude doit dire "Étape X ✅ VALIDÉE" avant de continuer!**

Si une étape n'est pas validée:
- Claude relit les critères
- Claude corrige
- Claude teste de nouveau
- Claude dit "Étape X ✅ VALIDÉE"

---

## 💡 POINTS CLÉS

✅ Garde SEULEMENT: crypto_vibeness.md, PROMPT_COMPLET.md, README.md  
✅ Claude créera tous les fichiers .py  
✅ Claude committe régulièrement  
✅ Claude valide chaque étape strictement  
✅ Pas de "je pense que c'est bon" - validation stricte!  

---

**C'est tout. Vraiment. C'est aussi simple que ça.**

**→ Lis README.md maintenant**
