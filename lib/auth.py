from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db
from .nocache import nocache
from . import errorchecker
import os, hashlib, os.path
from . import response, records
path_to_script = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = '../templates'

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.portal'))

@auth.route('/employee/new', methods=['GET', 'POST'])
@login_required
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
        if records.create_emp_record() == False:
            flash('Employee Not Created. \n'
                  'A duplicate email record found')
            return redirect(url_for('auth.create_emp_record'))
        else:
            return redirect(url_for('main.get_emp_records'))
    else:
        return render_template('emp_create.html')


@auth.route('/employee/update', methods=['POST'])
@login_required
def update_emp_record():
    id = request.form.get('Id')
    if request.method == 'POST':
        if records.update_emp_record(id) != True:
            flash('Employee is not updated. \n'
                  'A duplicate email record found')
            return records.get_emp_data(id)
        else:
            return records.get_emp_data(id)
    else:
        return render_template('emp_info.html', title='Update Employee', action='/employee/update')

@auth.route('/employee/<action>/<id>', methods=['GET', 'POST'])
@login_required
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


@auth.route('/employee/delete', methods=['GET', 'POST'])
@nocache
@login_required
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



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
