#!bin/python
from flask import Flask
from flask import render_template, flash, redirect
from forms import LoginForm, SignupForm
import MySQLdb



app = Flask(__name__)
app.config.from_object('config')
db = MySQLdb.connect(host="mysql.server", # your host, usually localhost
                     user="FInalBoss", # your username
                      passwd="final1", # your password
                      db="FInalBoss$default") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * from tblToDo")

# print all the first cell of all the rows
for row in cur.fetchall() :
    print "Rows in tblToDo:"
    print row


@app.route('/index',  methods = ['GET', 'POST'])
def index():
    user = { 'nickname': 'User' }

    tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    },
          {
      'id': 3,
      'title': u'Finish Project',
      'description': u'Need to find finish project for Networking classs',
      'done': False
   },
   {
      'id': 4,
      'title': u'Finish Project',
      'description': u'Need to find finish project for Networking classs',
      'done': False
   }
]


    return render_template('index.html',
        title = 'ToDo List',
        user = user,
        tasks = tasks)


if __name__ == '__main__':
   app.run(debug = True)




@app.route('/NewUser', methods = ['GET', 'POST'])
def NewUser():
    form = SignupForm()

    if form.validate_on_submit():
        flash('Login requested for SignupUserName="' + form.SignupUserName.data + '" SignupPassword="' + form.SignupPassword.data)
        return redirect('/login')
    return render_template('NewUser.html',
        title = 'Sign Up',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        #this executes if button is clicked (both Username and password are required)

        cur = db.cursor()
        # Use all the SQL you like
        cur.execute('SELECT * from tblUsers where UserName ="' + form.UserName.data + '" and Password ="' + form.Password.data + '";')

        # print all the first cell of all the rows
        for row in cur.fetchall() :
            print "Returned rows in tblUsers:"
            print row
            if row:
                #Authentication Successful
                flash('Login requested for UserName="' + form.UserName.data + '" Password="' + form.Password.data + '", remember_me=' + str(form.remember_me.data))
                return redirect('/index')
        #Authentication Fail
        return redirect('/login')

    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])
