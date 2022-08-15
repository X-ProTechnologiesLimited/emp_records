from sqlalchemy import event
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    dob = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    attempt = db.Column(db.Integer, default=0)
    is_locked = db.Column(db.Boolean, default=False)


@event.listens_for(User.__table__, 'after_create')
def create_user(*args, **kwargs):
    db.session.add(User(name='HR Admin', email='admin@app.com', password='admin@123',
                        is_admin=True, is_verified=True, attempt=0))
    db.session.commit()

class Emp_main(db.Model):
    __tablename__ = 'Emp_main'
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
    __tablename__ = 'Emp_contact'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    address = db.Column(db.String(500))
    phone = db.Column(db.Integer)
    mobile = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)

class Emp_bank(db.Model):
    __tablename__ = 'Emp_bank'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    bank = db.Column(db.String(100))
    sortcode = db.Column(db.Integer)
    account = db.Column(db.Integer)