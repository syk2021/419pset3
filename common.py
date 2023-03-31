from time import localtime, asctime, strftime

# -----------------------------------------------------------------------


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
