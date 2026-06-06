# M-Motors - Backend

API REST Flask pour la plateforme de vente et location de véhicules M-Motors.

## Stack technique

- Python / Flask
- SQLAlchemy
- Flask-CORS
- PostgreSql
- JWT
- Bcrypt

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

## Endpoints

| Méthode | Route | Description |
|--------|-------|-------------|
| GET | `/vehicules` | Récupère tous les véhicules |
| GET | `/vehicules/filter?name=xxx` | Filtre les véhicules par nom |

## Architecture globale

Frontend React
↓
API FLASK
↓
PostgreSql

## Fonctionnalités actuelles

-Affichage véhicule
-Filtrage véhicules
-API fLASK
-Connection React a Flask
-Changement de sqlLite a PosteSQL
-Création compte utilisateur
-Vérification email
-Hashage sécurisé (mot de passe-bcrypt)
-Authentification user
-Générer token JWT
-Sotckage token coté client (localstorage)

## fonctionnalités à venir 

Authentification =>
-Routes protégées JWT
-Déconnexion user
-gestion des rôles (client/admin)

Espace client =>
-Dashboard user
-Consultation des demandes en cours
-Suivi des statuts dossiers

Gestion des dossiers=>
-Création d'une demande achat
-Création d"une demande LLD
-Gestion des statuts ( en cours, validé, refusé, documents manquants)

Gestion doc =>
-Upload doc
-Consultation des docs déposés
-Vérification des docs

Espace Admin =>
-Consultation de tous les dossiers
-Validation des demandes 
-Refus des demandes
-Mise à jour des status 

Qualité et déploiement 
-Test backend
-Test frontend
-Déploiement de l'app
-Doc tehnique 