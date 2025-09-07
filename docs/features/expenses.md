# 💸 Gestion des Dépenses

La gestion des dépenses est au cœur de l'application Dépenses Couple. Cette section vous guide dans l'utilisation optimale de toutes les fonctionnalités liées aux dépenses.

## 🎯 Vue d'Ensemble

### Qu'est-ce qu'une Dépense ?

Dans l'application, une dépense représente toute sortie d'argent avec ces informations :
- **💰 Montant** : La somme dépensée (obligatoire)
- **📝 Description** : Ce qui a été acheté (obligatoire)
- **📅 Date** : Quand l'achat a eu lieu
- **🏷️ Catégorie** : Type de dépense (Alimentation, Transport, etc.)
- **👤 Personne** : Qui a payé
- **💬 Notes** : Commentaires et contexte
- **⚡ Exceptionnelle** : Si c'est une dépense inhabituelle
- **💳 Remboursement** : Si une personne doit rembourser

---

## ➕ Ajouter une Dépense

### 1. Accès Rapide

Plusieurs moyens d'ajouter une dépense :
- **Bouton principal** : "Nouvelle dépense" sur le tableau de bord
- **Menu navigation** : Section "Dépenses" → "Ajouter"
- **Actions rapides** : Widget dédié en bas de page
- **Raccourci clavier** : `Ctrl + N` (si configuré)

### 2. Formulaire de Saisie

```
💸 Nouvelle Dépense

💰 Montant * : [85,50] €
📝 Description * : [Restaurant Chez Luigi]
📅 Date : [2024-12-07] 📅
🏷️ Catégorie * : [Divertissement] ▼

👤 Payé par : [Alex] ▼
☑️ Dépense exceptionnelle
☑️ Nécessite un remboursement

💬 Notes :
[Dîner romantique pour nos 2 ans ❤️
Sam me doit sa part : 42,75€]

[Ajouter] [Annuler]
```

### 3. Champs Détaillés

**💰 Montant**
- Format accepté : `85.50`, `85,50`, `85`
- Devise automatique : € (configurable)
- Validation : Doit être > 0

**📝 Description**
- Exemples : "Courses Carrefour", "Essence Total", "Restaurant Luigi"
- Conseils : Soyez précis pour retrouver facilement
- Limite : 200 caractères

**🏷️ Catégorie**
- Liste prédéfinie : Alimentation, Transport, Logement...
- Création possible de nouvelles catégories
- Impact sur les budgets et analyses

**👤 Personne**
- Liste personnalisable : Vos prénoms
- "Non spécifié" par défaut (à personnaliser)
- Mémorisation automatique pour faciliter la saisie

**💬 Notes**
- **Très important** pour la communication en couple
- Expliquez le contexte, la motivation
- Mentionnez les arrangements de partage
- Limite : 500 caractères

---

## ✏️ Modifier une Dépense

### 1. Accès à la Modification

Dans la liste des dépenses :
- Cliquez sur l'**icône crayon** à côté de la dépense
- Ou cliquez sur la ligne de la dépense (si activé)

### 2. Types de Modifications

**Corrections Simples**
```
Avant : "Restaurant" - 85€
Après : "Restaurant Chez Luigi" - 87,50€
Note ajoutée : "J'avais oublié le pourboire"
```

**Ajout d'Informations**
```
Dépense basique : "Courses - 67€"
Après modification :
- Catégorie : Alimentation  
- Personne : Alex
- Notes : "Courses bio de la semaine, très bons légumes ! 🥕"
- Remboursement : Sam doit 33,50€
```

**Négociation Différée**
```
Dépense initiale : "Réparation voiture - 320€" (Alex)
Modification après discussion :
- Remboursement activé
- Notes : "Discuté avec Sam, partage 60/40 car elle l'utilise plus"
- Montant à rembourser : 128€ (40% de 320€)
```

---

## 🗑️ Supprimer une Dépense

### Quand Supprimer ?

- **Erreur de saisie** importante
- **Doublon** accidentel
- **Annulation** d'un achat (remboursement magasin)

### Comment Supprimer

1. Trouvez la dépense dans la liste
2. Cliquez sur l'**icône poubelle** 🗑️
3. Confirmez la suppression
4. ⚠️ **Action irréversible** - soyez sûr !

### Alternative : Dépense d'Annulation

