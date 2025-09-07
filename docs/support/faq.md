# ❓ FAQ - Questions Fréquentes

Retrouvez ici les réponses aux questions les plus couramment posées par les utilisateurs de Dépenses Couple.

## 🚀 Installation et Démarrage

### Q: L'application ne démarre pas, que faire ?

**R:** Vérifiez ces points dans l'ordre :

1. **Version de Python**
```bash
python --version
# Doit afficher Python 3.8 ou supérieur
```

2. **Installation des dépendances**
```bash
pip install -r requirements.txt
# Réinstallez si nécessaire avec --force-reinstall
```

3. **Port disponible**
```bash
# Si le port 5000 est occupé
lsof -i :5000
# Tuez le processus ou changez de port
```

### Q: Où sont stockées mes données ?

**R:** Vos données sont dans le fichier `expenses.db` (base SQLite) dans le dossier de l'application. 

**⚠️ Important :** Sauvegardez régulièrement ce fichier !

### Q: Puis-je utiliser l'application sur plusieurs appareils ?

**R:** L'application est conçue pour un usage local. Pour un usage multi-appareils :
- Installez sur un serveur accessible aux deux partenaires
- Ou synchronisez le fichier `expenses.db` via cloud (Dropbox, Google Drive)
- Attention aux conflits si utilisation simultanée !

---

## 💰 Gestion des Dépenses

### Q: Comment corriger une dépense saisie par erreur ?

**R:** Plusieurs options :

1. **Modification simple**
   - Cliquez sur l'icône "crayon" à côté de la dépense
   - Modifiez les champs nécessaires
   - Sauvegardez

2. **Suppression complète**
   - Cliquez sur l'icône "poubelle" 
   - Confirmez la suppression
   - ⚠️ Cette action est irréversible

3. **Annulation par dépense inverse**
   - Créez une nouvelle dépense avec un montant négatif
   - Même catégorie, description "Annulation [description originale]"

### Q: Comment gérer les dépenses en espèces ?

**R:** Saisissez-les comme les autres dépenses :
- Choisissez la personne qui a sorti l'argent
- Ajoutez "Espèces" dans la description
- Utilisez les commentaires pour préciser la source
- Exemple : "Boulangerie - Espèces depuis mon porte-monnaie"

### Q: Que faire pour les achats groupés (ex: courses) ?

**R:** Deux approches :

**Approche Globale (recommandée)**
```
Montant : 127,50€
Description : Courses hebdomadaires Carrefour
Catégorie : Alimentation
Notes : "Courses complètes : légumes, viande, produits entretien"
```

**Approche Détaillée**
```
Dépense 1 : 45€ - Légumes et fruits (Alimentation)
Dépense 2 : 62€ - Viande et poisson (Alimentation)  
Dépense 3 : 20,50€ - Produits d'entretien (Autres)
```

### Q: Comment catégoriser les dépenses mixtes ?

**R:** Utilisez la catégorie principale et précisez dans les notes :

```
Montant : 89€
Catégorie : Alimentation (60% du montant)
Description : Carrefour - Courses + Pharmacie
Notes : "Courses 60€ + médicaments 29€"
```

---

## 💬 Communication et Partage

### Q: Mon partenaire ne voit pas mes commentaires

**R:** Vérifiez que :
- Vous utilisez la même base de données (même fichier `expenses.db`)
- La page a été actualisée (F5)
- Les commentaires sont bien sauvegardés (bouton "Modifier")

### Q: Comment bien utiliser les champs de commentaires ?

**R:** Suivez ces bonnes pratiques :

**✅ Exemples efficaces :**
```
"Restaurant romantique pour nos 2 ans ❤️"
"Cadeau surprise pour ta promotion 🎉"
"Réparation urgente - à discuter du partage"
"Courses bio, on teste cette semaine"
```

**❌ Évitez :**
```
"ok"
"normal"  
"..."
[commentaire vide]
```

### Q: Comment négocier un partage équitable ?

