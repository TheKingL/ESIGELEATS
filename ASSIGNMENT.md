# Spécifications du Projet

Ce projet consiste en une application web de gestion de recettes. L'application permet aux utilisateurs de créer, consulter, annoter et noter des recettes de cuisine.
Les administrateurs ont la capacité de valider ou refuser les recettes soumises par les utilisateurs.

## Fonctionnalités Requises

Ces fonctionnalités constituent le cœur de l'application et doivent être implémentées en priorité.

### Authentification
Les utilisateurs doivent pouvoir créer un compte et se connecter de manière sécurisée.
- Login/Logout avec sessions
- Inscription de nouveaux utilisateurs
- Profils utilisateurs basiques
- Profils privés/publics
- Support des comptes administrateurs

### Gestion des Recettes
Le système de gestion des recettes permet d'organiser, de consulter et de partager des recettes de cuisine.
- Affichage d'une liste de recettes
  - Avec un champ dédié pour saisir et afficher les ingrédients
- Gestion des recettes favorites
- Ajout d'annotations personnelles (publiques ou privées selon le profil)
  - Les annotations doivent s'actualiser en temps réel
- Attribution d'une note sur 5 pour chaque recette
- Calcul et affichage de la note moyenne d'une recette
- Recherche de recettes (par titre, ingrédient, etc.)
- Consultation de la page profil d'un utilisateur
- Création de recettes par les utilisateurs, avec validation obligatoire par un administrateur

### États des Recettes
Chaque recette passe par différents états qui définissent son cycle de vie.
- Validation par un administrateur en attente
- À modifier
- Validée
- Refusée

### Interface Administrative
Une interface dédiée aux administrateurs pour la gestion et la supervision de l'application.
- Vue de tous les utilisateurs
- Vue de toutes les recettes
- Panneau d'administration pour valider/refuser des recettes

## Compétences Techniques à Démontrer

Durant ce projet, vous devrez démontrer votre maîtrise des composants suivants :

### HTML/Formulaires
- Création de formulaires statiques HTML (login, inscription, création de recette)
- Validation native des champs (required, pattern, etc.)
- Structure sémantique des pages

### JavaScript/Interactivité
- Création de formulaires dynamiques
- Mise à jour en temps réel des données (annotations, notes, états des recettes)
- Manipulation du DOM pour l'interface utilisateur
- Requêtes AJAX pour les interactions avec l'API

### Python/Flask
- Gestion des routes et des contrôleurs
- Manipulation des sessions utilisateur
- Création d'API RESTful
- Intégration avec la base de données
- Protection des routes avec des décorateurs

### Base de Données
- Conception du schéma relationnel
- Création des tables et relations
- Requêtes SQL pour la manipulation des données
- Gestion des transactions

## Fonctionnalités Facultatives

Ces fonctionnalités permettent d'enrichir l'expérience utilisateur mais ne sont pas essentielles au fonctionnement de base.

### Améliorations Authentification
Fonctionnalités additionnelles pour personnaliser l'expérience utilisateur.
- Images de profil personnalisées
- Préférences utilisateur (thème, paramètres de confidentialité)

### Améliorations Application Recettes
Ajouts qui enrichissent l'expérience autour des recettes.
- Filtre et tri avancés côté front (par note, temps de préparation, difficulté, etc.)
- Historique des recettes consultées ou créées
- Suggestions de recettes similaires

### API
Points d'accès pour l'intégration avec d'autres services ou applications.
- Endpoints REST pour les données de recettes et d'utilisateurs
- Mises à jour en temps réel (annotations, favoris, notes)
- API administrative

### Statistiques Avancées
Analyse approfondie autour des recettes et de l'activité des utilisateurs.
- Classements de recettes (les mieux notées, les plus commentées, les plus favorites)
- Graphiques d'évolution des notes ou du nombre de favoris
- Statistiques par utilisateur (nombre de recettes publiées, moyenne des notes reçues)
