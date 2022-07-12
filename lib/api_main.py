# lib/api_main.py
"""
Created on May 27, 2020
@author: Krishnendu Banerjee
@summary: This file is responsible for creating basic APIS for the Flask applications.
"""
import os, hashlib, os.path
from flask import Blueprint, redirect, url_for, render_template, request, send_from_directory, flash, render_template_string
from .nocache import nocache
from . import errorchecker
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
        if records.create_emp_record() == True:
            flash('Employee Added Successfully. \n'
                '!!!Warning!!!\n'
                'Refreshing the page will create duplicate record.')
        elif records.create_emp_record() == False:
            flash('Employee Not Created. \n'
                  '!!!Error!!!\n'
                  'A duplicate email record found')
        return get_emp_records()
    else:
        return render_template('emp_create.html')

@api_main.route('/employee/delete', methods=['GET', 'POST'])
@nocache
def delete_emp_record():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls to API to search all assets on the database
    :access: public
    :method: post
    :return: post: module: search; function: search_all_packages
    """
    id = request.form.get('Id')
    if request.method == 'POST':
        return records.delete_emp_record(id)
    else:
        return render_template('emp_info.html', title='Delete Employee', action='/employee/delete')


@api_main.route('/employee/<action>/<id>', methods=['GET', 'POST'])
def get_form_employee(id, action):
    emp_profile = records.get_emp_profile(id)
    emp_contact = records.get_emp_contact(id)
    emp_bank = records.get_emp_bank(id)
    emp_name = records.get_emp_name(id)

    if action == 'update':
        return render_template('emp_details.html',
                               Id=emp_profile.id,
                               per_title=emp_profile.per_title,
                               firstname=emp_profile.firstname,
                               lastname=emp_profile.lastname,
                               title=emp_profile.title,
                               type=emp_profile.type,
                               status=emp_profile.status,
                               dob=emp_profile.dob,
                               doj=emp_profile.doj,
                               dol=emp_profile.dol,
                               salary=emp_profile.salary,
                               address=emp_contact.address,
                               phone=emp_contact.phone,
                               mobile=emp_contact.mobile,
                               email=emp_contact.email,
                               bank=emp_bank.bank,
                               sortcode=emp_bank.sortcode,
                               account=emp_bank.account)

    elif action == 'delete':
        return render_template('delete_emp.html', Id=emp_profile.id, Employee_Name=emp_name,
                               title='Delete Employee', action='/employee/delete')


@api_main.route('/get_emp_details/<id>', methods=['GET'])
def get_emp_details(id):
    return records.get_emp_data(id)

@api_main.route('/employee/update', methods=['POST'])
def update_emp_record():
    id = request.form.get('Id')
    if request.method == 'POST':
        if records.update_emp_record(id) == True:
            flash('Employee Updated Successfully. \n')
        else:
            flash('Employee Not Updated. \n')

        return records.get_emp_data(id)
    else:
        return render_template('emp_info.html', title='Update Employee', action='/employee/update')


@api_main.route('/employee/search', methods=['GET','POST'])
def search_emp_record():
    if request.method == 'POST':
        field = request.form.get('Field')
        if 'Date' in field:
            return records.search_emp_record(field, request.form.get('date'))
        else:
            return records.search_emp_record(field, request.form.get('keyword'))
    else:
        return render_template('search_employee.html', title='Search Employee', action='/employee/search')

########## API Shutdown Route ####################

@api_main.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return 'Appliation shutting down...'