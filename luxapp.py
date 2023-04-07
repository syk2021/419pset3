from html import escape
from flask import Flask, request, make_response, redirect, url_for, render_template, abort
from common import get_header, get_footer, get_form, get_style, DB_NAME
from query import LuxQuery, LuxDetailsQuery, NoSearchResultsError
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
    label_res = request.args.get('l')
    classification_res = request.args.get('c')
    agent_res = request.args.get('a')
    department_res = request.args.get('d')

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

    if request.cookies.get('previous_search') == "True":   
        search_response = LuxQuery(DB_NAME).search(agt=prev_agent, dep=prev_department,
                                                   classifier=prev_classifier, label=prev_label)
    else:
        search_response = LuxQuery(DB_NAME).search(agt=agent_res, dep=department_res,
                                                   classifier=classification_res, label=label_res)
    search_response = json.loads(search_response)
    response_data = search_response["data"]

    html = render_template('index.html', time=asctime(localtime()), table_data=response_data, prev_label=prev_label,
                           prev_classifier=prev_classifier, prev_agent=prev_agent, prev_department=prev_department)
    response = make_response(html)

    if label_res:
        response.set_cookie('prev_label', label_res)
    if classification_res:
        response.set_cookie('prev_classifier', classification_res)
    if agent_res:
        response.set_cookie('prev_agent', agent_res)
        print(request.cookies.get('prev_agent'))
    if department_res:
        response.set_cookie('prev_department', department_res)
    response.set_cookie('previous_search', "False")

    return response

@app.errorhandler(404)
def page_not_found(e):
    message = e.description
    return render_template("error.html", message=message), 404

@app.route('/obj/', methods=["GET"])
def missing_obj():
    abort(404, description="missing object id.")
    
@app.route('/obj/<object_id>', methods=['GET'])
def search_obj(object_id):
    try:
        search_response = LuxDetailsQuery(DB_NAME).search(object_id)
    except NoSearchResultsError:
        abort(404, description=f"no object with id {object_id} exists.")
    else:
        search_response = json.loads(search_response)
        html = render_template(
            'luxdetails.html', object_id=object_id, search_response=search_response)
        response = make_response(html)

        # set previous_search as true
        response.set_cookie('previous_search', "True")
        return response
