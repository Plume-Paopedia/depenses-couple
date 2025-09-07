# 💰 Dépenses Couple - Gestionnaire de Finances Partagées

Une application web Flask moderne et intuitive pour gérer les finances d'un couple. Suivez vos dépenses, abonnements, budgets et revenus avec une interface élégante et des graphiques informatifs.

## ✨ Fonctionnalités

### 📊 Tableau de Bord
- Vue d'ensemble des finances du mois en cours
- Résumé des revenus, dépenses et abonnements
- Budget restant calculé automatiquement
- Dépenses récentes et abonnements à renouveler

### 💸 Gestion des Dépenses
- Ajout rapide de dépenses avec catégorisation
- Marquage des dépenses exceptionnelles
- Historique complet avec pagination
- Filtrage par catégorie

### 🔄 Abonnements
- Suivi des abonnements mensuels et annuels
- Alertes pour les renouvellements à venir
- Gestion de l'état actif/inactif
- Calcul automatique de l'impact sur le budget

### 🎯 Budgets
- Définition de limites par catégorie
- Suivi en temps réel des dépenses vs budget
- Indicateurs visuels de dépassement
- Pourcentages d'utilisation

### 💹 Revenus
- Enregistrement des revenus ponctuels et récurrents
- Historique des entrées d'argent
- Calcul automatique du budget disponible

### 📈 Analyses et Graphiques
- Évolution des dépenses sur 6 mois
- Répartition par catégorie
- Graphiques interactifs et colorés

## 🛠️ Technologies Utilisées

- **Backend**: Flask 2.3.3 (Python)
- **Base de données**: SQLite avec SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Graphiques**: Chart.js (intégré via JavaScript)
- **Icons**: Font Awesome

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+ (testé avec Python 3.12.3)
- pip (gestionnaire de packages Python)

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/Plume-Paopedia/depenses-couple.git
cd depenses-couple
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
python app.py
```

L'application sera accessible à l'adresse : `http://localhost:5000`

### Configuration

- La base de données SQLite est créée automatiquement au premier lancement
- Des catégories par défaut sont ajoutées automatiquement
- Pour la production, modifiez la `SECRET_KEY` dans `app.py`

## 📱 Utilisation

### Premier lancement
1. L'application créera automatiquement la base de données avec des catégories par défaut
2. Accédez au tableau de bord pour voir l'interface
3. Commencez par ajouter vos premiers revenus et dépenses

### Navigation
- **Tableau de bord** (`/`) : Vue d'ensemble de vos finances
- **Dépenses** (`/expenses`) : Gestion et historique des dépenses
- **Abonnements** (`/subscriptions`) : Suivi des abonnements
- **Budgets** (`/budgets`) : Configuration et suivi des budgets

### Ajout de données
Utilisez les modales et formulaires disponibles sur chaque page pour :
- Ajouter une dépense avec sa catégorie
- Enregistrer un nouvel abonnement
- Définir des budgets par catégorie
- Saisir des revenus

## 🏗️ Structure du Projet

```
depenses-couple/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation
├── .gitignore            # Fichiers ignorés par Git
├── templates/            # Templates HTML
│   ├── base.html         # Template de base
│   ├── dashboard.html    # Tableau de bord
│   ├── expenses.html     # Page des dépenses
│   ├── subscriptions.html # Page des abonnements
│   └── budgets.html      # Page des budgets
└── static/               # Fichiers statiques
    ├── css/              # Styles CSS
    └── js/               # Scripts JavaScript
```

## 🗄️ Modèle de Base de Données

### Tables principales

- **Category** : Catégories de dépenses (Alimentation, Transport, etc.)
- **Expense** : Dépenses individuelles avec montant, description, date
- **Subscription** : Abonnements mensuels/annuels
- **Budget** : Limites budgétaires par catégorie
- **Income** : Revenus ponctuels ou récurrents

### Relations
- Les dépenses sont liées aux catégories
- Les budgets sont définis par catégorie
- Les abonnements sont catégorisés

## 🔌 API Endpoints

### Dépenses
- `POST /api/expenses` - Ajouter une dépense
- `GET /api/charts/expenses` - Données pour graphique des dépenses

### Abonnements
- `POST /api/subscriptions` - Ajouter un abonnement

### Budgets
- `POST /api/budgets` - Créer/modifier un budget

### Revenus
- `POST /api/income` - Ajouter un revenu

### Graphiques
- `GET /api/charts/categories` - Répartition par catégorie

## 🎨 Catégories par Défaut

L'application inclut des catégories préconfigurées :
- 🍽️ Alimentation
- 🚗 Transport
- 🏠 Logement
- 🎮 Divertissement
- ❤️ Santé
- 👕 Vêtements
- 🎓 Éducation
- 🔄 Abonnements
- ⚡ Autres

## 🤝 Contribution

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos modifications (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## 🔧 Développement

### Lancement en mode développement
```bash
export FLASK_ENV=development  # Sur Windows: set FLASK_ENV=development
python app.py
```

### Structure de développement
- L'application utilise SQLAlchemy pour l'ORM
- Les templates utilisent Jinja2
- Le mode debug est activé par défaut
- La base de données est automatiquement créée et initialisée

## 📝 Licence

Ce projet est sous licence libre. Vous pouvez l'utiliser, le modifier et le distribuer librement.

## 🙋‍♂️ Support

Pour toute question ou problème :
1. Vérifiez la documentation ci-dessus
2. Consultez les issues existantes sur GitHub
3. Créez une nouvelle issue si nécessaire

## 🎯 Roadmap

Fonctionnalités prévues :
- [ ] Export des données en CSV/Excel
- [ ] Notifications push pour les échéances
- [ ] Gestion multi-utilisateurs
- [ ] Synchronisation bancaire
- [ ] Application mobile
- [ ] Rapports mensuels automatiques

---

Développé avec ❤️ pour simplifier la gestion financière des couples.