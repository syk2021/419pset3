from html import escape
from flask import Flask, request, make_response, redirect, url_for
from common import get_header, get_footer, DB_NAME
from query import LuxQuery, LuxDetailsQuery
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():

    html = """<!DOCTYPE html>
    <html>
    <style>
      div {
        margin-bottom: 10px;
      }
      label {
        display: inline-block;
        width: 150px;
        text-align: right;
        padding-right: 10px;
      }
      .container{
      text-align: center;
      width: 350px;
      }
    </style>"""
    html += get_header()
    html += '<form action="search" method="get">'
    html += '<div><label>Label</label><input type="text" name="Label"></div>'
    html += '<div><label>Classification</label><input type="text" name="Classification"></div>'
    html += '<div><label>Agent</label><input type="text" name="Agent"></div>'
    html += '<div><label>Department</label><input type="text" name="Department"></div>'
    html += '<div class="container">'
    html += '<input id="btn" type="submit" value="Search">'
    html += '</div>'
    html += '</form>'
    html += get_footer()
    html += '</html>'

    response = make_response(html)
    return response


@app.route('/search', methods=['GET'])
def search():
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

    html = f"""
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

    response = make_response(html)
    return response

