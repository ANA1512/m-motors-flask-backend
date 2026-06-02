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
             new_user = User(
                id = request.form.get('id'),
                name = request.form.get('name'),
                email = request.form.get('email'),
                password = request.form.get('password'),
                role = request.form.get('role')
             )
             db.session.add(new_user)
             db.session.commit()
             return ("/login.jsx")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5001)


  

