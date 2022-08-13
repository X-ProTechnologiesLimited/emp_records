# Filename: lib/errorchecker.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the function to handle all the error messages for the tool

"""

from flask import Blueprint, render_template
from os import path
from json2html import *
from w3lib.html import replace_entities

errorchecker = Blueprint('errorchecker', __name__)
basepath = path.dirname(__file__)
html_outfile = path.abspath(path.join(basepath, "../", "templates", "search_response.html"))

def error_response_creator(message):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to delete the EST Group Assets
    :access: public.
    :param message: This is the error message
    :return: render Jinja template templates/searh_response.html
    """
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    output_escaped = replace_entities(output)
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write('<p></p>')
        outf.write('<div class="container">')
        outf.write(output_escaped)
        outf.write('</div>')
        outf.write('{% endblock %}')

    return render_template('search_response.html')

@errorchecker.errorhandler(501)
def internal_server_error():
    message = {
        'status': 501,
        'message': 'Internal Server Error. Could not update database.'
    }
    return error_response_creator(message)


@errorchecker.errorhandler(502)
def not_implemented_yet():
    message = {
            'status': 502,
            'message': 'This requirement is not yet implemented'
        }
    return error_response_creator(message)


@errorchecker.errorhandler(404)
def no_employees_in_db():
    message = {
            'Message': f'No employees found in your organisation, Create a <a style="font-weight:bold" href="/employee/new"</a>New Employee',
            'Status': 404
        }
    return error_response_creator(message)


@errorchecker.errorhandler(404)
def no_employees_match():
    message = {
            'Message': 'No Employees are matched with the search conditions',
            'Status': 404,
        }
    return error_response_creator(message)


@errorchecker.errorhandler(502)
def input_missing(input_field):
    if input_field == 'EmpId_Radio':
        message_field = 'Please select an Asset radio button from the list.'
    else:
        message_field = 'input field: ' + input_field + ' missing for this request'
    message = {
            'status': 502,
            'message': message_field
        }
    return error_response_creator(message)