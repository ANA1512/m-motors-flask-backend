from flask import Flask, jsonify, request
#import variable db
from models.models import db , Vehicule


#create the app
app = Flask(__name__)


#configure the SQLite db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vehicules.db"

# initialize the app with the extension
db.init_app(app)

#app use the flask context
with app.app_context():
    try :
        db.drop_all()
        db.create_all()
        
        voiture1 = Vehicule(name="Renault", description=" cinq portes", price ="30")
        voiture2 = Vehicule(name="bmw", description=" trois portes", price ="20")

        db.session.add(voiture1)
        db.session.add(voiture2)
        db.session.commit()

        voiture1_db =db.session.query(Vehicule).filter(Vehicule.name == 'Renault').first()
        voiture2_db =db.session.query(Vehicule).filter(Vehicule.name == 'bmw').first()
        print(f"{voiture1_db.id}: {voiture1_db.name} - {voiture1_db.description} -{ voiture1_db.price}")
        print(f"{voiture2_db.id}: {voiture2_db.name} - {voiture2_db.description} -{ voiture2_db.price}")
        
        @app.route("/vehicules")
        def all_vehicules() :
            vehicules =Vehicule.query.all()
            return jsonify([v.to_dict() for v in vehicules])

        @app.route("/vehicules/filter")
        def index():
            name = request.args.get('name')
            res= db.session.query(Vehicule).filter(Vehicule.name ==name).first()
            return jsonify(res.to_dict())
    
        app.run()
    except Exception as ex:
        print(ex)

  

