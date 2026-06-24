from app import app
from models.models import db, Vehicule

vehicules = [
    Vehicule(name="Audi A3", description="Berline compacte élégante", price=22000, type="Vente", kilometrage=15000, marque="Audi", transmission="Automatique", places=5),
    Vehicule(name="Mercedes Classe A", description="Citadine premium", price=28000, type="Vente", kilometrage=8000, marque="Mercedes", transmission="Automatique", places=5),
    Vehicule(name="Volkswagen Golf", description="Compacte polyvalente", price=18000, type="Vente", kilometrage=25000, marque="Volkswagen", transmission="Manuelle", places=5),
    Vehicule(name="Toyota Yaris", description="Citadine économique", price=14000, type="Vente", kilometrage=30000, marque="Toyota", transmission="Manuelle", places=5),
    Vehicule(name="Ford Focus", description="Berline familiale", price=16000, type="Vente", kilometrage=20000, marque="Ford", transmission="Manuelle", places=5),
    Vehicule(name="BMW X1", description="SUV premium", price=800, type="Location", kilometrage=5000, marque="BMW", transmission="Automatique", places=5),
    Vehicule(name="Peugeot 2008", description="SUV compact moderne", price=450, type="Location", kilometrage=12000, marque="Peugeot", transmission="Automatique", places=5),
    Vehicule(name="Renault Captur", description="Crossover familial", price=350, type="Location", kilometrage=18000, marque="Renault", transmission="Manuelle", places=5),
    Vehicule(name="Citroën C3", description="Citadine pratique", price=280, type="Location", kilometrage=22000, marque="Citroën", transmission="Manuelle", places=5),
    Vehicule(name="Nissan Juke", description="SUV sportif", price=500, type="Location", kilometrage=8000, marque="Nissan", transmission="Automatique", places=5),
    Vehicule(name="Peugeot 308", description="Compacte berline en excellent état", price=15000, type="Vente", kilometrage=45000, marque="Peugeot", transmission="Manuelle", places=5),
    Vehicule(name="Renault Clio", description="Compacte fiable", price=12000, type="Vente", kilometrage=30000, marque="Renault", transmission="Manuelle", places=5),
    Vehicule(name="BMW Série 3", description="Berline premium", price=35000, type="Vente", kilometrage=20000, marque="BMW", transmission="Manuelle", places=5),
]

with app.app_context():
    if Vehicule.query.count() > 0:
        print("Des véhicules existent déjà, seed annulé.")
    else:
        db.session.add_all(vehicules)
        db.session.commit()
        print("Seed terminé : véhicules ajoutés.")