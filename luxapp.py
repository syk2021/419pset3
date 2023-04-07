from html import escape
from flask import Flask, request, make_response, redirect, url_for, render_template
from common import get_header, get_footer, get_form, get_style, DB_NAME
from query import LuxQuery, LuxDetailsQuery
import json
from time import localtime, asctime, strftime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    html = render_template('index.html', time=asctime(localtime()))
    response = make_response(html)
    return response


@app.route('/search', methods=['GET'])
def search():
    # get cookie values
    prev_label = request.cookies.get('prev_label')
    if not prev_label:
        prev_label = ""
    prev_classifier = request.cookies.get('prev_classifier')
    if not prev_classifier:
        prev_classifier = ""
    prev_agent = request.cookies.get('prev_agent')
    if not prev_agent:
        prev_agent = ""
    prev_department = request.cookies.get('prev_department')
    if not prev_department:
        prev_department = ""

    label_res = request.args.get('Label')
    classification_res = request.args.get('Classification')
    agent_res = request.args.get('Agent')
    department_res = request.args.get('Department')

    search_response = LuxQuery(DB_NAME).search(agt=agent_res, dep=department_res,
                                               classifier=classification_res, label=label_res)
    search_response = json.loads(search_response)
    print(search_response)
    print(type(search_response))
    response_data = search_response["data"]

    html = render_template('index.html', time=asctime(localtime()), table_data=response_data, prev_label=prev_label,
                           prev_classifier=prev_classifier, prev_agent=prev_agent, prev_department=prev_department)
    response = make_response(html)
    response.set_cookie('prev_label', label_res)
    response.set_cookie('prev_classifier', classification_res)
    response.set_cookie('prev_agent', agent_res)
    response.set_cookie('prev_department', department_res)

    return response

@app.route('/obj/<int:object_id>', methods=['GET'])
def search_obj(object_id):
    search_response = LuxDetailsQuery(DB_NAME).search(object_id)
    search_response = json.loads(search_response)
    print(type(search_response))
    print(search_response)
    print(search_response["accession_no"])
    html = render_template('luxdetails.html', object_id=object_id, search_response=search_response)
    response = make_response(html)
    return response
