from html import escape
from flask import Flask, request, make_response, redirect, url_for
from common import get_header, get_footer, get_form, get_style, DB_NAME
from query import LuxQuery, LuxDetailsQuery
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():

    html = get_style()
    html += get_header()
    html += get_form()
    html += get_footer()

    response = make_response(html)
    return response


@app.route('/search', methods=['GET'])
def search():
    label_res = request.args.get('Label')
    classification_res = request.args.get('Classification')
    agent_res = request.args.get('Agent')
    department_res = request.args.get('Department')

    if not label_res and not classification_res and not agent_res and not department_res:
        html = get_style()
        html += get_header()
        html += "No search terms provided. Please enter some search terms."
        html += get_form()
        html += get_footer()
        response = make_response(html)
        return response

    search_response = LuxQuery(DB_NAME).search(agt=agent_res, dep=department_res,
                                               classifier=classification_res, label=label_res)
    search_response = json.loads(search_response)
    print(search_response)
    print(type(search_response))
    response_data = search_response["data"]

    row_gen = ""

    for row in response_data:
        row_gen += '<tr>'
        # Label
        row_gen += f'<td>{row[1]}</td>'
        # Date
        row_gen += f'<td>{row[2]}</td>'
        # Agents
        row_gen += f'<td>{row[3]}</td>'
        # Classified As
        row_gen += f'<td>{row[4]}</td>'
        row_gen += '</tr>'

    html = get_style()
    html += get_header()
    html += get_form()

    html += f"""
    <table>
        <thead>
            <tr>
                <th>Label</th>
                <th>Date</th>
                <th>Agents</th>
                <th>Classified As</th>
            </tr>
        </thead>
        <tbody>
        {row_gen}
        </tbody>
    </table>
    """

    html += get_footer()

    response = make_response(html)
    return response
