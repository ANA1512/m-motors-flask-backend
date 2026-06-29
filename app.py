from flask import Flask, jsonify, request
#import variable db
from models.models import db , Vehicule, User,Dossier, Document
#import flask-cors
from flask_cors import CORS
#env variable
from dotenv import load_dotenv
import os
os.makedirs('uploads', exist_ok=True)
load_dotenv()
#route for admin access files 
from flask import send_from_directory
from flask_cors import cross_origin
#routes protégées
from flask_jwt_extended import jwt_required, get_jwt_identity

import sentry_sdk
from flask import Flask

from werkzeug.utils import secure_filename

sentry_sdk.init(
    dsn="https://279dc778bc8c309ddeef31e156e66ac7@o4511633338925056.ingest.de.sentry.io/4511633350393936",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)


#create the app
from flask_cors import CORS
app = Flask(__name__)
CORS(
      app, 
      origins =[
             "https://m-motors-react-frontend.netlify.app"
             ]
    )

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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
database_url = os.environ.get("DATABASE_URL", "")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
print("DATABASE_URL =", database_url)

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/vehicules")
def all_vehicules() :
        vehicules =Vehicule.query.all()
        return jsonify([v.to_dict() for v in vehicules])

@app.route("/vehicules/filter")
def index():
        name = request.args.get('name')
        res= db.session.query(Vehicule).filter(Vehicule.name ==name).first()
        return jsonify(res.to_dict())


#Post vehicule
@app.route("/vehicule", methods =["POST"])
@jwt_required()
def create_vehicule():
       data= request.get_json()
       new_vehicule = Vehicule(
        name = data.get("name"),
        description = data.get("description"),
        price = data.get("price"),
        type = data.get("type"),
        kilometrage = data.get("kilometrage"),
        marque = data.get("marque"),
        transmission = data.get("transmission"),
        places = data.get("places")

       )
       db.session.add(new_vehicule)
       db.session.commit()
       return jsonify(new_vehicule.to_dict()),201

#GET vehicule
@app.route("/vehicule/<id>", methods =["GET"])
def get_vehicule(id):

        response = Vehicule.query.get(id)
        if response is None:
                return jsonify({"msg": "Véhicule introuvable"}), 404
        return jsonify(response.to_dict()), 200

#PUT -vehicule
@app.route("/vehicule/<id>", methods =["PUT"])
@jwt_required()
def update_vehicule(id):
        data= request.get_json()
        vehicule_modify = Vehicule.query.get(id)
        vehicule_modify.name = data.get("name")
        vehicule_modify.description = data.get("description")
        vehicule_modify.price = data.get("price")
        vehicule_modify.type = data.get("type")
        vehicule_modify.kilometrage = data.get("kilometrage")
        vehicule_modify.marque = data.get("marque")
        vehicule_modify.transmission = data.get("transmission")
        vehicule_modify.places = data.get("places")

        db.session.commit()
        return jsonify(vehicule_modify.to_dict()),200

#DELETE -vehicule
@app.route("/vehicule/<id>" , methods =["DELETE"])
@jwt_required()
def delete_vehicule(id):
       
        vehicule_delete = Vehicule.query.get(id)
        db.session.delete(vehicule_delete)
        db.session.commit()
        return "",204 


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
                role = "client"
             )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Utilisateur créé avec succès"}), 201

@app.route("/login",methods =[ "POST"])
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

##files 

#create 
@app.route("/dossier", methods =["POST"])
@jwt_required()
def dossier() :
        data= request.get_json()
        user_id = int(get_jwt_identity())
        new_dossier = Dossier(
        user_id =user_id,
        vehicule_id = data.get("vehicule_id"),
        type_financement = data.get("type_financement"),
        revenu_mensuel = data.get("revenu_mensuel"),
        statut = data.get("statut"),
      
        )
        db.session.add(new_dossier)
        db.session.commit()

        return jsonify(new_dossier.to_dict()),201

#read
@app.route("/dossier/<id>", methods=["GET"])
@jwt_required()
def show_files(id):
        response = Dossier.query.get(id)
        return jsonify(response.to_dict()),200


