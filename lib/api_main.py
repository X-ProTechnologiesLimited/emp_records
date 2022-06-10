# lib/api_main.py
"""
Created on May 27, 2020
@author: Krishnendu Banerjee
@summary: This file is responsible for creating basic APIS for the Flask applications.
"""
import os, hashlib, os.path
from flask import Blueprint, render_template, request, send_from_directory, flash
from .nocache import nocache
from bson.json_util import dumps
from . import response, records
path_to_script = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = '../templates'


api_main = Blueprint('api_main', __name__)

######## Index #########
@api_main.route('/')
def index(): # Load Index.html
    return render_template('index.html')

########### View Employee records ###############
@api_main.route('/employees')
@nocache
def get_emp_records():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls to API to search all assets on the database
    :access: public
    :method: post
    :return: post: module: search; function: search_all_packages
    """
    return records.get_emp_records()


@api_main.route('/employee/new', methods=['GET', 'POST'])
@nocache
def create_emp_record():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls to API to search all assets on the database
    :access: public
    :method: post
    :return: post: module: search; function: search_all_packages
    """
    if request.method == 'POST':
        records.create_emp_record()
        flash('Employee Added Successfully. \n'
              '!!!Warning!!!\n'
              'Refreshing the page will create duplicate record.')
        return get_emp_records()
    else:
        return render_template('create_employee.html')


########## API Shutdown Route ####################

@api_main.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return 'Appliation shutting down...'