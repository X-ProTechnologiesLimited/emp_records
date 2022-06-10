""""
Created on June 09, 2022

@author: Krishnendu Banerjee
@summary: This file holds the functions to perform different search assets in the local database
"""
import urllib.parse
from flask import request, flash, redirect, url_for
from .models import Emp_main
from . import errorchecker, response, db, api_main
from bson.json_util import dumps
from sqlalchemy import or_, and_

def get_emp_records():
    """
    :author: Krishnendu Banerjee.
    :date: 09/06/2022.
    :description: Function to Return all emp records in Database in JSON Format
    :access: public.
    :return: Return all emp records in Database in JSON format
    """
    emp_data = {}
    emp_data['Employees'] = []
    for record in Emp_main.query.all():
        emp_data['Employees'].append({
            'Id': record.id,
            'First Name': record.firstname,
            'Last Name': record.lastname,
            'Job Title': record.title,
            'Birth Date': record.dob,
            'Employed Since': record.doj,
            'Salary': record.salary
        })

    emp_data['total'] = Emp_main.query.count()

    if emp_data['total'] == 0:  # If no employee records found in database
        return errorchecker.no_employees_in_db()
    else:
        json_data = dumps(emp_data)

    return response.emp_retrieve(json_data)


def create_emp_record():
    """
    :author: Krishnendu Banerjee.
    :date: 09/06/2022.
    :description: Function to Create emp records in Database in JSON Format
    :access: public.
    :return: Create Emp records in Database in JSON format
    """
    try:
        new_employee = Emp_main(firstname=request.form.get('firstname'),
                                lastname=request.form.get('lastname'),
                                title=request.form.get('title'),
                                dob=request.form.get('dob'),
                                doj=request.form.get('doj'),
                                salary=request.form.get('salary'))

        db.session.add(new_employee)
        db.session.commit()

    except:
        errorchecker.internal_server_error()