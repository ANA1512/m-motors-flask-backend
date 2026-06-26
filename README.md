# M-Motors - Backend

API REST Flask pour la plateforme de vente et location de véhicules M-Motors.

L'API assure  la communication entre front React et PostgreSL. Elle gère l'authentification des users, les véhicules, les dossiers client, les doc transmis pour la demande de financement. 


## Stack technique

- Python / Flask
- SQLAlchemy
- Flask-CORS
- Flask-JWT-Extended
- PostgreSql
- Bcrypt


## Architecture globale

Frontend React
↓
API FLASK
↓
PostgreSql

## Fonctionnalités réalisées

#Gestion des users
-Connection React a Flask
-Changement de sqlLite a PosteSQL
-Création compte utilisateur
-Vérification email
-Hashage sécurisé (mot de passe-bcrypt)
-Authentification par JWT
-Générer token JWT
-Route /me permettant de récupérer l'user connecté et son rôle 
-Stockage token coté client (localstorage)

#véhicules 
- Consultation de tous les véhicules
- Consultation d'un véhicule
- Filtrage véhicules
- CRUD des véhicules via API 

Gestion des dossiers=>
- Création d'une demande achat
- Création d"une demande LLD
- Gestion des statuts ( en attente, validé, refusé, documents manquants)
- Consultation, modification, suppression 

Gestion doc =>
- Upload doc
- Association des doc à un dossier
- Consultation des docs déposés en lecture seule par admin
- Vérification des docs

Espace Admin =>
- Consultation de tous les dossiers
- Validation  ou refus des demandes 
- Mise à jour des status
- Suppression d'un dossier

## Base de données

Utilisation de PostgreSQL via SQLALchemy

Les principames tables sont  :
- User
- Vehicule
- Dossier
- Document 

## Installation

```bash
git clone https://github.com/ANA1512/m-motors-flask-backend.git
cd m-motors-flask-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Le serveur tourne sur `http://localhost:5001`

# TEST 

Backend => 
- Postman utilisé pour tester les routes API
- Pytest pour les tests automatisés 
- Frontend (Playwright)

# Déploiement 

- Backend : RENDER
- Base de données  : PostgreSQL (render)
- Frontend : Netlify
  
  Point à configurer pour fonctionnement  :
- Variables d'environnement
- Connexion à la base PostGreSQL de production 
- Configuration CORS
- MAJ des Urls entre env local et production 
- Initialisation de la base grâce au script de seed des véhicules 

# Difficultes rencontrées 

- Configurations des règles CORS entre REACT et FLASK
- Gestion des URLS env local et production 
- Connexion à la bonne base de PostgreSQL lors du déploiement 
-Initialisation de la bd avec le script de seed
- Sécurisation des routes (JWT)

