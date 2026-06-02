
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer,String, Float

from sqlalchemy.orm import Mapped, mapped_column

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

    def to_register_user(self) :
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role":self.role
        }