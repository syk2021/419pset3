"""Code for flask application."""
import json
from time import localtime, asctime
from flask import Flask, request, make_response, render_template, abort
from query import LuxQuery, LuxDetailsQuery, NoSearchResultsError
from sqlite3 import OperationalError
import sys
import os


class ServerShutdownException(Exception):
    pass


DB_NAME = "./lux.sqlite"

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Function for '/' route."""
    html = render_template('index.html', time=asctime(localtime()))
    response = make_response(html)
    return response


@app.route('/search', methods=['GET'])
def search():
    """Function for the '/search' route."""

    # if any of the 4 are not null, forget about cookies, and update cookies at the end
    label_search = request.args.get('l', "")
    classification_search = request.args.get('c', "")
    agent_search = request.args.get('a')
    department_search = request.args.get('d', "")

    # else, load cookie values inside to the variables
    if not (label_search or classification_search or agent_search or department_search):
        label_search = request.cookies.get('prev_label', "")
        classification_search = request.cookies.get('prev_classifier', "")
        agent_search = request.cookies.get('prev_agent', "")
        department_search = request.cookies.get('prev_department', "")

    # if no search terms provided, set no_search_terms to True
    no_search_terms = not (
        label_search or classification_search or agent_search or department_search)

    # query the database and select data that we need
    try:
        search_response = LuxQuery(DB_NAME).search(agt=agent_search, dep=department_search,
                                                   classifier=classification_search, label=label_search)
    except OperationalError:
        # if can not query database, then exits with 1
        print(f"Database {DB_NAME} unable to open")
        os._exit(1)

    search_response = json.loads(search_response)
    response_data = search_response["data"]

    # formatting for multiple agents and classifiers
    for obj in response_data:
        obj[3] = obj[3].split(',') if obj[3] else [obj[3]]
        obj[4] = obj[4].split(',') if obj[4] else [obj[4]]

    # render template
    html = render_template('index.html', time=asctime(localtime()), table_data=response_data,
                           prev_label=label_search, prev_classifier=classification_search,
                           prev_agent=agent_search, prev_department=department_search,
                           no_search_terms=no_search_terms)
    response = make_response(html)

    # set cookies
    response.set_cookie('prev_label', label_search)
    response.set_cookie('prev_classifier', classification_search)
    response.set_cookie('prev_agent', agent_search)
    response.set_cookie('prev_department', department_search)

    return response


@app.errorhandler(404)
def page_not_found(error_message):
    """Function for 404 error handler."""

    message = error_message.description
    return render_template("error.html", message=message), 404


@app.route('/obj/', methods=["GET"])
def missing_obj():
    """If object id not provided, abort with 404 and message."""

    abort(404, description="missing object id.")


@app.route('/obj/<object_id>', methods=['GET'])
def search_obj(object_id):
    """Function for the '/obj/<object_id>' route."""

    try:
        search_response = LuxDetailsQuery(DB_NAME).search(object_id)
    except NoSearchResultsError:
        # if no search results, abort with 404 and message
        return abort(404, description=f"no object with id {object_id} exists.")
    except OperationalError:
        # if can not query database, then exits with 1
        print(f"Database {DB_NAME} unable to open")
        os._exit(1)

    # if no exception, then render_template with luxdetails
    search_response = json.loads(search_response)
    html = render_template(
        'luxdetails.html', time=asctime(localtime()), object_id=object_id, search_response=search_response)
    response = make_response(html)

    return response
