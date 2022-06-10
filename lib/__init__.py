# lib/__init__.py
"""
Created on June 9th, 2022

@author: Krishnendu Banerjee
@summary: This file is responsible for creating the main flask application:

"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Setting the flask jinja template render directories
TEMPLATE_DIR = '../templates'
STATIC_DIR = '../static'

# Initializing the Database
db = SQLAlchemy()

# Creating the Flask Application for Asset Generator
def create_app():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Creates Main Flask Application for ADI manager.
    :access: public.
    """
    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

    # Setting the Flask application configuration
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Specifying the database file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    db.init_app(app) # Initialise the application

    from .api_main import api_main as api_main_blueprint  # Import the API module
    app.register_blueprint(api_main_blueprint) # Register application

    return app # Creates and returns the flask application