**R:** Utilisez la fonction de négociation intégrée :

1. **Ouvrez la dépense** concernée
2. **Cliquez "Proposer un partage"**
3. **Justifiez votre proposition** avec bienveillance
4. **Proposez des alternatives** si refus

**Exemple de bonne négociation :**
```
"Je propose qu'on partage 70/30 car j'ai pris l'entrée 
et le dessert en plus. Qu'est-ce que tu en penses ? 😊"
```

---

## 🔄 Abonnements et Récurrence

### Q: Comment gérer les abonnements annuels ?

**R:** Deux méthodes :

**Méthode 1 : Abonnement annuel direct**
```
Nom : Assurance Auto
Montant : 900€
Cycle : Annuel
Prochaine facturation : 15/03/2025
```

**Méthode 2 : Provisionnement mensuel**
```
Nom : Provision Assurance Auto
Montant : 75€ (900€/12)
Cycle : Mensuel
Notes : "Mise de côté pour l'assurance annuelle"
```

### Q: Un abonnement a changé de prix, comment l'ajuster ?

**R:** 
1. Trouvez l'abonnement dans la liste
2. Cliquez sur "Modifier"
3. Changez le montant
4. Ajoutez une note : "Augmentation de X€ depuis le [date]"
5. Sauvegardez

### Q: Comment suspendre temporairement un abonnement ?

**R:** 
- Décochez "Actif" dans les paramètres de l'abonnement
- Ou changez la date de prochaine facturation
- Ajoutez une note explicative
- L'abonnement n'impactera plus vos calculs de budget

---

## 📊 Budgets et Analyses

### Q: Mes budgets sont toujours dépassés, comment les ajuster ?

**R:** Processus d'optimisation en 3 étapes :

1. **Analysez vos dépenses réelles** (3 derniers mois)
2. **Identifiez les catégories problématiques**
3. **Ajustez progressivement** (+20% du dépassement moyen)

**Exemple :**
```
Budget Divertissement : 100€
Dépenses moyennes : 140€
Nouveau budget : 120€ (100 + 20% de 40€)
```

### Q: Comment interpréter les graphiques ?

**R:** Guide de lecture :

**📈 Évolution des dépenses :**
- Tendance à la hausse = besoin de vigilance
- Pics isolés = dépenses exceptionnelles normales
- Tendance stable = bon contrôle

**🍰 Répartition par catégorie :**
- Alimentation > 30% = peut-être optimiser
- Divertissement > 20% = vérifier si acceptable
- Transport variable selon votre situation

### Q: Pourquoi mon "reste à vivre" est négatif ?

**R:** Plusieurs causes possibles :

1. **Revenus pas à jour** → Vérifiez vos saisies de revenus
2. **Mois exceptionnel** → Dépenses inhabituelles ce mois
3. **Abonnements oubliés** → Vérifiez les abonnements actifs
4. **Erreur de saisie** → Vérifiez les gros montants

---

## 🔔 Notifications et Rappels

### Q: Je ne reçois pas de notifications

**R:** Vérifications :

1. **Dans l'application :** Paramètres → Notifications activées
2. **Navigateur :** Autorisations de notifications accordées
3. **Système :** Notifications du navigateur activées
4. **Email :** Vérifiez vos spams (si emails activés)

### Q: Comment personnaliser les rappels ?

**R:** Accédez aux paramètres des rappels :
- Fréquence (quotidien, hebdomadaire, mensuel)
- Types de rappels (remboursements, budgets, occasions)
- Ton des messages (amical, professionnel, humoristique)
- Seuils de déclenchement

### Q: Les rappels sont trop fréquents/rares

**R:** Ajustez dans Paramètres → Rappels :
- **Trop fréquents :** Passez en mode "hebdomadaire" ou "essentiel"
- **Pas assez :** Activez les rappels quotidiens et baissez les seuils
- **Mode focus :** Suspendez temporairement pendant 1-7 jours

---

## 🤝 Utilisation en Couple

