
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer,String, Float

from sqlalchemy.orm import Mapped, mapped_column,ForeignKey

#variable interact with db from any files
db = SQLAlchemy()

#define models
#class Vehicule(Base):
   # _tablename_ = "vehicules"

class Vehicule(db.Model):
    id : Mapped[int]=  mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(unique=True)
    description :  Mapped[str]
    price : Mapped[int]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price
        }
    
class User(db.Model):
    id : Mapped[int]=  mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(unique=True)
    email : Mapped[str] =  mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    role :Mapped[str] = mapped_column()

    def to_dict(self) :
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role":self.role
        }
    
class Dossier(db.model): 
    id : Mapped[int]=  mapped_column(primary_key=True)
    user_id : Mapped[int]=  mapped_column(ForeignKey("user.id"))
    vehicule_id : Mapped[int]=  mapped_column(ForeignKey("vehicule.id"))
    type_financement: Mapped[str] = mapped_column()
    revenu_mensuel: Mapped[int]=  mapped_column()
    statut: Mapped[str] = mapped_column()

    def to_dict(self):
        return {

            "id" : self.id,
            "user_id" : self.user_id,
            "vehicule_id" : self.vehicule_id,
            "type_financement": self.type_financement,
            "revenu_mensuel": self.revenu_mensuel,
            "statut": self.statut
        }