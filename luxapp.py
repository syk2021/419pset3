from html import escape
from flask import Flask, request, make_response, redirect, url_for
from common import get_header, get_footer


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
    Label = request.args.get('Label')
    Classification = request.args.get('Classification')
    Agent = request.args.get('Agent')
    Department = request.args.get('Department')
