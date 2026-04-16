# 🐧 Installation sur WSL (Windows Subsystem for Linux)

Si vous obtenez l'erreur `python3-venv not available`, ce guide vous aidera.

## ❌ Erreur courante

```
The virtual environment was not created successfully because ensurepip is not available.
On Debian/Ubuntu systems, you need to install the python3-venv package using the following command.
    apt install python3.12-venv
```

## ✅ Solution: Une commande pour tout installer

```bash
# Clone le repository
git clone https://github.com/Tom-rib/cryptographie_vibe.git
cd cryptographie_vibe

# Installation complète (automatique)
make setup
```

**C'est tout!** La commande `make setup` va:
1. ✅ Vérifier et installer `python3-venv` si nécessaire (avec `sudo`)
2. ✅ Créer le virtual environment
3. ✅ Installer toutes les dépendances Python

## 🔧 Alternative: Script setup.sh

Si vous préférez un script bash:

```bash
bash setup.sh
```

Le script va automatiquement installer `python3-venv` via apt-get.

## 📋 Options d'installation manuelles

Si `make setup` ne fonctionne pas, vous pouvez installer manuellement:

### ⚠️ Venv Corrompu?

Si vous voyez: `ModuleNotFoundError: No module named 'pip'`

**Solution rapide:**
```bash
make clean-venv    # Supprime le venv corrompu
make setup         # Crée un nouveau venv frais
```

### Étape 1: Installer python3-venv
```bash
# Sur Debian/Ubuntu
sudo apt-get update
sudo apt-get install -y python3-venv

# Sur Fedora
sudo dnf install -y python3-venv

# Sur Arch
sudo pacman -S python-venv
```

### Étape 2: Créer le virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Étape 3: Installer les dépendances
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## 🚀 Après l'installation

```bash
# Vérifier que tout fonctionne
make test

# Lancer le serveur (terminal 1)
make run

# Lancer un client (terminal 2)
python3 src/client.py

# Lancer un autre client (terminal 3)
python3 src/client.py
```

## ✨ Commandes utiles

```bash
make help           # Affiche tous les commandes disponibles
make setup          # Installation complète
make test           # Lancer tous les tests
make clean          # Nettoyer les fichiers temporaires
make clean-venv     # Supprimer le venv (pour réinitialiser)
make clean-all      # Nettoyer venv inclus
```

## 🐛 Troubleshooting

### Erreur: "ModuleNotFoundError: No module named 'pip'"

Le venv est corrompu. **Solution:**
```bash
make clean-venv     # Supprime le venv
make setup          # Crée un nouveau venv frais et installe tout
```

### Erreur: "Permission denied"
```bash
# Assurez-vous que setup.sh est exécutable
chmod +x setup.sh
bash setup.sh
```

### Erreur: "sudo password required"
Si vous êtes invité à entrer un mot de passe:
- La commande `make setup` va demander votre mot de passe pour installer `python3-venv`
- C'est normal et nécessaire

### Erreur: "make not found"
Installez make:
```bash
# Debian/Ubuntu
sudo apt-get install -y make

# Fedora
sudo dnf install -y make

# Arch
sudo pacman -S make
```

## 📚 Ressources

- **README.md** - Vue d'ensemble du projet
- **COMMANDS.md** - Référence des commandes de chat
- **docs/INDEX.md** - Guide de navigation pour développeurs
- **docs/Ressource_vibe/** - Tous les fichiers de développement

## 🎯 Résumé rapide

```bash
git clone https://github.com/Tom-rib/cryptographie_vibe.git
cd cryptographie_vibe
make setup    # Installation automatique complète
make test     # Vérifier que tout fonctionne
make run      # Lancer le serveur
```

Voilà! 🎉 Vous êtes prêt à utiliser Crypto Vibeness!
