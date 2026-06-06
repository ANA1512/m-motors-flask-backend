# M-Motors - Backend

API REST Flask pour la plateforme de vente et location de véhicules M-Motors.

## Stack technique

- Python / Flask
- SQLAlchemy
-PostgreSql
- Flask-CORS

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
