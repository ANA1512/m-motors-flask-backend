from flask import Flask, jsonify, request
#import variable db
from models.models import db , Vehicule, User,Dossier
#import flask-cors
from flask_cors import CORS
#env variable
from dotenv import load_dotenv
import os
load_dotenv()
#routes protégées
from flask_jwt_extended import jwt_required, get_jwt_identity


#create the app
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])


#import bcrypt and jwt
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager , create_access_token
bcrypt = Bcrypt(app)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

#import flask-migrate
from flask_migrate import Migrate
migrate = Migrate(app, db)



#configure the PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"]= os.environ.get("DATABASE_URL")

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

@app.route("/register", methods =["GET","POST"])
def register():
       if request.method == "POST":

        data= request.get_json()
        email = data.get('email')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user :
                return jsonify({"message": "Cet email existe déjà"}),409

        hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
        new_user = User(
                name = data.get('name'),
                email = email,
                password = hashed_password,
                role = data.get('role')
             )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Utilisateur créé avec succès"}), 201

@app.route("/login",methods =[ "GET","POST"])
def login():
       if request.method == "POST" :
          
                email = request.json.get('email')
                password = request.json.get('password')
                user = User.query.filter_by(email=email).first()

                if not user or not bcrypt.check_password_hash(user.password, password):
                        return jsonify({'message': 'Invalid email or password'}), 401
                
                token = create_access_token(identity=str(user.id))

                return jsonify({'token': token}), 200

@app.route("/mon-compte", methods=["GET"])
@jwt_required()
def mon_compte():
       user_id = get_jwt_identity()
       user = User.query.get(user_id)
       return jsonify(user.to_dict()),200

@app.route("/dossier", methods =["POST"])
@jwt_required()
def dossier() :
        data= request.get_json()
        user_id =get_jwt_identity(),
        new_dossier = Dossier(
        user_id =user_id,
        vehicule_id = data.get("vehicule_id"),
        type_financement = data.get("type_financement"),
        revenu_mensuel = data.get("revenu_mensuel"),
        statut = data.get("statut")
        )
        db.session.add(new_dossier)
        db.session.commit()

        return jsonify(new_dossier.to_dict()),201
        

if __name__ == "__main__":
    app.run(port=5001, debug= True)


  

