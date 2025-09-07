# 🛠️ Résolution de Problèmes

Guide de dépannage pour résoudre les problèmes les plus courants de l'application Dépenses Couple.

## 🚨 Problèmes d'Installation

### ❌ "Python n'est pas reconnu comme une commande"

**Cause :** Python n'est pas installé ou pas dans le PATH

**Solutions :**
```bash
# Vérifier l'installation Python
python --version
python3 --version

# Si aucune ne fonctionne, installer Python :
# Windows : https://python.org/downloads
# Mac : brew install python3
# Ubuntu : sudo apt install python3 python3-pip
```

### ❌ "pip : commande introuvable"

**Solutions :**
```bash
# Essayer python -m pip
python -m pip install -r requirements.txt

# Ou python3
python3 -m pip install -r requirements.txt

# Installation pip si manquant
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### ❌ "Permission denied" lors de l'installation

**Solutions :**
```bash
# Utiliser --user pour installation locale
pip install -r requirements.txt --user

# Ou créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## 🔥 Problèmes de Démarrage

### ❌ "Address already in use - Port 5000"

**Cause :** Le port 5000 est déjà utilisé

**Solutions :**
```bash
# Option 1 : Tuer le processus sur le port 5000
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F

# Option 2 : Changer de port
# Modifier app.py ligne finale :
app.run(debug=True, host='0.0.0.0', port=5001)
```

### ❌ "ModuleNotFoundError: No module named 'flask'"

**Cause :** Dépendances non installées ou mauvais environnement Python

**Solutions :**
```bash
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall

# Vérifier l'environnement virtuel
which python  # Doit pointer vers votre venv si activé

# Installer manuellement les modules manquants
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5
```

### ❌ "sqlite3.OperationalError: database is locked"

**Cause :** Base de données utilisée par un autre processus

**Solutions :**
```bash
# Arrêter tous les processus Python
pkill python

# Supprimer le fichier de lock (si existant)
rm expenses.db-wal expenses.db-shm

# Redémarrer l'application
python app.py
```

---

## 💾 Problèmes de Base de Données

### ❌ "Table doesn't exist" ou erreurs SQL

**Solutions :**
```bash
# Supprimer la base corrompue et recréer
rm expenses.db
python app.py  # Se recréera automatiquement
```

**Récupération de données :**
```bash
# Sauvegarder avant suppression
cp expenses.db expenses.db.backup

# Si récupération nécessaire, restaurer
cp expenses.db.backup expenses.db
```

### ❌ Données manquantes après mise à jour

**Diagnostic :**
```bash
# Vérifier l'existence du fichier
ls -la expenses.db

# Vérifier le contenu
sqlite3 expenses.db
.tables
SELECT COUNT(*) FROM expense;
.quit
```

**Solutions :**
- Restaurer depuis sauvegarde si disponible
- Vérifier que vous êtes dans le bon dossier
- Recréer manuellement les données importantes

### ❌ Base de données corrompue

**Récupération :**
```bash
# Créer une nouvelle base propre
python -c "
from app import app, db
with app.app_context():
    db.create_all()
"

# Ou forcer la recréation complète
rm expenses.db
python app.py
```

---

## 🌐 Problèmes de Navigation

### ❌ "This site can't be reached"

**Vérifications :**
1. L'application est-elle démarrée ? (Vérifier la console)
2. L'URL est-elle correcte ? (`http://localhost:5000`)
3. Le port est-il correct ?

**Solutions :**
```bash
# Vérifier que l'app tourne
ps aux | grep python

# Tester l'accès direct
curl http://localhost:5000

# Essayer une autre URL
http://127.0.0.1:5000
http://0.0.0.0:5000
```

### ❌ Page blanche ou erreur 500

**Diagnostic :**
1. Vérifier la console Python pour les erreurs
2. Activer le mode debug si pas déjà fait
3. Vérifier les logs

**Solutions :**
```python
# Dans app.py, s'assurer que debug=True
app.run(debug=True, host='0.0.0.0', port=5000)
```

### ❌ CSS/JavaScript non chargés

**Cause :** Problème de chemins statiques

**Solutions :**
1. Vérifier que le dossier `static/` existe
2. Contrôler la structure des dossiers
3. Redémarrer l'application

---

## 📱 Problèmes d'Interface

### ❌ Interface déformée sur mobile

**Solutions :**
- Forcer le rafraîchissement : `Ctrl+F5`
- Vider le cache navigateur
- Tester sur un autre navigateur
- Vérifier la connexion internet

### ❌ Boutons qui ne répondent pas

**Diagnostic :**
1. Ouvrir les outils développeur (`F12`)
2. Vérifier la console pour les erreurs JavaScript
3. Tester le réseau dans l'onglet "Network"

**Solutions :**
- Désactiver les extensions navigateur temporairement
- Tester en navigation privée
- Redémarrer le navigateur

### ❌ Formulaires qui ne s'envoient pas

**Vérifications :**
1. Tous les champs obligatoires sont-ils remplis ?
2. Y a-t-il des erreurs dans la console ?
3. La connexion réseau est-elle stable ?

**Solutions :**
```javascript
// Tester dans la console du navigateur
fetch('/api/expenses', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({amount: 10, description: 'test'})
})
```

---

## 💰 Problèmes de Données

### ❌ Montants incorrects dans les calculs

**Vérifications :**
1. Format des montants (virgule vs point)
2. Abonnements actifs/inactifs
3. Dates des revenus et dépenses

