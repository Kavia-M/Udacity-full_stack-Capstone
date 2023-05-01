import os
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'event_management')
DB_PATH = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

database_name = "event_management"
database_path ="postgresql://{}:{}@{}/{}".format('postgres', 'kavia2000','localhost:5432', database_name)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    app.app_context().push()
    db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    hall_1 = Hall('Raj Mahal', 500, 60000, '20, Kuppander Street-1, Pudhupalayam, Gobichettipalayam')
    hall_2 = Hall('Seetha Kalyana Mandapam', 400, 20000, 'Erode, Tamil Nadu')

    hall_1.insert()
    hall_2.insert()

    couple_1 = Couple('Bride', 'groom', '2022-03-28 4:00:55', 'abc@gmail.com', 'Indian Grand look', 1)
    couple_2 = Couple('Bride1', 'groom1', '2023-05-20 3:30:00', 'abcdef@gmail.com', None, None)
    couple_3 = Couple('Bride2', 'groom2', '2023-06-20 3:00:00', 'abcdefghijkl@gmail.com', None, None)

    couple_1.insert()
    couple_2.insert()
    couple_3.insert()

"""
Couple

"""
class Couple(db.Model):
    __tablename__ = 'couple'

    id = Column(Integer, primary_key=True)
    bride_name = Column(String, nullable=False)
    groom_name = Column(String, nullable=False)
    marriage_date = Column(DateTime, nullable=False)
    email_id = Column(String, nullable=False)
    wedding_theme = Column(String, nullable=True)
    hall = db.Column(db.Integer, db.ForeignKey('hall.id', ondelete='SET NULL') , nullable=True)

    def __init__(self, bride_name, groom_name, marriage_date, email_id, wedding_theme, hall):
        self.bride_name = bride_name
        self.groom_name = groom_name
        self.marriage_date =  marriage_date
        self.email_id = email_id
        self.wedding_theme = wedding_theme
        self.hall = hall

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'bride_name': self.bride_name,
            'groom_name': self.groom_name,
            'marriage_date': self.marriage_date,
            'email_id': self.email_id,
            'wedding_theme': self.wedding_theme if self.wedding_theme else 'Yet to be decided',
            'hall': self.hall if self.hall else 'Yet to be decided' 
            }

"""
Hall

"""
class Hall(db.Model):
    __tablename__ = 'hall'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    address = Column(String, nullable=False)

    def __init__(self, name, capacity, price, address):
        self.name = name
        self.capacity = capacity
        self.price = price
        self.address = address
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'capacity (number of persons)': self.capacity,
            'price (per day)': self.price,
            'address': self.address
            }

