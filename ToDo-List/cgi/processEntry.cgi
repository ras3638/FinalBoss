import cgi, cgitb

form = cgi.FieldStorage()

title = form.getvalue('title')
entry = form.getvalue('entry')
