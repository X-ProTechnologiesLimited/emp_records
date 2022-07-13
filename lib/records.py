""""
Created on June 09, 2022

@author: Krishnendu Banerjee
@summary: This file holds the functions to perform different search assets in the local database
"""
import urllib.parse
from flask import request, flash, redirect, url_for
from .models import Emp_main, Emp_contact, Emp_bank
from . import errorchecker, response, db
from bson.json_util import dumps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, or_

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
            'Employee Id': record.id,
            'Name': f'<a style="font-weight:bold" href="/get_emp_details/{record.id}"</a>{record.firstname} {record.lastname}',
            'Job Title': record.title,
            'Employment Status': record.status,
            'Employed Since': record.doj,
            'Date of Birth': record.dob,
        })

    emp_data['Total'] = Emp_main.query.count()

    if emp_data['Total'] == 0:  # If no employee records found in database
        return errorchecker.no_employees_in_db()
    else:
        json_data = dumps(emp_data)

    return response.emp_list_form(json_data)


def create_emp_record():
    """
    :author: Krishnendu Banerjee.
    :date: 09/06/2022.
    :description: Function to Create emp records in Database in JSON Format
    :access: public.
    :return: Create Emp records in Database in JSON format
    """
    try:
        new_employee = Emp_main(per_title=request.form.get('per_title'),
                                firstname=request.form.get('firstname'),
                                lastname=request.form.get('lastname'),
                                title=request.form.get('title'),
                                type=request.form.get('type'),
                                status=request.form.get('status'),
                                dob=request.form.get('dob'),
                                doj=request.form.get('doj'),
                                salary=request.form.get('salary'))

        new_employee_contact = Emp_contact(address=request.form.get('address'),
                                           phone=request.form.get('phone'),
                                           mobile=request.form.get('mobile'),
                                           email=request.form.get('email'))

        new_employee_bank = Emp_bank(bank=request.form.get('bank'),
                                     sortcode=request.form.get('sortcode'),
                                     account=request.form.get('account'))

        db.session.add(new_employee)
        db.session.add(new_employee_contact)
        db.session.add(new_employee_bank)
        try:
            db.session.commit()
            return True
        except exc.IntegrityError:
            db.session.rollback()
            return False

    except:
        return errorchecker.internal_server_error()


def update_emp_record(id):
    try:
        emp_profile = Emp_main.query.filter_by(id=id).first()
        emp_contact = Emp_contact.query.filter_by(id=id).first()
        emp_bank = Emp_bank.query.filter_by(id=id).first()
        emp_profile = Emp_main.query.filter_by(id=id).update(dict(per_title=request.form.get('per_title'),
                                                                  firstname=request.form.get('firstname'),
                                                                  title=request.form.get('title'),
                                                                  type=request.form.get('type'),
                                                                  status=request.form.get('status'),
                                                                  dob=request.form.get('dob'),
                                                                  doj=request.form.get('doj'),
                                                                  dol=request.form.get('dol'),
                                                                  salary=request.form.get('salary')))
        emp_contact = Emp_contact.query.filter_by(id=id).update(dict(address=request.form.get('address'),
                                                                     phone=request.form.get('phone'),
                                                                     mobile=request.form.get('mobile'),
                                                                     email=request.form.get('email')))
        emp_bank = Emp_bank.query.filter_by(id=id).update(dict(bank=request.form.get('bank'),
                                                               sortcode=request.form.get('sortcode'),
                                                               account=request.form.get('account')))


        db.session.commit()
        return True
    except:
        return errorchecker.no_employees_in_db


def delete_emp_record(id):
    """
    :author: Krishnendu Banerjee.
    :date: 24/06/2020.
    :description: Function to delete the Standard Employee records
    :access: public.
    :param employee id: This is the Standard employee ID
    :return: commit delete transaction
    """
    employee = Emp_main.query.filter_by(id=id).first()
    if not employee:
        return errorchecker.no_employees_in_db()

    try:
        Emp_main.query.filter_by(id=id).delete()
        Emp_contact.query.filter_by(id=id).delete()
        Emp_bank.query.filter_by(id=id).delete()
        db.session.commit()
        return get_emp_records()
    except:
        return errorchecker.internal_server_error()


def get_emp_name(id):
    employee = Emp_main.query.filter_by(id=id).first()
    name = f'{employee.firstname} {employee.lastname}'
    return name

