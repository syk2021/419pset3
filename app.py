from html import escape
from flask import Flask, request, make_response, redirect, url_for


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    html = '<!DOCTYPE html>'
    html += '<html>'
    html += '<head>'
    html += 'Hello world'
    html += '</head>'
    html += '</html>'

    response = make_response(html)
    return response

