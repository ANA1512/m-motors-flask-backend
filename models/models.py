
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer,String, Float,ForeignKey
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

#variable interact with db from any files
db = SQLAlchemy()

#define models
#class Vehicule(Base):
   # _tablename_ = "vehicules"

class Vehicule(db.Model):
    id : Mapped[int]=  mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column()
    description :  Mapped[str]  = mapped_column()
    price : Mapped[int]  = mapped_column()
    type : Mapped[str] = mapped_column(default ="vente")
    kilometrage : Mapped[int] =mapped_column(default = 0)
    marque: Mapped[str] = mapped_column()
    transmission : Mapped[str] = mapped_column()
    places : Mapped[int] = mapped_column(default =5)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "type" : self.type,
            "kilometrage" : self.kilometrage,
            "marque" : self.marque,
            "transmission" : self.transmission,
            "places" : self.places
        }
    
class User(db.Model):
    id : Mapped[int]=  mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(unique=True)
    email : Mapped[str] =  mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(default="user")

    def to_dict(self) :
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role" :self.role
            
        }
    
class Dossier(db.Model): 
    id : Mapped[int]=  mapped_column(primary_key=True)
    user_id : Mapped[int]=  mapped_column(ForeignKey("user.id"))
    vehicule_id : Mapped[int]=  mapped_column(ForeignKey("vehicule.id"))
    type_financement: Mapped[str] = mapped_column()
    revenu_mensuel: Mapped[Optional[int]] = mapped_column(nullable=True)
    statut: Mapped[str] = mapped_column()

    documents = db.relationship("Document", backref="dossier", lazy=True)

    def to_dict(self):
        return {

            "id" : self.id,
            "user_id" : self.user_id,
            "vehicule_id" : self.vehicule_id,
            "type_financement": self.type_financement,
            "revenu_mensuel": self.revenu_mensuel,
            "statut": self.statut,
            "documents": [doc.to_dict() for doc in self.documents]
        }
    
#Model document
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    dossier_id = db.Column(db.Integer, db.ForeignKey("dossier.id"), nullable=False)

    doc_type = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)

    uploaded_at = db.Column(db.DateTime)

    def to_dict(self):
        return {

            "id" : self.id,
            "dossier_id": self.dossier_id,
            "doc_type" : self.doc_type,
            "filename" : self.filename,
            "filepath": self.filepath
          
        }

