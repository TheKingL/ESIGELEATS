# 🍽️ ESIGELEATS – Plateforme de recettes ESIGELEC

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?logo=tailwind-css&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![CI/CD](https://img.shields.io/badge/GitHub%20Actions-Active-2088FF?logo=github-actions&logoColor=white)

Application web de gestion de recettes réalisée en **Flask**.
Les étudiants peuvent créer, noter, commenter et mettre en favori des recettes.
Les administrateurs disposent d’un panneau de modération et d’un dashboard de statistiques (**ApexCharts**).

> ℹ️ **Remarque :** Dans la version finale, les *annotations* du sujet ont été remplacées par de vrais **commentaires publics** sous chaque recette.

---

## ✨ Fonctionnalités Principales

### 👤 1. Authentification et Profils

* **Accès :** Création de compte, login et logout via sessions Flask.
* **Profils utilisateurs :**
  * Nom d’utilisateur + Nom affiché.
  * Biographie personnalisable.
  * Profil **public** ou **privé**.
* **Gestion des rôles :**
  * Utilisateur classique (public ou privé).
  * Administrateur (Modération + Dashboard).
* **Visibilité :** Page de profil publique accessible uniquement aux connectés.
* **Gestion de compte :** Édition du profil, changement de mot de passe, suppression de compte.

### 🍳 2. Recettes

* **CRUD complet :** Création, édition et suppression de recettes par les utilisateurs.
* **Contenu :**
  * Titre, description, image uploadée.
  * Nombre de portions.
  * Temps de préparation.
  * Liste d’ingrédients avec quantités libres.
  * Étapes numérotées de préparation.
* **Modération :** Validation obligatoire par un administrateur avant apparition publique.
* **Navigation :** Recherche par titre, tri et filtres.
* **Interactivité :** Sélecteur de portions intelligent qui ajuste les quantités en JavaScript.

### ⭐ 3. Notes, Favoris et Commentaires

* **Notes sur 5 étoiles :**
  * Une seule note par utilisateur/recette.
  * Mise à jour en temps réel (AJAX).
  * Calcul dynamique de la moyenne.
* **Favoris :** Bouton cœur cliquable pour ajouter/retirer des favoris instantanément (JavaScript).
* **Commentaires :**
  * Espace de discussion sous chaque recette.
  * Affichage de l'avatar (lettre), du pseudo et des badges de rôle.

### 🚦 4. États des Recettes et Modération

Chaque recette possède un statut :

* `PENDING` : En attente de validation.
* `CHANGES_REQUIRED` : Modifications demandées par l'admin.
* `APPROVED` : Validée (visible publiquement).
* `REJECTED` : Refusée.

**Interface Admin :**
* Liste des recettes en attente.
* Actions rapides en AJAX (Valider / Demander modif / Refuser).
* Toasts visuels de confirmation.

### 🔔 5. Notifications Visuelles

* **Pastilles rouges** dans la navbar et sur le profil.
* **Utilisateurs :** Alertes pour les recettes "À modifier".
* **Admins :** Alertes pour les nouvelles recettes "En attente".
* **Auto-refresh :** Actualisation automatique des compteurs (toutes les 30s).

### 📊 6. Dashboard Admin (Insights)

Page exclusive aux administrateurs avec des graphiques **ApexCharts** interactifs :
* Indicateurs globaux (KPIs).
* Répartition des statuts (Donut chart).
* Évolution temporelle des créations/validations.
* Distribution des notes et Top Auteurs.

---

## 🛠️ Stack Technique

### Backend
* **Flask 3.1** : Le cœur de l'application.
* **Flask-Session** : Gestion des sessions serveur.
* **SQLite** : Base de données légère (fichier `database.db`).
* **Architecture MVC** : Séparation claire (Routes / Controllers / Models).
* **SQL Raw** : Pas d'ORM lourd, requêtes SQL optimisées à la main.

### Frontend
* **Jinja2** : Moteur de templates.
* **TailwindCSS** : Framework CSS utilitaire (compilé).
* **JavaScript Vanilla** : Pas de framework JS lourd (React/Vue), tout est fait main (AJAX, DOM).
* **ApexCharts** : Bibliothèque de graphiques modernes.

### Qualité & CI/CD
* **Linters :** `ruff`, `pylint` (Python), `djlint` (HTML), `eslint` (JS), `prettier` (JS).
* **Tests :** `pytest` pour les tests unitaires et d'intégration.
* **Coverage :** Rapport de couverture de code (> 70%).
* **Hooks Git :** `pre-commit` pour forcer la qualité avant chaque commit.
* **GitHub Actions :** Pipeline CI complet (Lint + Test + Build Docker).

---

## 💻 Installation et Lancement

### 1. Cloner le dépôt
```bash
git clone [https://github.com/esigpoitiers/projet-site-web-TheKingL](https://github.com/esigpoitiers/projet-site-web-TheKingL)
cd projet-site-web-TheKingL
```

### 2. Environnement Virtuel
```bash
# macOS / Linux
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Dépendances
```bash
# Python
pip install -r requirements.txt

# JavaScript (Tailwind, Linters JS)
# Installe automatiquement tout ce qui est dans package.json
npm install
```

### 4. Base de Données
```bash
# Création des tables
sqlite3 database.db < sql/setupdb.sql

# (Optionnel) Données de démo
sqlite3 database.db < sql/fill_recipes.sql

# Créer un Admin
python add_admin.py
```

### 5. Build CSS & Lancement
```bash
# Générer le CSS Tailwind
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify

# Lancer le serveur (Debug mode)
flask run --debug
```
🚀 Accédez à l'application sur : **http://127.0.0.1:5050**

---

## 🐳 Docker

Pour lancer l'application dans un conteneur isolé sans rien installer :

```bash
# Construire l'image
docker build -t esigeleats .

# Lancer le conteneur
docker run --rm -p 5050:5050 esigeleats
```

---

## ✅ Tests & Qualité

Pour vérifier que tout est carré :

```bash
# Lancer les tests
pytest

# Vérifier la couverture
coverage run --sources=routes/ -m pytest
coverage report
coverage html # génère un rapport HTML détaillé dans htmlcov/
```