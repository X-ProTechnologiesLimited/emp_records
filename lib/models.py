from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Emp_main(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    per_title = db.Column(db.String(100))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    title = db.Column(db.String(100))
    type = db.Column(db.String(100))
    status = db.Column(db.String(100))
    dob = db.Column(db.String(100))
    doj = db.Column(db.String(100))
    dol = db.Column(db.String(100))
    salary = db.Column(db.Integer)

class Emp_contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    address = db.Column(db.String(500))
    phone = db.Column(db.Integer)
    mobile = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)

class Emp_bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    bank = db.Column(db.String(100))
    sortcode = db.Column(db.Integer)
    account = db.Column(db.Integer)