from flask import Blueprint, render_template, request
from . import db
from flask_login import login_required, current_user
from . import records
import os, hashlib, os.path
path_to_script = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = '../templates'

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/portal')
@login_required
def portal():
    return render_template('portal.html', name=current_user.name)


@main.route('/employees')
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


@main.route('/get_emp_details/<id>', methods=['GET'])
def get_emp_details(id):
    return records.get_emp_data(id)


@main.route('/employee/search', methods=['GET','POST'])
def search_emp_record():
    if request.method == 'POST':
        field = request.form.get('Field')
        if 'Date' in field:
            return records.search_emp_record(field, request.form.get('date'))
        else:
            return records.search_emp_record(field, request.form.get('keyword'))
    else:
        return render_template('search_employee.html', title='Search Employee', action='/employee/search')
