
from flask import Flask, request, make_response, render_template, abort
from query import LuxQuery, LuxDetailsQuery, NoSearchResultsError
import json
from time import localtime, asctime

DB_NAME = "./lux.sqlite"

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    html = render_template('index.html', time=asctime(localtime()))
    response = make_response(html)
    return response


@app.route('/search', methods=['GET'])
def search():
    label_search = ""
    classification_search = ""
    agent_search = ""
    department_search = ""

    # if any of the 4 are not null, forget about cookies, and update cookies at the end
    label_search = request.args.get('l')
    classification_search = request.args.get('c')
    agent_search = request.args.get('a')
    department_search = request.args.get('d')

    # else, load cookie values inside to the variables
    if not (label_search or classification_search or agent_search or department_search):
        label_search = request.cookies.get('prev_label', "")
        classification_search = request.cookies.get('prev_classifier', "")
        agent_search = request.cookies.get('prev_agent', "")
        department_search = request.cookies.get('prev_department', "")

    search_response = LuxQuery(DB_NAME).search(agt=agent_search, dep=department_search,
                                               classifier=classification_search, label=label_search)
    search_response = json.loads(search_response)
    response_data = search_response["data"]

    html = render_template('index.html', time=asctime(localtime()), table_data=response_data, prev_label=label_search,
                           prev_classifier=classification_search, prev_agent=agent_search, prev_department=department_search)
    response = make_response(html)

    if label_search:
        response.set_cookie('prev_label', label_search)
    if classification_search:
        response.set_cookie('prev_classifier', classification_search)
    if agent_search:
        response.set_cookie('prev_agent', agent_search)
        print(request.cookies.get('prev_agent'))
    if department_search:
        response.set_cookie('prev_department', department_search)

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

        return response
