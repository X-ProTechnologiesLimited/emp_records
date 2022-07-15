# Filename: lib/response.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the functions to serialise all the different successful responses to a JSON format
"""

from flask import Blueprint, render_template
from os import path
from json2html import *
from w3lib.html import replace_entities

response = Blueprint('response', __name__)
basepath = path.dirname(__file__)
html_outfile = path.abspath(path.join(basepath, "../", "templates", "search_response.html"))


def response_creator(message):
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write('<div class="container">')
        outf.write(output)
        outf.write('</div>')
        outf.write('{% endblock %}')

    return render_template('search_response.html')


def emp_list_form(json_data):
    output = json2html.convert(json=json_data,
                               table_attributes="id=\"Error\" class=\"table table-hover\"" 
                                                "border=2")
    output_escaped = replace_entities(output)
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write('<p></p>')
        outf.write('<div class="container">')
        outf.write('<input type="text" id="myInput" onkeyup="myFunction()" placeholder="Quick Lookup..." title="Type in a name">')
        outf.write(output_escaped)
        outf.write('</div>')
        outf.write('{% endblock %}')

    return render_template('search_response.html')


def emp_details_form(json_data, id):
    output = json2html.convert(json=json_data,
                               table_attributes="id=\"Error\" class=\"table table-hover\"" 
                                                "border=2")

    linkUpdate = f'/employee/update/{id}'
    linkTextUpdate = '<a href="{}">{}</a></button>'.format(linkUpdate, 'Update')
    linkDelete = f'/employee/delete/{id}'
    linkTextDelete = '<a href="{}">{}</a></button>'.format(linkDelete, 'Delete')
    linkBack = f'/employees'
    linkTextBack = '<a href="{}">{}</a></button>'.format(linkBack, 'Back')


    output_escaped = replace_entities(output)
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write('<p></p>')
        outf.write('{% with messages = get_flashed_messages() %}')
        outf.write('{% if messages %}')
        outf.write('<div class="notification is-danger">')
        outf.write('{{ messages[0] }}')
        outf.write('</div>')
        outf.write('{% endif %}')
        outf.write('{% endwith %}')
        outf.write('<div class="container">')
        outf.write('<input type="text" id="myInput" onkeyup="myFunction()" placeholder="Lookup data..." title="Type in a name">')
        outf.write(f'<button class="button is-info is-medium">{linkTextUpdate} ')
        outf.write(f'<button class="button is-info is-medium">{linkTextDelete} ')
        outf.write(f'<button class="button is-info is-medium">{linkTextBack}')
        outf.write('<br>&nbsp;</br>')
        outf.write(output_escaped)
        outf.write('</div>')
        outf.write('{% endblock %}')

    return render_template('search_response.html')