### Q: Comment convaincre mon partenaire d'utiliser l'app ?

**R:** Stratégies efficaces :

1. **Commencez seul** et montrez les bénéfices
2. **Proposez une période d'essai** (1 mois)
3. **Mettez l'accent sur la communication** plutôt que le contrôle
4. **Montrez les économies réalisées** grâce au suivi
5. **Adaptez à ses habitudes** (smartphone, ordinateur, etc.)

### Q: Nous avons des habitudes de dépenses très différentes

**R:** L'application s'adapte :
- **Budgets personnalisés** par catégorie
- **Partages flexibles** (50/50, proportionnel, personnalisé)
- **Commentaires** pour expliquer les différences
- **Négociation** pour trouver des compromis

### Q: Comment gérer les dépenses personnelles vs communes ?

**R:** Système de classification clair :

**🟢 Toujours Commun :**
- Logement, factures, courses alimentaires
- Sorties de couple, cadeaux familiaux

**🟡 À Négocier :**
- Restaurants, loisirs partagés
- Équipement maison, vacances

**🔴 Toujours Personnel :**
- Vêtements, soins personnels
- Cadeaux pour ses propres amis/famille
- Loisirs individuels

---

## 🔧 Problèmes Techniques

### Q: L'application est lente

**R:** Solutions par ordre de priorité :

1. **Redémarrer l'application** (Ctrl+C puis relancer)
2. **Vider le cache navigateur** (Ctrl+Shift+Delete)
3. **Nettoyer la base de données** (supprimer anciennes données)
4. **Vérifier l'espace disque** disponible
5. **Mettre à jour l'application** si nouvelle version

### Q: J'ai perdu mes données

**R:** Récupération possible :

1. **Vérifiez la corbeille** (si suppression accidentelle)
2. **Cherchez des sauvegardes** automatiques (`expenses.db.backup`)
3. **Restaurez depuis cloud** si synchronisation activée
4. **Récupération partielle** via historique navigateur
5. **⚠️ Pour l'avenir :** Sauvegarde hebdomadaire recommandée

### Q: Erreur lors de l'ajout d'une dépense

**R:** Vérifications :

1. **Tous les champs requis** sont remplis
2. **Format des montants** correct (virgule ou point selon config)
3. **Date valide** (pas dans le futur si restriction activée)
4. **Catégorie sélectionnée** existe encore
5. **Redémarrer l'app** si problème persiste

---

## 📱 Utilisation Mobile

### Q: L'application fonctionne-t-elle sur smartphone ?

**R:** Oui, via navigateur web :
- **Interface responsive** adaptée aux petits écrans
- **Navigation tactile** optimisée
- **Saisie rapide** depuis le mobile
- **⚠️ Limitation :** Pas d'app native (pour l'instant)

### Q: Comment utiliser efficacement sur mobile ?

**R:** Conseils d'usage mobile :

1. **Marquez la page** en favori pour accès rapide
2. **Ajoutez un raccourci** sur l'écran d'accueil
3. **Utilisez la saisie vocale** pour les descriptions
4. **Préparez des templates** de commentaires fréquents
5. **Synchronisez régulièrement** avec la version ordinateur

---

## 💡 Conseils d'Optimisation

### Q: Comment rendre l'utilisation plus fluide ?

**R:** Habitudes qui font la différence :

**⚡ Saisie Express :**
- Templates de descriptions fréquentes
- Catégories par défaut selon le lieu
- Commentaires pré-rédigés

**🔄 Routine Optimale :**
- Saisie immédiate lors de l'achat
- Révision hebdomadaire des dépenses
- Négociation mensuelle des partages
- Analyse trimestrielle des tendances

**🎯 Personnalisation :**
- Budgets adaptés à VOS habitudes
- Notifications selon VOTRE rythme
- Partages selon VOTRE équité
- Catégories selon VOS besoins

---

*Cette FAQ évolue selon vos retours ! N'hésitez pas à nous signaler d'autres questions fréquentes. 💬*