#delete
@app.route('/dossier/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_dossier(id):
    current_user_id = int(get_jwt_identity())  # ← forcer en int
    current_user = User.query.get(current_user_id)
    
    dossier = Dossier.query.get_or_404(id)
    
    if dossier.user_id != current_user_id and current_user.role != "admin":
        return jsonify({"message": "Non autorisé"}), 403
    
    for doc in dossier.documents:
        db.session.delete(doc)
    
    db.session.delete(dossier)
    db.session.commit()
    return jsonify({"message": "Dossier supprimé"}), 200
     
#get client files
@app.route("/dossier", methods =["GET"])
@jwt_required()
def get_all_clients_files():
       user_id = int(get_jwt_identity())
       user = db.session.get(User, user_id)
       
       if user.role =="admin":
          all_files= Dossier.query.all()
       else :
          all_files = Dossier.query.filter_by(user_id= user_id).all()
      
       return jsonify([dossier.to_dict() for dossier in all_files]),200

#ADMIN : get all client files

@app.route("/admin/dossier", methods =["GET"])
@jwt_required()
def admin_all_clients_files():
       user_id = int(get_jwt_identity())

       clientAllFiles = Dossier.query.all()

       bd_user_id = User.query.get(user_id)
       role = bd_user_id.role

       if bd_user_id.role != 'admin' :
              return  jsonify({"message": "Aucun accès autorisé"}),401
       else :
              return jsonify([dossier.to_dict() for dossier in clientAllFiles]),201
       


#PUT  dossier client/admin
@app.route("/dossier/<id>", methods=["PUT"])
@jwt_required()
def update_dossier(id):
    data = request.get_json()
    dossier = db.session.get(Dossier, id)
    
    if "statut" in data:
        dossier.statut = data["statut"]
    if "vehicule_id" in data:
        dossier.vehicule_id = data["vehicule_id"]
    if "type_financement" in data:
        dossier.type_financement = data["type_financement"]
    if "revenu_mensuel" in data:
        dossier.revenu_mensuel = data["revenu_mensuel"]
    
    db.session.commit()
    return jsonify(dossier.to_dict()), 200

#route admin connected
@app.route("/me", methods =["GET"])
@jwt_required()
def get_me() :
      user_id =int(get_jwt_identity())
      user = db.session.get(User,user_id)
      return jsonify(user.to_dict()), 200
       
#route upload doc for client files
@app.route("/document", methods =["POST"])
@jwt_required()
def upload_doc():
        file = request.files.get('file')
        dossier_id =request.form.get('dossier_id')
        doc_type = request.form.get('doc_type')
      

        if not file:
            return jsonify({"message": "Aucun fichier envoyé"}), 400

        if file.filename == "":
            return jsonify({"message": "Nom de fichier vide"}), 400

        if not allowed_file(file.filename):
            return jsonify({"message": "Format non autorisé. Formats acceptés : PDF, PNG, JPG, JPEG"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

        file.save(filepath)
     
        new_doc = Document(
       
        dossier_id = dossier_id,
        doc_type =doc_type,
        filename= filename,
        filepath = filepath
        )
      
        db.session.add(new_doc)
        db.session.commit()
        return jsonify(new_doc.to_dict()),201

#delete doc
@app.route('/document/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_document(id):
    current_user_id = int(get_jwt_identity())
    doc = Document.query.get_or_404(id)
    
    # files belong to client 
    dossier = Dossier.query.get(doc.dossier_id)
    if dossier.user_id != current_user_id:
        return jsonify({"message": "Non autorisé"}), 403
    
    db.session.delete(doc)
    db.session.commit()
    return jsonify({"message": "Document supprimé"}), 200

#route get admin doc client 
@app.route("/dossiers/<int:dossier_id>/documents", methods=["GET"])
@cross_origin()
def get_documents_by_dossier(dossier_id):
    documents = Document.query.filter_by(dossier_id=dossier_id).all()
    print("DOSSIER :", dossier_id)
    print("DOCUMENTS :", documents)
    return jsonify([doc.to_dict() for doc in documents]), 200


@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory("uploads", filename)

#@app.route("/test-sentry")
#def test_sentry():
    #1/0


if __name__ == "__main__":
    app.run(port=5001, debug= True)


  

