# Filename: lib/models.py
"""
Created on June 09, 2022
@author: Krishnendu Banerjee
@summary: This file holds the model/schema for the Database
"""
from . import db

class Emp_main(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    title = db.Column(db.String(100))
    dob = db.Column(db.String(100))
    doj = db.Column(db.String(100))
    salary = db.Column(db.Integer)