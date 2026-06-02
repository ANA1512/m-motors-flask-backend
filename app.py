from flask import Flask, jsonify, request
#import variable db
from models.models import db , Vehicule, User
#import flask-cors
from flask_cors import CORS
#env variable
from dotenv import load_dotenv
import os
load_dotenv()



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
             hashed_password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
             new_user = User(
                name = request.form.get('name'),
                email = request.form.get('email'),
                password = hashed_password,
                role = request.form.get('role')
             )
             db.session.add(new_user)
             db.session.commit()
             return jsonify({"message": "Utilisateur créé avec succès"}), 201

@app.route("/login",methods =[ "GET","POST"])
def login():
       if request.method == "POST" :
          
                email = request.form.get('email')
                password = request.form.get('password')
                user = User.query.filter_by(email=email).first()

                if not user or not bcrypt.check_password_hash(user.password, password):
                        return jsonify({'message': 'Invalid email or password'}), 401
                
                token = create_access_token(identity=str(user.id))

                return jsonify({'token': token}), 200
            

if __name__ == "__main__":
    app.run(port=5001, debug= True)


  

