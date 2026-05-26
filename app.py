from flask import Flask, jsonify, request
#import variable db
from models.models import db , Vehicule
#import flask-cors
from flask_cors import CORS


#create the app
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])


#configure the SQLite db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vehicules.db"

# initialize the app with the extension
db.init_app(app)

@app.route("/vehicules")
def all_vehicules() :
        vehicules =Vehicule.query.all()
        return jsonify([v.to_dict() for v in vehicules])

@app.route("/vehicules/filter")
def index():
        name = request.args.get('name')
        res= db.session.query(Vehicule).filter(Vehicule.name ==name).first()
        return jsonify(res.to_dict())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5001)


  

