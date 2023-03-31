from time import localtime, asctime, strftime

DB_NAME = "./lux.sqlite"


def get_header():
    html = ''
    html += '<hr>'
    html += '<h2>YUAG Collection Search</h2>'
    html += '<hr>'
    return html


def get_footer():
    html = ''
    html += '<hr>'
    html += "CPSC 419 Group #9 Solution.  "
    html += 'Today is ' + asctime(localtime()) + ''
    html += '</html>'
    return html


def get_style():
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
    return html


def get_form():
    html = ""
    html += '<form action="search" method="get">'
    html += '<div><label>Label</label><input type="text" name="Label"></div>'
    html += '<div><label>Classification</label><input type="text" name="Classification"></div>'
    html += '<div><label>Agent</label><input type="text" name="Agent"></div>'
    html += '<div><label>Department</label><input type="text" name="Department"></div>'
    html += '<div class="container">'
    html += '<input id="btn" type="submit" value="Search">'
    html += '</div>'
    html += '</form>'

    return html
