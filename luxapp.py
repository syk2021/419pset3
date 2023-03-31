from html import escape
from flask import Flask, request, make_response, redirect, url_for


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
    </style>"""
    html += '<form action="search" method="get">'
    html += '<div><label>Label</label><input type="text" name="Label"></div>'
    html += '<div><label>Classification</label><input type="text" name="Classification"></div>'
    html += '<div><label>Agent</label><input type="text" name="Agent"></div>'
    html += '<div><label>Department</label><input type="text" name="Department"></div>'
    html += '</form>'
    html += '</html>'
    print(html)

    response = make_response(html)
    return response

