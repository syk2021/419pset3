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
    return html


def get_form(label="", department="", agent="", classifier=""):
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
    html += f'<div><label>Label</label><input type="text" name="Label" value={label}></div>'
    html += f'<div><label>Classification</label><input type="text" name="Classification" value={classifier}></div>'
    html += f'<div><label>Agent</label><input type="text" name="Agent" value={agent}></div>'
    html += f'<div><label>Department</label><input type="text" name="Department" value={department}></div>'
    html += '<div class="container">'
    html += '<input id="btn" type="submit" value="Search">'
    html += '</div>'
    html += '</form>'

    return html