**Solutions :**
- Vérifier les paramètres régionaux
- Recalculer manuellement pour validation
- Corriger les données aberrantes

### ❌ Catégories manquantes

**Solutions :**
```python
# Réinitialiser les catégories par défaut
python -c "
from app import app, db, Category
with app.app_context():
    # Ajouter les catégories manquantes
    categories = [
        ('Alimentation', '#28a745', 'fas fa-utensils'),
        ('Transport', '#007bff', 'fas fa-car'),
        # ... autres catégories
    ]
    for name, color, icon in categories:
        if not Category.query.filter_by(name=name).first():
            cat = Category(name=name, color=color, icon=icon)
            db.session.add(cat)
    db.session.commit()
"
```

### ❌ Graphiques qui ne s'affichent pas

**Causes possibles :**
- Pas assez de données (< 2 mois)
- Erreur JavaScript
- Problème de bibliothèque Chart.js

**Solutions :**
1. Ajouter plus de données
2. Vérifier la console pour erreurs JS
3. Redémarrer l'application

---

## 🔐 Problèmes de Sécurité

### ❌ "Your connection is not private"

**Cause :** Certificat SSL auto-signé ou manquant

**Solutions temporaires :**
- Cliquer "Advanced" puis "Proceed to localhost"
- Utiliser `http://` au lieu de `https://`
- Ajouter une exception dans le navigateur

### ❌ Session qui expire constamment

**Solutions :**
```python
# Dans app.py, augmenter la durée des sessions
from datetime import timedelta
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
```

---

## 🚀 Problèmes de Performance

### ❌ Application très lente

**Diagnostic :**
1. Taille de la base de données
2. Nombre d'enregistrements
3. Ressources système disponibles

**Solutions :**
```sql
-- Nettoyer les anciennes données
DELETE FROM expense WHERE date < date('now', '-2 years');

-- Réorganiser la base
VACUUM;
```

### ❌ Mémoire insuffisante

**Solutions :**
- Fermer d'autres applications
- Redémarrer l'ordinateur
- Migrer vers un serveur plus puissant si usage intensif

---

## 🔧 Outils de Diagnostic

### Script de Diagnostic Automatique

```python
# diagnostic.py
import os
import sqlite3
from flask import Flask

def diagnose():
    print("=== DIAGNOSTIC DÉPENSES COUPLE ===\n")
    
    # Vérifier Python
    import sys
    print(f"Python: {sys.version}")
    
    # Vérifier les modules
    try:
        import flask
        print(f"Flask: {flask.__version__}")
    except ImportError:
        print("❌ Flask non installé")
    
    # Vérifier la base de données
    if os.path.exists('expenses.db'):
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM expense")
        expenses = cursor.fetchone()[0]
        print(f"Dépenses en base: {expenses}")
        
        cursor.execute("SELECT COUNT(*) FROM category")
        categories = cursor.fetchone()[0]
        print(f"Catégories en base: {categories}")
        
        conn.close()
    else:
        print("❌ Base de données non trouvée")
    
    # Vérifier les fichiers
    required_files = ['app.py', 'requirements.txt', 'templates/', 'static/']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} manquant")

if __name__ == "__main__":
    diagnose()
```

### Commandes de Debug Utiles

```bash
# Logs détaillés
python app.py > debug.log 2>&1

# Vérifier les ports utilisés
netstat -tulpn | grep :5000

# Tester la connectivité
curl -v http://localhost:5000

# Vérifier l'espace disque
df -h

# Vérifier la mémoire
free -h
```

---

## 📞 Quand Demander de l'Aide

### Informations à Fournir

Lors d'une demande d'aide, incluez :

1. **Système d'exploitation** et version
2. **Version Python** (`python --version`)
3. **Message d'erreur complet** (copier-coller)
4. **Étapes pour reproduire** le problème
5. **Capture d'écran** si problème visuel
6. **Logs de l'application** si disponibles

### Template de Bug Report

```
🐛 Bug Report

**Environnement:**
- OS: [Windows 10 / macOS 12 / Ubuntu 20.04]
- Python: [3.9.7]
- Navigateur: [Chrome 98.0]

**Problème:**
[Description claire du problème]

**Étapes pour reproduire:**
1. [Première étape]
2. [Deuxième étape]
3. [Résultat observé]

**Résultat attendu:**
[Ce qui devrait se passer]

**Captures d'écran:**
[Si applicable]

**Logs d'erreur:**
```
[Copier-coller les erreurs]
```

**Informations supplémentaires:**
[Contexte utile]
```

---

## 🔄 Procédures de Récupération

### Sauvegarde Préventive

```bash
# Script de sauvegarde quotidienne
#!/bin/bash
DATE=$(date +%Y%m%d)
cp expenses.db "backup/expenses_$DATE.db"

# Garder seulement les 30 derniers jours
find backup/ -name "expenses_*.db" -mtime +30 -delete
```

### Récupération d'Urgence

```bash
# Procédure de récupération complète
cd depenses-couple
git pull origin main  # Dernière version
rm expenses.db        # Supprimer base corrompue
python app.py         # Recréer base vide

# Restaurer depuis sauvegarde si disponible
cp backup/expenses_YYYYMMDD.db expenses.db
python app.py
```

---

*En cas de problème persistant, n'hésitez pas à consulter la [FAQ](faq.md) ou [contacter le support](contact.md) ! 🆘*