Pour traçabilité, préférez parfois une dépense négative :
```
Dépense originale : "Veste H&M - 45€"
Dépense d'annulation : "Remboursement veste H&M - (-45€)"
Notes : "Taille incorrecte, échangé le lendemain"
```

---

## 🔍 Recherche et Filtrage

### 1. Barre de Recherche

Recherchez par :
- **Description** : "restaurant", "carrefour"
- **Notes** : "cadeau", "remboursement"
- **Montant** : "45", "45.50"
- **Personne** : "Alex", "Sam"

### 2. Filtres Avancés

**Par Catégorie**
```
🍽️ Alimentation uniquement
🚗 Transport uniquement
🎮 Divertissement uniquement
[Toutes] pour réinitialiser
```

**Par Période**
```
📅 Ce mois-ci
📅 Mois dernier  
📅 Trimestre en cours
📅 Période personnalisée : [01/10] à [31/12]
```

**Par Personne**
```
👤 Dépenses d'Alex uniquement
👤 Dépenses de Sam uniquement
👤 Toutes les dépenses
```

**Par Statut**
```
💳 Avec remboursement uniquement
⚡ Exceptionnelles uniquement
💬 Avec commentaires uniquement
```

### 3. Tri et Organisation

Triez vos dépenses par :
- **Date** (récent → ancien ou inverse)
- **Montant** (croissant ou décroissant)
- **Catégorie** (alphabétique)
- **Personne** (Alex puis Sam ou inverse)

---

## 📊 Analyses des Dépenses

### 1. Vue Mensuelle

```
📊 Novembre 2024 - Vos Dépenses

Total : 1.247,50€ (+12% vs Octobre)

Par catégorie :
🍽️ Alimentation : 387€ (31%) [Budget : 400€] ✅
🚗 Transport : 156€ (13%) [Budget : 200€] ✅  
🎮 Divertissement : 234€ (19%) [Budget : 150€] ⚠️
🏠 Logement : 289€ (23%) [Budget : 300€] ✅
👕 Vêtements : 98€ (8%) [Budget : 80€] ⚠️
⚡ Autres : 83€ (6%) [Budget : 100€] ✅

Tendance : +2 dépassements vs mois dernier
```

### 2. Comparaisons Temporelles

```
📈 Évolution 6 Derniers Mois

Juin : 1.156€
Juillet : 1.034€ (vacances préparées)
Août : 1.789€ (vacances réalisées)
Septembre : 1.123€ (retour calme)
Octobre : 1.113€ (stable)
Novembre : 1.248€ (fêtes préparées)

Moyenne : 1.244€/mois
Tendance : Stabilité avec pics prévisibles ✅
```

### 3. Analyse par Personne

```
👥 Répartition Alex / Sam - Novembre

Alex a payé : 745€ (60%) 
├─ 12 dépenses
├─ Ticket moyen : 62€
└─ Plus grosse : 145€ (courses familiales)

Sam a payé : 502€ (40%)
├─ 8 dépenses  
├─ Ticket moyen : 63€
└─ Plus grosse : 89€ (restaurant)

Équilibrage après remboursements :
Alex : 623€ (50%) ✅
Sam : 624€ (50%) ✅
```

---

## 💬 Communication sur les Dépenses

### 1. Bonnes Pratiques de Commentaires

**✅ Commentaires Efficaces**
```
"Courses bio cette semaine, on teste la qualité 🥕"
"Cadeau surprise pour ta promotion - bien mérité ! 🎉"
"Plein d'essence pour notre weekend Normandie 🚗"
"Pizza livraison, trop fatigués pour cuisiner 😴"
"Pharmacie urgence - mal de tête carabiné 💊"
```

**❌ Commentaires Inutiles**
```
"Normal"
"OK"  
"Habituel"
[pas de commentaire]
```

### 2. Communication des Remboursements

**Demandes Bienveillantes**
```
"Resto sympa ! Tu peux me rembourser ta part ? (42€) 😊"
"J'ai avancé pour nous deux, remboursement quand tu peux ❤️"
"Courses communes, on partage 50/50 comme d'hab ?"
```

**Justifications Claires**
```
"Réparation ma voiture, 100% personnel"
"Cadeau pour tes parents, tu me rembourses ?"
"Sortie avec mes amis, je règle ma part"
```

### 3. Négociation dans les Notes

```
"Resto gastronomique - je propose de partager 60/40 
car j'ai insisté pour cet endroit cher 😊"

"Courses + mes produits beauté (25€)
Partage sur le reste : 45€ à partager ?"

"Weekend spa pour mes 30 ans 🎂
J'aimerais que ce soit ton cadeau ❤️"
```

