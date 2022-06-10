# Filename: lib/response.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the functions to serialise all the different successful responses to a JSON format
"""

from flask import Blueprint, render_template
from os import path
from json2html import *

response = Blueprint('response', __name__)
basepath = path.dirname(__file__)
html_outfile = path.abspath(path.join(basepath, "..", "templates", "search_response.html"))


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

def emp_retrieve(json_data):
    output = json2html.convert(json=json_data,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write('<div class="container">')
        outf.write(output)
        outf.write('</div>')
        outf.write('{% endblock %}')

    return render_template('search_response.html')