def get_emp_data(id):
    emp_profile = Emp_main.query.filter_by(id=id).first()
    emp_contact = Emp_contact.query.filter_by(id=id).first()
    emp_bank = Emp_bank.query.filter_by(id=id).first()
    employee = {}
    employee['Profile'] = {}
    employee['Contact'] = {}
    employee['Bank'] = {}

    if not emp_profile:
        return errorchecker.no_employees_in_db

    employee['Profile']['Employee Id'] = emp_profile.id
    employee['Profile']['Title'] = emp_profile.per_title
    employee['Profile']['Firstname'] = emp_profile.firstname
    employee['Profile']['Lastname'] = emp_profile.lastname
    employee['Profile']['Job Title'] = emp_profile.title
    employee['Profile']['Employment Type'] = emp_profile.type
    employee['Profile']['Status'] = emp_profile.status
    employee['Profile']['Date of Birth'] = emp_profile.dob
    employee['Profile']['Employed Since'] = emp_profile.doj
    employee['Profile']['Date of Leaving'] = emp_profile.dol
    employee['Profile']['Salary'] = emp_profile.salary
    employee['Contact']['Address'] = emp_contact.address
    employee['Contact']['Phone Number'] = emp_contact.phone
    employee['Contact']['Mobile Number'] = emp_contact.mobile
    employee['Contact']['Email'] = emp_contact.email
    employee['Bank']['Bank Name'] = emp_bank.bank
    employee['Bank']['SortCode'] = emp_bank.sortcode
    employee['Bank']['Account Number'] = emp_bank.account

    json_data = dumps(employee)
    return response.emp_details_form(json_data, id=id)


def get_emp_profile(id):
    emp_profile = Emp_main.query.filter_by(id=id).first()
    return emp_profile

def get_emp_contact(id):
    emp_contact = Emp_contact.query.filter_by(id=id).first()
    return emp_contact

def get_emp_bank(id):
    emp_bank = Emp_bank.query.filter_by(id=id).first()
    return emp_bank

def search_emp_record(field, value):
    if value == '':
        return errorchecker.no_employees_match()

    keyword = "%{}%".format(value)
    emp_data = {}
    emp_data['Employees'] = []
    if ('Email' not in field) and ('Mobile' not in field):
        q = db.session.query(Emp_main)
        for record in q.filter(or_(getattr(Emp_main, emp_field_map[field]).like(keyword),
                               Emp_main.lastname.like(keyword))).all():
            emp_data['Employees'].append({
                'Employee Id': record.id,
                'Name': f'<a style="font-weight:bold" href="/get_emp_details/{record.id}"</a>{record.firstname} {record.lastname}',
                'Job Title': record.title,
                'Employment Status': record.status,
                'Employed Since': record.doj,
                'Date of Birth': record.dob,
            })

        emp_data['Total'] = q.filter(or_(getattr(Emp_main, emp_field_map[field]).like(keyword),
                                         Emp_main.lastname.like(keyword))).count()

        if emp_data['Total'] == 0:  # If no employee records found in database
            return errorchecker.no_employees_match()
        else:
            json_data = dumps(emp_data)

    else:
        q = db.session.query(Emp_contact)
        if q.filter(getattr(Emp_contact, emp_field_map[field]) == value).count() == 0:
            return errorchecker.no_employees_match()

        emp_contact = q.filter(getattr(Emp_contact, emp_field_map[field]) == value).first()
        emp_id = emp_contact.id
        for record in Emp_main.query.filter_by(id=emp_id).all():
            emp_data['Employees'].append({
                'Employee Id': record.id,
                'Name': f'<a style="font-weight:bold" href="/get_emp_details/{record.id}"</a>{record.firstname} {record.lastname}',
                'Job Title': record.title,
                'Employment Status': record.status,
                'Employed Since': record.doj,
                'Date of Birth': record.dob,
            })

        emp_data['Total'] = Emp_main.query.filter_by(id=emp_id).count()

        if emp_data['Total'] == 0:  # If no employee records found in database
            return errorchecker.no_employees_match()
        else:
            json_data = dumps(emp_data)

    return response.emp_list_form(json_data)

emp_field_map = {
    'Name': 'firstname',
    'Date of Birth': 'dob',
    'Date of Joining': 'doj',
    'Email': 'email',
    'Mobile': 'mobile',
}