---

## 🎯 Conseils d'Optimisation

### 1. Habitudes Efficaces

**⚡ Saisie Immédiate**
- Ajoutez la dépense directement après l'achat
- Utilisez votre smartphone en mobilité
- Ne remettez jamais à plus tard

**📝 Documentation Systématique**
- Toujours remplir les notes
- Expliquer le contexte et la motivation
- Mentionner les arrangements spéciaux

**🔄 Révision Régulière**
- Vérifiez vos dépenses chaque weekend
- Corrigez les erreurs rapidement
- Négociez les remboursements en temps réel

### 2. Templates de Saisie

Créez vos modèles pour gagner du temps :

**Courses Alimentaires**
```
Description : "Courses [magasin]"
Catégorie : Alimentation
Notes : "Courses [période] - partage 50/50"
```

**Restaurants**
```
Description : "Restaurant [nom]"
Catégorie : Divertissement  
Notes : "[Occasion] - [qui invite qui]"
```

**Transport**
```
Description : "Essence [station]"
Catégorie : Transport
Notes : "Plein pour [destination/période]"
```

### 3. Gestion des Exceptions

**Dépenses Exceptionnelles**
- Cochez systématiquement la case
- Justifiez dans les notes
- Prévoyez l'impact sur le budget

**Urgences**
```
"Réparation chaudière - 450€"
☑️ Exceptionnel
Notes : "Urgence absolue, on puise dans l'épargne"
Remboursement : À discuter selon notre accord urgences
```

**Cadeaux Surprises**
```
"Bijoux pour anniversaire - 180€"  
☑️ Exceptionnel
Notes : "Surprise ! Budget cadeau dépassé mais elle le vaut ❤️"
Remboursement : 0€ (cadeau personnel)
```

---

## 🔔 Notifications et Rappels

### 1. Notifications Automatiques

**Ajout de Dépense**
```
💸 Nouvelle dépense ajoutée
"Alex a ajouté : Restaurant (85€)"
[Voir détails] [Commenter]
```

**Demande de Remboursement**
```
💰 Remboursement demandé  
"Sam demande 42€ pour le restaurant d'hier"
[Accepter] [Négocier] [Voir détails]
```

### 2. Rappels de Saisie

Si vous oubliez de saisir :
```
📝 Rappel de Saisie
"Aucune dépense depuis 3 jours
Avez-vous des achats à ajouter ?"
[Ajouter maintenant] [Rien à signaler] [Reporter]
```

### 3. Alertes Budget

```
⚠️ Alerte Budget
"Catégorie Divertissement : 89% utilisé  
Reste : 16€ pour 8 jours"
[Voir détails] [Ajuster budget] [Continuer]
```

---

## 🛠️ Configuration Avancée

### 1. Préférences de Saisie

```
⚙️ Paramètres des Dépenses

Devise par défaut : [EUR €] ▼
Format montant : [1.234,56] ▼
Catégorie par défaut : [Dernière utilisée] ▼
Personne par défaut : [Personne connectée] ▼

Validation automatique :
☑️ Date du jour par défaut
☑️ Alerte si montant > 200€
☑️ Rappel notes si vide
□ Sauvegarde automatique (draft)
```

### 2. Gestion des Catégories

**Catégories par Défaut**
- 🍽️ Alimentation
- 🚗 Transport  
- 🏠 Logement
- 🎮 Divertissement
- ❤️ Santé
- 👕 Vêtements
- 🎓 Éducation
- 🔄 Abonnements
- ⚡ Autres

**Ajouter une Catégorie**
```
🎨 Nouvelle Catégorie

Nom : [Bricolage]
Icône : [🔨] (choix multiple)
Couleur : [#FF6B35] 🎨
Budget suggéré : [100€/mois]

[Créer] [Annuler]
```

---

## 📱 Usage Mobile

### Optimisations Mobile

**Interface Adaptée**
- Formulaires tactiles
- Boutons plus gros
- Navigation par glissement

**Saisie Rapide**
- Reconnaissance vocale pour descriptions
- Suggestions automatiques
- Templates favoris

**Mode Hors-ligne**
- Sauvegarde locale temporaire
- Synchronisation au retour réseau
- Indicateur de statut

---

*La gestion des dépenses devient un plaisir quand elle facilite la communication en couple ! 💸💕*